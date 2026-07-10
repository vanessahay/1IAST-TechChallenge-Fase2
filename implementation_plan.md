# Plano de Implementação - Pipeline Dataform: PIPE_1IAST_Fase2

## Objetivo
Expandir o pipeline de dados no Dataform no projeto GCP `vanehay` (dataset `1IAST_Fase2`) para materializar seis tabelas da camada Bronze: `bronze_uf`, `bronze_municipio`, `bronze_alunos`, `bronze_meta_alfabetizacao_brasil`, `bronze_meta_alfabetizacao_uf` e `bronze_meta_alfabetizacao_municipio`, todas particionadas pelo campo inteiro `ano`, aplicando regras rigorosas de autocleaning e otimização de consultas SQL.

## Premissas (Assumptions)
1. O repositório Dataform está configurado para apontar para o projeto GCP `vanehay` e localização `US` (localização constatada do dataset `vanehay:1IAST_Fase2`).
2. Como o campo `ano` é do tipo `INTEGER`, a partição no BigQuery é realizada nas seis tabelas através da função `RANGE_BUCKET(ano, GENERATE_ARRAY(2000, 2050, 1))`.
3. Todas as seis tabelas de destino são gerenciadas com o tipo de modelo no Dataform `type: "table"`.
4. As tabelas de origem públicas na `basedosdados` possuem chaves textuais e descrições que requerem padronização de espaços em branco (`TRIM`) e conversão segura de tipos numéricos (`SAFE_CAST`) para prevenção contra anomalias e quebras de execução.

## Arquitetura do Pipeline
*   **Origens (Sources declaradas)**:
    *   `basedosdados.br_inep_avaliacao_alfabetizacao.dicionario`
    *   `basedosdados.br_inep_avaliacao_alfabetizacao.uf`
    *   `basedosdados.br_inep_avaliacao_alfabetizacao.municipio`
    *   `basedosdados.br_inep_avaliacao_alfabetizacao.alunos`
    *   `basedosdados.br_bd_diretorios_brasil.uf`
    *   `basedosdados.br_bd_diretorios_brasil.municipio`
    *   `basedosdados.br_inep_avaliacao_alfabetizacao.meta_alfabetizacao_brasil`
    *   `basedosdados.br_inep_avaliacao_alfabetizacao.meta_alfabetizacao_uf`
    *   `basedosdados.br_inep_avaliacao_alfabetizacao.meta_alfabetizacao_municipio`
*   **Destino (Target Tables)**:
    *   `vanehay.1IAST_Fase2.bronze_uf` (Tabela materializada e particionada por UF com séries escolares).
    *   `vanehay.1IAST_Fase2.bronze_municipio` (Tabela materializada e particionada por Município com séries e redes escolares).
    *   `vanehay.1IAST_Fase2.bronze_alunos` (Tabela materializada e particionada granular por Aluno com proficiência e 5 dicionários consolidados).
    *   `vanehay.1IAST_Fase2.bronze_meta_alfabetizacao_brasil` (Tabela materializada e particionada com metas nacionais).
    *   `vanehay.1IAST_Fase2.bronze_meta_alfabetizacao_uf` (Tabela materializada e particionada com metas estaduais/UF).
    *   `vanehay.1IAST_Fase2.bronze_meta_alfabetizacao_municipio` (Tabela materializada e particionada com metas municipais/IBGE).
*   **Transformações**:
    *   Subconsultas comuns (`CTE`) otimizadas para filtrar dicionários (`dicionario_uf`, `dicionario_municipio`, `dicionario_alunos`) e diretórios (`diretorio_sigla_uf`, `diretorio_id_municipio`), aplicando eliminação de redundância e pushdown de predicados.
    *   Limpeza de strings com `TRIM(...)` em todos os códigos IBGE, siglas, séries, redes, cadernos, presença e status.
    *   Cast seguro (`SAFE_CAST`) em todas as métricas numéricas, proficiências, pesos amostrais, médias de português, metas de alfabetização e campos de ano.

## Estratégia de Implementação
*   **Fase 1: Configuração do Repositório (Setup)**
    *   Manutenção do repositório no GCP Dataform (`PIPE_1IAST_Fase2`) sincronizado com o GitHub (`dev` e `main`).
    *   Criação das 9 declarações de fontes em `definitions/sources/`.
*   **Fase 2: Ingestão, Limpeza e Otimização**
    *   Desenvolvimento dos modelos `bronze_uf.sqlx`, `bronze_municipio.sqlx`, `bronze_alunos.sqlx`, `bronze_meta_alfabetizacao_brasil.sqlx`, `bronze_meta_alfabetizacao_uf.sqlx` e `bronze_meta_alfabetizacao_municipio.sqlx`.
*   **Fase 3: Verificação e Validação SQL**
    *   Validação sintática e de custos usando `bq query --dry_run`.
    *   Execução de amostragem de dados para checar ausência de regressões ou nulos inesperados.

## Profiling Evidence
- [ ] Dataplex Data Profile Job ID: N/A (A verificação via script `dataplex_scanner.py` não se aplica a bases do projeto de terceiros `basedosdados` devido a permissões de criação de recursos `dataplex.datascans` em projetos públicos).
- [ ] Profile Result Summary: Inspeção e verificação realizadas via consultas nativas no BigQuery CLI (`bq query`). A fonte `alunos` consolida o nível mais granular e volumoso de proficiência por aluno, cruzado a 5 dicionários do INEP.

## Verification Plan
*   Verificar sintaxe do SQL de transformação no BigQuery via dry-run para todos os 6 modelos.
*   Confrontar amostras dos dados transformados para garantir o alinhamento de esquemas e consistência dos joins.

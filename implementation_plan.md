# Plano de Implementação - Pipeline Dataform: PIPE_1IAST_Fase2

## Objetivo
Expandir o pipeline de dados no Dataform no projeto GCP `vanehay` (dataset `1IAST_Fase2`) para materializar três tabelas da camada Bronze: `bronze_uf`, `bronze_meta_alfabetizacao_brasil` e `bronze_meta_alfabetizacao_uf`, todas particionadas pelo campo inteiro `ano`, aplicando regras rigorosas de autocleaning e otimização de consultas SQL.

## Premissas (Assumptions)
1. O repositório Dataform está configurado para apontar para o projeto GCP `vanehay` e localização `US` (localização constatada do dataset `vanehay:1IAST_Fase2`).
2. Como o campo `ano` é do tipo `INTEGER`, a partição no BigQuery é realizada nas três tabelas através da função `RANGE_BUCKET(ano, GENERATE_ARRAY(2000, 2050, 1))`.
3. Todas as três tabelas de destino são gerenciadas com o tipo de modelo no Dataform `type: "table"`.
4. As tabelas de origem públicas na `basedosdados` possuem chaves textuais e descrições que requerem padronização de espaços em branco (`TRIM`) e conversão segura de tipos numéricos (`SAFE_CAST`) para prevenção contra anomalias e quebras de execução.

## Arquitetura do Pipeline
*   **Origens (Sources declaradas)**:
    *   `basedosdados.br_inep_avaliacao_alfabetizacao.dicionario`
    *   `basedosdados.br_inep_avaliacao_alfabetizacao.uf`
    *   `basedosdados.br_bd_diretorios_brasil.uf`
    *   `basedosdados.br_inep_avaliacao_alfabetizacao.meta_alfabetizacao_brasil`
    *   `basedosdados.br_inep_avaliacao_alfabetizacao.meta_alfabetizacao_uf`
*   **Destino (Target Tables)**:
    *   `vanehay.1IAST_Fase2.bronze_uf` (Tabela materializada e particionada por UF com séries escolares).
    *   `vanehay.1IAST_Fase2.bronze_meta_alfabetizacao_brasil` (Tabela materializada e particionada com metas nacionais).
    *   `vanehay.1IAST_Fase2.bronze_meta_alfabetizacao_uf` (Tabela materializada e particionada com metas estaduais/UF).
*   **Transformações**:
    *   Subconsulta comum (`CTE`) otimizada para filtrar o dicionário e o diretório de UFs (`diretorio_sigla_uf`), aplicando eliminação de redundância e pushdown de predicados.
    *   Limpeza de strings com `TRIM(...)` em todos os campos de texto e junções (`sigla`, `serie`, `rede`).
    *   Cast seguro (`SAFE_CAST`) em todas as métricas numéricas, metas de alfabetização (2024-2030) e campos de ano.

## Estratégia de Implementação
*   **Fase 1: Configuração do Repositório (Setup)**
    *   Manutenção do repositório no GCP Dataform (`PIPE_1IAST_Fase2`) sincronizado com o GitHub (`dev` e `main`).
    *   Criação das 5 declarações de fontes em `definitions/sources/`.
*   **Fase 2: Ingestão, Limpeza e Otimização**
    *   Desenvolvimento dos modelos `bronze_uf.sqlx`, `bronze_meta_alfabetizacao_brasil.sqlx` e `bronze_meta_alfabetizacao_uf.sqlx`.
*   **Fase 3: Verificação e Validação SQL**
    *   Validação sintática e de custos usando `bq query --dry_run`.
    *   Execução de amostragem de dados para checar ausência de regressões ou nulos inesperados.

## Profiling Evidence
- [ ] Dataplex Data Profile Job ID: N/A (A verificação via script `dataplex_scanner.py` não se aplica a bases do projeto de terceiros `basedosdados` devido a permissões de criação de recursos `dataplex.datascans` em projetos públicos).
- [ ] Profile Result Summary: Inspeção e verificação realizadas via consultas nativas no BigQuery CLI (`bq query`). A fonte `meta_alfabetizacao_uf` consolida as metas regionais por estado, cobrindo com precisão as unidades da federação cadastradas no diretório.

## Verification Plan
*   Verificar sintaxe do SQL de transformação no BigQuery via dry-run para todos os modelos.
*   Confrontar amostras dos dados transformados para garantir o alinhamento de esquemas e consistência dos joins.

# Plano de Implementação - Pipeline Dataform: PIPE_1IAST_Fase2

## Objetivo
Expandir o pipeline de dados no Dataform no projeto GCP `vanehay` (dataset `1IAST_Fase2`) para materializar duas tabelas da camada Bronze: `bronze_uf` e `bronze_meta_alfabetizacao_brasil`, ambas particionadas pelo campo inteiro `ano`, aplicando regras rigorosas de autocleaning e otimização de consultas SQL.

## Premissas (Assumptions)
1. O repositório Dataform está configurado para apontar para o projeto GCP `vanehay` e localização `US` (localização constatada do dataset `vanehay:1IAST_Fase2`).
2. Como o campo `ano` é do tipo `INTEGER`, a partição no BigQuery é realizada em ambas as tabelas através da função `RANGE_BUCKET(ano, GENERATE_ARRAY(2000, 2050, 1))`.
3. Ambas as tabelas de destino são gerenciadas com o tipo de modelo no Dataform `type: "table"`.
4. As tabelas de origem públicas na `basedosdados` possuem chaves textuais e descrições que requerem padronização de espaços em branco (`TRIM`) e conversão segura de tipos numéricos (`SAFE_CAST`) para prevenção contra anomalias e quebras de execução.

## Arquitetura do Pipeline
*   **Origens (Sources declaradas)**:
    *   `basedosdados.br_inep_avaliacao_alfabetizacao.dicionario`
    *   `basedosdados.br_inep_avaliacao_alfabetizacao.uf`
    *   `basedosdados.br_bd_diretorios_brasil.uf`
    *   `basedosdados.br_inep_avaliacao_alfabetizacao.meta_alfabetizacao_brasil`
*   **Destino (Target Tables)**:
    *   `vanehay.1IAST_Fase2.bronze_uf` (Tabela materializada e particionada por UF).
    *   `vanehay.1IAST_Fase2.bronze_meta_alfabetizacao_brasil` (Tabela materializada e particionada com metas nacionais).
*   **Transformações**:
    *   Subconsulta comum (`CTE`) otimizada para filtrar o dicionário em `bronze_uf` uma única vez para `serie` e `rede`, aplicando eliminação de redundância (Common Subexpression Reuse) e pushdown de predicados.
    *   Limpeza de strings com `TRIM(...)` em todos os campos de texto e junções (`sigla`, `serie`, `rede`).
    *   Cast seguro (`SAFE_CAST`) em todas as métricas numéricas, metas de alfabetização (2024-2030) e campos de ano.

## Estratégia de Implementação
*   **Fase 1: Configuração do Repositório (Setup)**
    *   Manutenção do repositório no GCP Dataform (`PIPE_1IAST_Fase2`) sincronizado com o GitHub na agulha `main`.
    *   Criação das 4 declarações de fontes em `definitions/sources/`.
*   **Fase 2: Ingestão, Limpeza e Otimização**
    *   Desenvolvimento de `definitions/bronze_uf.sqlx` e `definitions/bronze_meta_alfabetizacao_brasil.sqlx` aplicando o protocolo `@skill:data-autocleaning` e `@skill:developing-with-bigquery`.
*   **Fase 3: Verificação e Validação SQL**
    *   Validação sintática e de custos usando `bq query --dry_run`.
    *   Execução de amostragem de dados para checar ausência de regressões ou nulos inesperados.

## Profiling Evidence
- [ ] Dataplex Data Profile Job ID: N/A (A verificação via script `dataplex_scanner.py` não se aplica a bases do projeto de terceiros `basedosdados` devido a permissões de criação de recursos `dataplex.datascans` em projetos públicos).
- [ ] Profile Result Summary: Inspeção e verificação realizadas via consultas nativas no BigQuery CLI (`bq query`). A fonte `meta_alfabetizacao_brasil` possui 3 registros agregando as taxas e metas evolutivas do Brasil (2024 a 2030). O dataset `uf` possui 145 registros (2023 e 2024), e as tabelas de dicionário e diretório possuem 27 registros cada (mapeando as 27 UFs do Brasil).

## Verification Plan
*   Verificar sintaxe do SQL de transformação no BigQuery via dry-run para ambos os modelos.
*   Confrontar amostras dos dados transformados para garantir o alinhamento de esquemas e consistência dos joins.

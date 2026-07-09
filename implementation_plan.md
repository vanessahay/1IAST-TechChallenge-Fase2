# Plano de Implementação - Pipeline Dataform: PIPE_1IAST_Fase2

## Objetivo
Criar um pipeline de dados no Dataform no projeto GCP `vanehay` (dataset `1IAST_Fase2`) para gerar a tabela `bronze_uf` particionada pelo campo inteiro `ano`, aplicando regras rigorosas de autocleaning e otimização de consultas SQL.

## Premissas (Assumptions)
1. O repositório Dataform está configurado para apontar para o projeto GCP `vanehay` e localização `US` (localização constatada do dataset `vanehay:1IAST_Fase2`).
2. Como o campo `ano` é do tipo `INTEGER`, a partição no BigQuery será realizada através da função `RANGE_BUCKET(ano, GENERATE_ARRAY(2000, 2050, 1))`.
3. Por se tratar da criação de uma nova tabela (a tabela `bronze_uf` não existe atualmente no dataset), o tipo do modelo no Dataform será definido como `type: "table"`.
4. As tabelas de origem públicas na `basedosdados` possuem chaves textuais e descrições que requerem padronização de espaços em branco (`TRIM`) e conversão segura de tipos numéricos (`SAFE_CAST`) para prevenção contra anomalias e quebras de execução.

## Arquitetura do Pipeline
*   **Origens (Sources declaradas)**:
    *   `basedosdados.br_inep_avaliacao_alfabetizacao.dicionario`
    *   `basedosdados.br_inep_avaliacao_alfabetizacao.uf`
    *   `basedosdados.br_bd_diretorios_brasil.uf`
*   **Destino (Target Table)**:
    *   `vanehay.1IAST_Fase2.bronze_uf` (Tabela materializada e particionada).
*   **Transformações**:
    *   Subconsulta comum (`CTE`) otimizada para filtrar o dicionário uma única vez para `serie` e `rede`, aplicando eliminação de redundância (Common Subexpression Reuse) e pushdown de predicados.
    *   Limpeza de strings com `TRIM(...)` nas chaves de junção (`sigla`, `serie`, `rede`).
    *   Cast seguro (`SAFE_CAST`) em todas as métricas numéricas e no campo de ano.

## Estratégia de Implementação
*   **Fase 1: Configuração do Repositório (Setup)**
    *   Criação de `workflow_settings.yaml`, `.df-credentials.json` e `package.json`.
    *   Criação das declarações das 3 tabelas de origem em `definitions/sources/`.
*   **Fase 2: Ingestão, Limpeza e Otimização**
    *   Desenvolvimento de `definitions/bronze_uf.sqlx` aplicando o protocolo `@skill:data-autocleaning` e `@skill:developing-with-bigquery`.
    *   Configuração do particionamento por faixa de inteiros na coluna `ano`.
*   **Fase 3: Verificação e Validação SQL**
    *   Validação sintática e de custos usando `bq query --dry_run`.
    *   Execução de amostragem de dados para checar junções e ausência de regressões ou nulos inesperados.

## Profiling Evidence
- [ ] Dataplex Data Profile Job ID: N/A (A verificação via script `dataplex_scanner.py` retornou erro `403 Permission Denied` pois as tabelas residem no projeto de terceiros `basedosdados`, no qual não temos permissão para criar recursos `dataplex.datascans`).
- [ ] Profile Result Summary: Inspeção e verificação realizadas via consultas nativas no BigQuery CLI (`bq query`). O dataset de origem `basedosdados.br_inep_avaliacao_alfabetizacao.uf` possui 145 registros abrangendo os anos de 2023 e 2024. As tabelas de dicionário e diretório possuem 27 registros cada, mapeando corretamente as 27 Unidades da Federação do Brasil.

## Verification Plan
*   Verificar sintaxe do SQL de transformação no BigQuery via dry-run.
*   Confrontar uma amostra dos dados transformados para garantir o alinhamento de esquemas e consistência dos joins.

# 1IAST - Tech Challenge Fase 2: Pipeline Dataform (`bronze_uf`, `bronze_meta_alfabetizacao_brasil`, `bronze_meta_alfabetizacao_uf` e `bronze_meta_alfabetizacao_municipio`)

Repositório contendo o pipeline de transformação e carga de dados no **Google Cloud Dataform** (Projeto: `vanehay`, Dataset: `1IAST_Fase2`, Repositório: `PIPE_1IAST_Fase2`), responsável por materializar as quatro tabelas particionadas da camada Bronze no BigQuery.

## 📁 Estrutura do Projeto

- `workflow_settings.yaml`: Configuração principal do repositório Dataform (Core v3.0.0, localização US).
- `definitions/sources/`: Declarações de fontes da Base dos Dados (`dicionario`, `uf`, diretório de UFs, diretório de Municípios, `meta_alfabetizacao_brasil`, `meta_alfabetizacao_uf` e `meta_alfabetizacao_municipio`).
- `definitions/bronze_uf.sqlx`: Modelo SQLX de carga da camada Bronze com indicadores estaduais de alfabetização.
- `definitions/bronze_meta_alfabetizacao_brasil.sqlx`: Modelo SQLX consolidador de metas evolutivas nacionais (2024-2030).
- `definitions/bronze_meta_alfabetizacao_uf.sqlx`: Modelo SQLX de carga de metas evolutivas regionais por Unidade da Federação, enriquecida com o nome dos estados.
- `definitions/bronze_meta_alfabetizacao_municipio.sqlx`: Modelo SQLX granular por município com metas e taxas de alfabetização do INEP, enriquecido com os nomes oficiais dos municípios pelo IBGE.
- `walkthrough.md`: Documentação técnica completa, evidências de validação e sumários de qualidade.
- `implementation_plan.md`: Plano arquitetural e estratégia de implementação do pipeline.

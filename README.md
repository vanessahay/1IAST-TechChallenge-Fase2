# 1IAST - Tech Challenge Fase 2: Pipeline Dataform (`bronze_uf` e `bronze_meta_alfabetizacao_brasil`)

Repositório contendo o pipeline de transformação e carga de dados no **Google Cloud Dataform** (Projeto: `vanehay`, Dataset: `1IAST_Fase2`, Repositório: `PIPE_1IAST_Fase2`), responsável por materializar as tabelas particionadas **`bronze_uf`** e **`bronze_meta_alfabetizacao_brasil`** no BigQuery.

## 📁 Estrutura do Projeto

- `workflow_settings.yaml`: Configuração principal do repositório Dataform (Core v3.0.0, localização US).
- `definitions/sources/`: Declarações de fontes da Base dos Dados (`dicionario`, `uf`, diretório de UFs e `meta_alfabetizacao_brasil`).
- `definitions/bronze_uf.sqlx`: Modelo SQLX de carga da camada Bronze estelar aplicando particionamento por inteiro (`RANGE_BUCKET` em `ano`), limpeza automática (`TRIM`, `SAFE_CAST`) e otimização de consultas (CTE reutilizada, pushdown de predicados).
- `definitions/bronze_meta_alfabetizacao_brasil.sqlx`: Modelo SQLX consolidador de metas evolutivas nacionais (2024-2030), aplicando particionamento por ano e normalização/cast seguro de indicadores numéricos.
- `walkthrough.md`: Documentação técnica completa, evidências de validação e sumários de qualidade.
- `implementation_plan.md`: Plano arquitetural e estratégia de implementação do pipeline.

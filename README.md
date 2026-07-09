# 1IAST - Tech Challenge Fase 2: Pipeline Dataform (`bronze_uf`)

Repositório contendo o pipeline de transformação e carga de dados no **Google Cloud Dataform** (Projeto: `vanehay`, Dataset: `1IAST_Fase2`), responsável por materializar a tabela particionada **`bronze_uf`** no BigQuery.

## 📁 Estrutura do Projeto

- `workflow_settings.yaml`: Configuração principal do repositório Dataform (Core v3.0.0, localização US).
- `definitions/sources/`: Declarações de fontes da Base dos Dados (`dicionario`, `uf`, diretório).
- `definitions/bronze_uf.sqlx`: Modelo SQLX de carga da camada Bronze aplicando particionamento por inteiro (`RANGE_BUCKET` em `ano`), limpeza automática (`TRIM`, `SAFE_CAST`) e otimização de consultas (CTE reutilizada, pushdown de predicados).
- `walkthrough.md`: Documentação técnica completa, evidências de validação e sumários de qualidade.
- `implementation_plan.md`: Plano arquitetural e estratégia de implementação do pipeline.

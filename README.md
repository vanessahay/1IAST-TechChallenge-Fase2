# 1IAST - Tech Challenge Fase 2: Pipeline Dataform (Arquitetura Medalhão + Regras de Qualidade)

Repositório contendo o pipeline de engenharia, transformação e governança de dados no **Google Cloud Dataform** (Projeto: `vanehay`, Dataset: `1IAST_Fase2`, Repositório: `PIPE_1IAST_Fase2`), estruturado na **Arquitetura Medalhão Completa (Bronze + Prata + Ouro)** e certificado com uma **Suite Robusta de Qualidade de Dados (Assertions)**.

## 📁 Estrutura do Projeto

- `workflow_settings.yaml`: Configuração principal do repositório Dataform (Core v3.0.61, localização US).
- `definitions/sources/`: Declarações das 7 fontes (INEP, diretórios IBGE e tabela de aterrissagem streaming do Pub/Sub).
- `definitions/bronze_*.sqlx`: 6 tabelas da Camada Bronze (Batch históricos `bronze_uf`, `bronze_municipio`, `bronze_alunos` + Incrementais streaming `bronze_meta_alfabetizacao_*`).
- `definitions/silver_*.sqlx`: 4 tabelas da Camada Prata (`silver_alfabetizacao_brasil`, `silver_alfabetizacao_uf`, `silver_alfabetizacao_municipio`, `silver_alunos_enriquecidos`).
- `definitions/gold_*.sqlx`: 4 tabelas da Camada Ouro (Dashboards BI `gold_indicadores_municipais`, Governança `gold_comparativo_metas_resultados`, Estatística `gold_evolucao_temporal_indicadores`, Machine Learning `gold_dataset_ml_proficiencia_alunos`).
- `definitions/assertions/assert_duplicidade_silver_municipio.sqlx`: Asserção verificando duplicidade na chave composta municipal.
- `definitions/assertions/assert_valores_ausentes_gold_kpis.sqlx`: Asserção detectando valores ausentes ou chaves nulas na camada Ouro.
- `definitions/assertions/assert_fk_relacionamento_municipios.sqlx`: Asserção validando integridade referencial com o diretório oficial do IBGE.
- `definitions/assertions/assert_consistencia_macro_brasil_vs_uf.sqlx`: Asserção checando consistência cruzada entre agregações estaduais e nacionais.
- `walkthrough.md`: Documentação técnica completa, evidências de validação e sumários das regras de governança e qualidade.
- `implementation_plan.md`: Plano arquitetural da Arquitetura Medalhão com Quality Suite.

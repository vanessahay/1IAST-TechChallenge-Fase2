# 1IAST - Tech Challenge Fase 2: Pipeline Dataform (Arquitetura Medalhão Completa: Bronze + Prata + Ouro)

Repositório contendo o pipeline de engenharia e transformação de dados no **Google Cloud Dataform** (Projeto: `vanehay`, Dataset: `1IAST_Fase2`, Repositório: `PIPE_1IAST_Fase2`), estruturado na **Arquitetura Medalhão Completa** com 14 tabelas organizadas em **Bronze** (Batch + Streaming), **Prata** (Dados Tratados) e **Ouro** (Dashboards BI, Análise Estatística e Treinamento de Machine Learning).

## 📁 Estrutura do Projeto

- `workflow_settings.yaml`: Configuração principal do repositório Dataform (Core v3.0.61, localização US).
- `definitions/sources/`: Declarações de fontes da Base dos Dados (`dicionario`, `uf`, `municipio`, `alunos`, diretórios do IBGE) e a declaração de aterrissagem streaming do Pub/Sub (`vanehay_landing_eventos_indicadores.sqlx`).
- `definitions/bronze_*.sqlx`: 6 modelos da Camada Bronze (Batch históricos `bronze_uf`, `bronze_municipio`, `bronze_alunos` + Incrementais streaming `bronze_meta_alfabetizacao_*`).
- `definitions/silver_*.sqlx`: 4 modelos da Camada Prata (`silver_alfabetizacao_brasil`, `silver_alfabetizacao_uf`, `silver_alfabetizacao_municipio`, `silver_alunos_enriquecidos`), limpos, normalizados (`LPAD` 7 dígitos) e integrados relacionalmente.
- `definitions/gold_indicadores_municipais.sqlx`: Modelo Ouro para **Dashboards BI**, categorizando o status de atingimento de meta de todos os municípios.
- `definitions/gold_comparativo_metas_resultados.sqlx`: Modelo Ouro para **Governança Multi-Nível**, comparando metas e resultados no Brasil, UF e Município.
- `definitions/gold_evolucao_temporal_indicadores.sqlx`: Modelo Ouro para **Análise Estatística**, com séries longitudinais, variação anual (`LAG`) e média móvel trienal (`AVG OVER PRECEDING`).
- `definitions/gold_dataset_ml_proficiencia_alunos.sqlx`: Modelo Ouro para **Machine Learning**, com *feature engineering* relacional, alvos contínuos (Regressão) e binários (Classificação de Risco).
- `walkthrough.md`: Documentação técnica detalhada, evidências de validação e sumários das diretrizes do pipeline.
- `implementation_plan.md`: Plano arquitetural e estratégia da Arquitetura Medalhão Completa.

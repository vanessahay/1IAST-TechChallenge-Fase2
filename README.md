# 1IAST - Tech Challenge Fase 2: Pipeline Dataform (Arquitetura Medalhão: Bronze Híbrida + Prata Integrada)

Repositório contendo o pipeline de engenharia e transformação de dados no **Google Cloud Dataform** (Projeto: `vanehay`, Dataset: `1IAST_Fase2`, Repositório: `PIPE_1IAST_Fase2`), estruturado na **Arquitetura Medalhão** para integrar cargas históricas (Batch) e medições evolutivas em tempo real (Streaming), consolidando tudo na **Camada Prata (Silver Layer - Dados Tratados e Integrados)**.

## 📁 Estrutura do Projeto

- `workflow_settings.yaml`: Configuração principal do repositório Dataform (Core v3.0.61, localização US).
- `definitions/sources/`: Declarações de fontes da Base dos Dados (`dicionario`, `uf`, `municipio`, `alunos`, diretórios do IBGE) e a declaração de aterrissagem streaming do Pub/Sub (`vanehay_landing_eventos_indicadores.sqlx`).
- `definitions/bronze_uf.sqlx`: Modelo Batch da camada Bronze com indicadores estaduais de alfabetização.
- `definitions/bronze_municipio.sqlx`: Modelo Batch da camada Bronze com indicadores municipais de alfabetização, séries e redes.
- `definitions/bronze_alunos.sqlx`: Modelo Batch da camada Bronze granular por Aluno com proficiência e dicionários consolidados.
- `definitions/bronze_meta_alfabetizacao_brasil.sqlx`: Modelo Incremental da camada Bronze alimentado via streaming do Pub/Sub com metas do Brasil.
- `definitions/bronze_meta_alfabetizacao_uf.sqlx`: Modelo Incremental da camada Bronze alimentado via streaming com metas regionais por UF.
- `definitions/bronze_meta_alfabetizacao_municipio.sqlx`: Modelo Incremental da camada Bronze alimentado via streaming com metas por Município.
- `definitions/silver_alfabetizacao_brasil.sqlx`: Modelo Prata consolidando metas nacionais e desvio de meta.
- `definitions/silver_alfabetizacao_uf.sqlx`: Modelo Prata integrando avaliações estaduais históricas e metas em streaming, com desvio de meta.
- `definitions/silver_alfabetizacao_municipio.sqlx`: Modelo Prata integrando avaliações municipais e metas com normalização de 7 dígitos IBGE.
- `definitions/silver_alunos_enriquecidos.sqlx`: Modelo Prata com registros individuais de Alunos normalizados e enriquecidos com a meta municipal.
- `walkthrough.md`: Documentação técnica detalhada, evidências de validação e sumários das 5 diretrizes de tratamento.
- `implementation_plan.md`: Plano arquitetural e estratégia da Arquitetura Medalhão.

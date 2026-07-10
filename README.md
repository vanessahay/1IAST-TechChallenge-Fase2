# 1IAST - Tech Challenge Fase 2: Pipeline Dataform (Camada Bronze Híbrida: Batch + Streaming Incremental)

Repositório contendo o pipeline de engenharia e transformação de dados no **Google Cloud Dataform** (Projeto: `vanehay`, Dataset: `1IAST_Fase2`, Repositório: `PIPE_1IAST_Fase2`), onde a **Camada Bronze** consolida em perfeita harmonia cargas históricas em lote (Batch) e atualizações evolutivas em tempo real (Streaming Incremental).

## 📁 Estrutura do Projeto

- `workflow_settings.yaml`: Configuração principal do repositório Dataform (Core v3.0.61, localização US).
- `definitions/sources/`: Declarações de fontes da Base dos Dados (`dicionario`, `uf`, `municipio`, `alunos`, diretório de UFs, diretório de Municípios) e a declaração de aterrissagem streaming do Pub/Sub (`vanehay_landing_eventos_indicadores.sqlx`).
- `definitions/bronze_uf.sqlx`: Modelo Batch da camada Bronze com indicadores estaduais de alfabetização.
- `definitions/bronze_municipio.sqlx`: Modelo Batch da camada Bronze com indicadores municipais de alfabetização, séries e redes.
- `definitions/bronze_alunos.sqlx`: Modelo Batch da camada Bronze granular por Aluno com proficiência e dicionários consolidados.
- `definitions/bronze_meta_alfabetizacao_brasil.sqlx`: Modelo Incremental da camada Bronze alimentado via streaming do Pub/Sub com metas e taxas evolutivas do Brasil.
- `definitions/bronze_meta_alfabetizacao_uf.sqlx`: Modelo Incremental da camada Bronze alimentado via streaming com metas regionais por UF e cruzamento com o IBGE.
- `definitions/bronze_meta_alfabetizacao_municipio.sqlx`: Modelo Incremental da camada Bronze alimentado via streaming com metas granulares por Município e IBGE.
- `walkthrough.md`: Documentação técnica detalhada, evidências de validação e sumários de limpezas/otimizações.
- `implementation_plan.md`: Plano arquitetural e estratégia de implementação da Camada Bronze Híbrida.

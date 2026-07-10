# 1IAST - Tech Challenge Fase 2: Pipeline Dataform (Arquitetura Híbrida: Batch + Streaming Incremental)

Repositório contendo o pipeline de engenharia e transformação de dados no **Google Cloud Dataform** (Projeto: `vanehay`, Dataset: `1IAST_Fase2`, Repositório: `PIPE_1IAST_Fase2`), estruturado para processar em harmonia cargas históricas em lote (Batch) e eventos de atualização contínua em tempo real (Streaming).

## 📁 Estrutura do Projeto

- `workflow_settings.yaml`: Configuração principal do repositório Dataform (Core v3.0.61, localização US).
- `definitions/sources/`: Declarações de fontes da Base dos Dados (`dicionario`, `uf`, `municipio`, `alunos`, diretório de UFs, diretório de Municípios) e a declaração de aterrissagem streaming do Pub/Sub (`vanehay_landing_eventos_indicadores.sqlx`).
- `definitions/bronze_uf.sqlx`: Modelo Batch da camada Bronze com indicadores estaduais de alfabetização.
- `definitions/bronze_municipio.sqlx`: Modelo Batch da camada Bronze com indicadores municipais de alfabetização, séries e redes.
- `definitions/bronze_alunos.sqlx`: Modelo Batch da camada Bronze granular por Aluno com proficiência e dicionários consolidados.
- `definitions/silver_atualizacao_medicoes_desempenho.sqlx`: Modelo Incremental da camada Prata para processamento em tempo real de novas medições, atualização de indicadores e revisão de metas via Pub/Sub.
- `walkthrough.md`: Documentação técnica detalhada, evidências de validação e sumários de limpezas/otimizações.
- `implementation_plan.md`: Plano arquitetural e estratégia de implementação híbrida.

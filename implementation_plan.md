# Plano de Implementação - Pipeline Dataform: PIPE_1IAST_Fase2 (Arquitetura Híbrida: Batch + Streaming Incremental)

## Objetivo
Estabelecer no Google Cloud Dataform no projeto GCP `vanehay` (dataset `1IAST_Fase2`) uma **Arquitetura Híbrida de Ingestão de Dados (Batch + Streaming Incremental)**:
- **Camada Bronze Batch (Histórico Consolidado)**: Materialização das três tabelas fundamentais de avaliação do INEP (`bronze_uf`, `bronze_municipio` e `bronze_alunos`), particionadas pelo campo inteiro `ano` via `RANGE_BUCKET`.
- **Camada Prata Incremental (Streaming em Tempo Real)**: Processamento contínuo de atualizações de indicadores, novas medições de desempenho e revisões de metas através do modelo incremental `silver_atualizacao_medicoes_desempenho`, consumindo eventos em tempo real da tabela de aterrissagem `landing_eventos_indicadores` (alimentada diretamente por assinatura do Cloud Pub/Sub).

## Premissas (Assumptions)
1. O repositório Dataform (`PIPE_1IAST_Fase2`) está configurado na região `US` rodando na versão do Dataform Core `3.0.61` para total sincronia com os *workspaces* do console GCP.
2. A separação clara entre cargas históricas (Batch) e medições/atualizações contínuas (Streaming) elimina redundância de processamento e garante latência próxima de zero para atualizações de indicadores.
3. O modelo incremental `silver_atualizacao_medicoes_desempenho` utiliza a cláusula dinâmica `when(incremental(), ...)` para filtrar mensagens pelo carimbo `publish_time`, reduzindo custos computacionais no BigQuery.

## Arquitetura do Pipeline
*   **Origens Batch Declaradas**:
    *   `basedosdados.br_inep_avaliacao_alfabetizacao.dicionario`
    *   `basedosdados.br_inep_avaliacao_alfabetizacao.uf`
    *   `basedosdados.br_inep_avaliacao_alfabetizacao.municipio`
    *   `basedosdados.br_inep_avaliacao_alfabetizacao.alunos`
    *   `basedosdados.br_bd_diretorios_brasil.uf`
    *   `basedosdados.br_bd_diretorios_brasil.municipio`
*   **Origens Streaming Declaradas**:
    *   `vanehay.1IAST_Fase2.landing_eventos_indicadores` (Tabela Landing do Cloud Pub/Sub Direct Subscription)
*   **Destino Batch (Camada Bronze Histórica - `type: "table"`)**:
    *   `vanehay.1IAST_Fase2.bronze_uf`
    *   `vanehay.1IAST_Fase2.bronze_municipio`
    *   `vanehay.1IAST_Fase2.bronze_alunos`
*   **Destino Streaming (Camada Prata Incremental - `type: "incremental"`)**:
    *   `vanehay.1IAST_Fase2.silver_atualizacao_medicoes_desempenho`
*   **Transformações e Limpezas (Autocleaning & Optimization)**:
    *   **Batch**: CTEs unificadas para reuso de subconsultas de dicionários (`dicionario_uf`, `dicionario_municipio`, `dicionario_alunos`) e diretórios (`diretorio_sigla_uf`, `diretorio_id_municipio`). `TRIM` em chaves textuais e `SAFE_CAST` em métricas numéricas.
    *   **Streaming/Incremental**: Extração JSON com `JSON_VALUE`, normalização com `TRIM` e tipagem com `SAFE_CAST` das novas medições e metas contínuas, particionado por `DATE(publish_time)`.

## Estratégia de Implementação e Evolução
*   **Fase 1: Configuração do Repositório e Sincronização**
    *   Alinhamento de `workflow_settings.yaml` (`3.0.61`) e organização limpa do repositório no GitHub (`dev` e `main`).
*   **Fase 2: Segregação Arquitetural**
    *   Remoção dos modelos de metas do fluxo Batch e introdução do modelo incremental `silver_atualizacao_medicoes_desempenho` acoplado ao Pub/Sub.
*   **Fase 3: Verificação no Workspace GCP**
    *   Sincronização (`pull_git_commits`) no `dev-workspace` e compilação nativa para garantia de 0 erros no grafo de execução.

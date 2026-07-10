# Plano de Implementação - Pipeline Dataform: PIPE_1IAST_Fase2 (Camada Bronze Híbrida: Batch + Streaming Incremental)

## Objetivo
Estabelecer no Google Cloud Dataform no projeto GCP `vanehay` (dataset `1IAST_Fase2`) uma **Camada Bronze Híbrida de Ingestão de Dados (Batch + Streaming Incremental)**:
- **Bronze Batch (Histórico Consolidado)**: Materialização das três tabelas de avaliação e proficiência do INEP (`bronze_uf`, `bronze_municipio` e `bronze_alunos`), particionadas por `ano` escolar via `RANGE_BUCKET`.
- **Bronze Streaming Incremental (Atualizações em Tempo Real)**: Processamento contínuo das metas e revisões evolutivas através dos modelos incrementais `bronze_meta_alfabetizacao_brasil`, `bronze_meta_alfabetizacao_uf` e `bronze_meta_alfabetizacao_municipio`, consumindo em tempo real os eventos da tabela de aterrissagem `landing_eventos_indicadores` (alimentada diretamente pelo Cloud Pub/Sub).

## Premissas (Assumptions)
1. O repositório Dataform (`PIPE_1IAST_Fase2`) está configurado na região `US` na versão de Core `3.0.61`, compatível 100% com o console GCP.
2. Centralizar as cargas em lote e as atualizações contínuas de metas diretamente na **Camada Bronze** assegura que a ingestão bruta e limpa fique padronizada na entrada da arquitetura Medalhão.
3. Os modelos incrementais `bronze_meta_alfabetizacao_*` utilizam a cláusula condicional `when(incremental(), ...)` para varrer apenas novas mensagens filtradas por `publish_time`.

## Arquitetura do Pipeline
*   **Origens Batch Declaradas**:
    *   `basedosdados.br_inep_avaliacao_alfabetizacao.dicionario`
    *   `basedosdados.br_inep_avaliacao_alfabetizacao.uf`
    *   `basedosdados.br_inep_avaliacao_alfabetizacao.municipio`
    *   `basedosdados.br_inep_avaliacao_alfabetizacao.alunos`
    *   `basedosdados.br_bd_diretorios_brasil.uf`
    *   `basedosdados.br_bd_diretorios_brasil.municipio`
*   **Origem Streaming Declarada**:
    *   `vanehay.1IAST_Fase2.landing_eventos_indicadores` (Tabela Landing do Cloud Pub/Sub Direct Subscription)
*   **Destino Batch Bronze (`type: "table"`)**:
    *   `vanehay.1IAST_Fase2.bronze_uf`
    *   `vanehay.1IAST_Fase2.bronze_municipio`
    *   `vanehay.1IAST_Fase2.bronze_alunos`
*   **Destino Streaming Bronze Incremental (`type: "incremental"`)**:
    *   `vanehay.1IAST_Fase2.bronze_meta_alfabetizacao_brasil`
    *   `vanehay.1IAST_Fase2.bronze_meta_alfabetizacao_uf`
    *   `vanehay.1IAST_Fase2.bronze_meta_alfabetizacao_municipio`
*   **Transformações e Limpezas (Autocleaning & Optimization)**:
    *   **Batch**: CTEs unificadas (`dicionario_*`, `diretorio_*`), `TRIM` em chaves e `SAFE_CAST` em métricas numéricas.
    *   **Streaming**: Extração de payloads JSON com `JSON_VALUE`, normalização com `TRIM`, `SAFE_CAST` e cruzamento dimensional com os diretórios do IBGE em tempo real.

## Estratégia de Implementação e Validação
*   **Sincronização no Console (`dev-workspace`)**: Concluída via `pull_git_commits` com grafo de compilação 100% íntegro e sem erros de versão.

# Plano de Implementação - Pipeline Dataform: PIPE_1IAST_Fase2 (Arquitetura Medalhão: Bronze Híbrida + Prata Integrada)

## Objetivo
Estabelecer no Google Cloud Dataform no projeto GCP `vanehay` (dataset `1IAST_Fase2`) uma **Arquitetura Medalhão de Nível Corporativo (Bronze Híbrida + Prata Integrada)**:
- **Camada Bronze Híbrida (Batch + Streaming Incremental)**: 6 tabelas cobrindo todo o ecossistema do INEP (`bronze_uf`, `bronze_municipio` e `bronze_alunos` via carga batch histórica; `bronze_meta_alfabetizacao_brasil`, `bronze_meta_alfabetizacao_uf` e `bronze_meta_alfabetizacao_municipio` via ingestão streaming incremental do Pub/Sub).
- **Camada Prata Integrada (Silver Layer - Dados Tratados)**: 4 modelos analíticos padronizados (`silver_alfabetizacao_brasil`, `silver_alfabetizacao_uf`, `silver_alfabetizacao_municipio`, `silver_alunos_enriquecidos`) aplicando limpeza estrita, normalização de chaves IBGE em 7 dígitos (`LPAD`), tratamento de ausentes (`COALESCE`), integração cruzada de avaliações com metas e cálculo automatizado do desvio de meta.

## Premissas (Assumptions)
1. O repositório Dataform (`PIPE_1IAST_Fase2`) roda no Core `3.0.61` em total alinhamento com a nuvem na localização `US`.
2. Todas as 10 tabelas do pipeline (6 Bronze + 4 Prata) mantêm particionamento harmonioso por `ano` escolar via `RANGE_BUCKET(ano, GENERATE_ARRAY(2000, 2050, 1))`.
3. A camada Prata atua como a única fonte de verdade corporativa ("Single Source of Truth") pronta para consumo executivo e modelagem Ouro.

## Arquitetura do Pipeline
*   **Fontes Declaradas**: 6 fontes originais do INEP/IBGE + tabela streaming `landing_eventos_indicadores`.
*   **Camada Bronze (6 tabelas)**: `bronze_uf`, `bronze_municipio`, `bronze_alunos` (`table`), `bronze_meta_alfabetizacao_brasil`, `bronze_meta_alfabetizacao_uf`, `bronze_meta_alfabetizacao_municipio` (`incremental`).
*   **Camada Prata (4 tabelas integradas - `type: "table"`)**:
    *   `vanehay.1IAST_Fase2.silver_alfabetizacao_brasil` (Consolidação nacional e desvio de meta)
    *   `vanehay.1IAST_Fase2.silver_alfabetizacao_uf` (Integração relacional UF + Metas + Desvio)
    *   `vanehay.1IAST_Fase2.silver_alfabetizacao_municipio` (Integração Município + Metas IBGE 7 dígitos)
    *   `vanehay.1IAST_Fase2.silver_alunos_enriquecidos` (Alunos normalizados enriquecidos com meta do município)
*   **Diretrizes de Tratamento Aplicadas (Silver Layer)**:
    *   **Normalização de Chaves**: `LPAD(TRIM(id_municipio), 7, '0')` e `UPPER(TRIM(sigla_uf))`.
    *   **Limpeza de Dados**: `INITCAP(TRIM(rede))` e validações condicionais de notas de proficiência (`CASE WHEN proficiencia < 0 THEN NULL ...`).
    *   **Valores Ausentes**: `COALESCE(id_municipio_nome, 'Município Não Identificado')`, `COALESCE(presenca, 'Ausente / Sem Registro')`.
    *   **Integração das Bases**: `FULL OUTER JOIN` entre avaliações históricas e metas evolutivas em streaming.

## Estratégia de Implementação e Validação
*   **Sincronização (`dev-workspace`)**: Concluída via `pull_git_commits` com compilação de grafo completa interligando as fontes, as 6 tabelas Bronze e as 4 tabelas Prata.

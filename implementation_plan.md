# Plano de Implementação - Pipeline Dataform: PIPE_1IAST_Fase2 (Arquitetura Medalhão Completa: Bronze + Prata + Ouro)

## Objetivo
Estabelecer no Google Cloud Dataform no projeto GCP `vanehay` (dataset `1IAST_Fase2`) uma **Arquitetura Medalhão Completa de Nível Corporativo (Bronze + Prata + Ouro)**:
- **Camada Bronze Híbrida (Batch + Streaming Incremental)**: 6 tabelas cobrindo todo o ecossistema do INEP (`bronze_uf`, `bronze_municipio` e `bronze_alunos` em modo `table`; `bronze_meta_alfabetizacao_brasil`, `bronze_meta_alfabetizacao_uf` e `bronze_meta_alfabetizacao_municipio` em modo `incremental` consumindo em tempo real do Cloud Pub/Sub).
- **Camada Prata Integrada (Dados Tratados)**: 4 modelos analíticos (`silver_alfabetizacao_brasil`, `silver_alfabetizacao_uf`, `silver_alfabetizacao_municipio`, `silver_alunos_enriquecidos`) aplicando limpeza estrita, normalização de chaves (`LPAD`, `UPPER`), tratamento de nulos (`COALESCE`) e cruzamento relacional entre avaliações históricas e metas evolutivas.
- **Camada Ouro Analítica (Produtos de Dados Prontos)**: 4 modelos analíticos especializados (`gold_indicadores_municipais`, `gold_comparativo_metas_resultados`, `gold_evolucao_temporal_indicadores`, `gold_dataset_ml_proficiencia_alunos`) customizados para **Dashboards BI**, **Análises Estatísticas Longitudinais (Séries Temporais)** e **Treinamento de Modelos de Machine Learning (Regressão e Classificação)**.

## Premissas (Assumptions)
1. O repositório Dataform (`PIPE_1IAST_Fase2`) roda no Core `3.0.61` em total alinhamento com a nuvem na localização `US`.
2. Todas as 14 tabelas do pipeline (6 Bronze + 4 Prata + 4 Ouro) mantêm particionamento harmonioso e de altíssimo desempenho por `ano` escolar via `RANGE_BUCKET(ano, GENERATE_ARRAY(2000, 2050, 1))`.
3. A camada Ouro entrega modelos analíticos finais com KPIs calculados, funções de janela (`LAG`, `AVG OVER ROWS PRECEDING`) e *feature engineering* purificado para modelos analíticos e inteligência artificial.

## Arquitetura do Pipeline
*   **7 Fontes Declaradas**: 6 fontes da Base dos Dados + tabela streaming `landing_eventos_indicadores`.
*   **6 Tabelas Bronze**: `bronze_uf`, `bronze_municipio`, `bronze_alunos` + 3 tabelas incrementais `bronze_meta_alfabetizacao_*`.
*   **4 Tabelas Prata**: `silver_alfabetizacao_brasil`, `silver_alfabetizacao_uf`, `silver_alfabetizacao_municipio`, `silver_alunos_enriquecidos`.
*   **4 Tabelas Ouro (Produtos Analíticos Finalizados - `type: "table"`)**:
    *   `vanehay.1IAST_Fase2.gold_indicadores_municipais` (Foco: Dashboards BI & Status de Atingimento de Meta)
    *   `vanehay.1IAST_Fase2.gold_comparativo_metas_resultados` (Foco: Governança multi-nível Brasil vs UF vs Município)
    *   `vanehay.1IAST_Fase2.gold_evolucao_temporal_indicadores` (Foco: Análise Estatística Longitudinal & Variação Anual)
    *   `vanehay.1IAST_Fase2.gold_dataset_ml_proficiencia_alunos` (Foco: Feature Engineering e Treino de Machine Learning)

## Estratégia de Implementação e Validação
*   **Sincronização (`dev-workspace`)**: Concluída via `pull_git_commits` com compilação de grafo completa integrando os 21 nós (7 fontes + 14 modelos).

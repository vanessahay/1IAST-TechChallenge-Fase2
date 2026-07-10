# Plano de Implementação - Pipeline Dataform: PIPE_1IAST_Fase2 (Arquitetura Medalhão + Suite de Qualidade de Dados)

## Objetivo
Estabelecer no Google Cloud Dataform no projeto GCP `vanehay` (dataset `1IAST_Fase2`) uma **Arquitetura Medalhão Completa com Suite Robusta de Qualidade de Dados**:
- **Camada Bronze Híbrida (Batch + Streaming Incremental)**: 6 tabelas (`bronze_uf`, `bronze_municipio`, `bronze_alunos`, `bronze_meta_alfabetizacao_brasil`, `bronze_meta_alfabetizacao_uf`, `bronze_meta_alfabetizacao_municipio`).
- **Camada Prata Integrada**: 4 modelos (`silver_alfabetizacao_brasil`, `silver_alfabetizacao_uf`, `silver_alfabetizacao_municipio`, `silver_alunos_enriquecidos`) com limpeza e normalização estrita (`LPAD`, `INITCAP`, `COALESCE`).
- **Camada Ouro Analítica**: 4 produtos analíticos finais (`gold_indicadores_municipais`, `gold_comparativo_metas_resultados`, `gold_evolucao_temporal_indicadores`, `gold_dataset_ml_proficiencia_alunos`).
- **Suite de Regras de Qualidade de Dados (`type: "assertion"`)**: 4 testes automatizados e integrados ao fluxo (`assert_duplicidade_silver_municipio`, `assert_valores_ausentes_gold_kpis`, `assert_fk_relacionamento_municipios`, `assert_consistencia_macro_brasil_vs_uf`), cobrindo duplicidade, ausência de nulos, integridade relacional com IBGE e consistência macro entre tabelas.

## Premissas (Assumptions)
1. O repositório Dataform (`PIPE_1IAST_Fase2`) roda no Core `3.0.61` sincronizado perfeitamente com a nuvem.
2. As asserções customizadas retornam os registros violadores; quando a consulta retorna 0 linhas, o teste no Dataform é aprovado com sucesso.

## Arquitetura e Componentes do Grafo
*   **7 Fontes Declaradas**: `dicionario`, `uf`, `municipio`, `alunos`, diretórios IBGE + `landing_eventos_indicadores`.
*   **14 Tabelas de Transformação**: 6 Bronze (`table` / `incremental`), 4 Prata (`table`), 4 Ouro (`table`).
*   **4 Asserções de Qualidade (`type: "assertion"`)**:
    *   `definitions/assertions/assert_duplicidade_silver_municipio.sqlx` (Duplicidade)
    *   `definitions/assertions/assert_valores_ausentes_gold_kpis.sqlx` (Nulos / Ausentes)
    *   `definitions/assertions/assert_fk_relacionamento_municipios.sqlx` (Chaves Foreign Key com IBGE)
    *   `definitions/assertions/assert_consistencia_macro_brasil_vs_uf.sqlx` (Consistência entre Tabelas)

## Estratégia de Implementação e Validação
*   **Sincronização (`dev-workspace`)**: Concluída via `pull_git_commits` com compilação de grafo completa integrando todos os 25 nós (7 fontes + 14 tabelas + 4 asserções).

# Walkthrough - Pipeline Dataform: PIPE_1IAST_Fase2 (Arquitetura Medalhão + Suite de Qualidade de Dados)

Este documento exibe a documentação corporativa integral do pipeline `PIPE_1IAST_Fase2` no **Google Cloud Dataform**, apresentando nossa **Arquitetura Medalhão Completa (Bronze + Prata + Ouro)** enriquecida com a **Suite de Regras de Qualidade de Dados (Data Quality Assertions)**, construída em conformidade com os skills `@skill:dataform-bigquery`, `@skill:data-autocleaning`, `@skill:developing-with-bigquery` e `@skill:ml-best-practices`.

## 1. Estrutura da Arquitetura Medalhão no Dataform
O projeto conecta de ponta a ponta as origens, transformações analíticas e testes automatizados de governança no Google Cloud (`us-central1`, Core `3.0.61`):
*   **7 Fontes Declaradas (`definitions/sources/*.sqlx`)**: 6 origens históricas/diretórios da Base dos Dados + tabela streaming `landing_eventos_indicadores`.
*   **6 Tabelas Bronze (`definitions/bronze_*.sqlx`)**: 3 Batch (`bronze_uf`, `bronze_municipio`, `bronze_alunos`) + 3 Incrementais de streaming (`bronze_meta_alfabetizacao_*`).
*   **4 Tabelas Prata (`definitions/silver_*.sqlx`)**: `silver_alfabetizacao_brasil`, `silver_alfabetizacao_uf`, `silver_alfabetizacao_municipio` e `silver_alunos_enriquecidos`.
*   **4 Tabelas Ouro (`definitions/gold_*.sqlx`)**: `gold_indicadores_municipais` (Dashboards BI), `gold_comparativo_metas_resultados` (Governança Multi-Nível), `gold_evolucao_temporal_indicadores` (Estatística Longitudinal) e `gold_dataset_ml_proficiencia_alunos` (Treino de Machine Learning).
*   **4 Asserções de Qualidade (`definitions/assertions/*.sqlx`)**: Testes de certificação de dados descritos no sumário abaixo.

## 2. Sumário das Regras e Asserções de Qualidade de Dados (`type: "assertion"`)

| Pilar de Qualidade Exigido | Modelo de Asserção (`.sqlx`) | Alvo da Validação | Mecanismo e Lógica SQL Aplicada | Ação / Comportamento no Pipeline |
| :--- | :--- | :--- | :--- | :--- |
| **1. Verificação de Duplicidade** | `assert_duplicidade_silver_municipio` | `silver_alfabetizacao_municipio` | Agrupa pelos campos chave (`ano`, `id_municipio`, `rede`) checando se `HAVING COUNT(*) > 1`. | Garante que nenhuma combinação dimensional se duplique, protegendo somas e agregações em relatórios BI. |
| **2. Detecção de Valores Ausentes** | `assert_valores_ausentes_gold_kpis` | `gold_indicadores_municipais` | Vare a tabela executiva verificando se chaves ou o KPI `status_atingimento_meta` são nulos (`IS NULL`). | Certifica que o produto Ouro entregue ao usuário final possui 100% de preenchimento nos campos executivos mandatórios. |
| **3. Validação de Chaves de Relacionamento** | `assert_fk_relacionamento_municipios` | `silver_alfabetizacao_municipio` + `br_bd_diretorios_brasil.municipio` | Roda um `LEFT JOIN` com o cadastro nacional de municípios do IBGE (`LPAD(TRIM(...), 7, '0')`) e retorna códigos sem par no IBGE (`IS NULL`). | Valida a integridade referencial (*Foreign Key*) garantindo que todas as cidades avaliadas existem oficialmente no censo. |
| **4. Consistência Entre Tabelas** | `assert_consistencia_macro_brasil_vs_uf` | `silver_alfabetizacao_brasil` + `silver_alfabetizacao_uf` | Compara a taxa nacional consolidada (`silver_*_brasil`) com a média agregada dos estados (`silver_*_uf`) para checar desvios atípicos (`> 25 p.p.`). | Garante a coerência macroeconômica e analítica cruzada entre as visões nacionais e estaduais do pipeline. |

## 3. Sumário de Limpeza e Otimização SQL (Autocleaning & Optimization)

*   **Autocleaning**: Normalização de 7 dígitos IBGE com `LPAD`, padronização de textos em `INITCAP`, remoção de quebras por `TRIM` e resiliência a nulos via `COALESCE(...)`.
*   **Otimização**: Particionamento por `ano` via `RANGE_BUCKET(ano, GENERATE_ARRAY(2000, 2050, 1))` em todas as tabelas, reuso de subconsultas (CTEs) e processamento condicional incremental.

## 4. Validação e Sincronização na Nuvem

*   **Sincronização no Console (`dev-workspace`)**: Concluída refletindo todos os 25 nós interligados.
*   **Verificação de Compilação**: Grafo do pipeline compilado na nuvem com **sucesso e 0 erros**, unindo transformações analíticas e testes automáticos de governança em um único fluxo corporativo.

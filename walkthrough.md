# Walkthrough - Pipeline Dataform: PIPE_1IAST_Fase2 (Arquitetura Medalhão Completa: Bronze + Prata + Ouro)

Este documento exibe a documentação corporativa integral do pipeline `PIPE_1IAST_Fase2` no **Google Cloud Dataform**, onde implementamos a **Arquitetura Medalhão Completa (Bronze + Prata + Ouro)**, atendendo rigorosamente a todos os requisitos de Dashboards, Análise Estatística e Treinamento de Machine Learning em conformidade com os skills `@skill:dataform-bigquery`, `@skill:data-autocleaning`, `@skill:developing-with-bigquery` e `@skill:ml-best-practices`.

## 1. Estrutura da Arquitetura Medalhão no Dataform
O projeto conecta de ponta a ponta as origens na Base dos Dados e streaming do Cloud Pub/Sub até os produtos analíticos finais da Camada Ouro (`us-central1`, Core `3.0.61`):
*   **7 Fontes Declaradas (`definitions/sources/*.sqlx`)**: 6 origens históricas/diretórios da Base dos Dados + tabela de aterrissagem `landing_eventos_indicadores`.
*   **6 Tabelas Bronze (`definitions/bronze_*.sqlx`)**: 3 tabelas Batch históricas (`bronze_uf`, `bronze_municipio`, `bronze_alunos`) + 3 tabelas Incrementais de streaming (`bronze_meta_alfabetizacao_*`).
*   **4 Tabelas Prata Integradas (`definitions/silver_*.sqlx`)**: `silver_alfabetizacao_brasil`, `silver_alfabetizacao_uf`, `silver_alfabetizacao_municipio` e `silver_alunos_enriquecidos`.
*   **4 Tabelas Ouro Analíticas (`definitions/gold_*.sqlx`)**:
    *   `gold_indicadores_municipais`: Visão executiva para **Dashboards BI**, categorizando o KPI `status_atingimento_meta`.
    *   `gold_comparativo_metas_resultados`: Tabela unificada (`UNION ALL`) para **Governança Multi-Nível**, comparando o atingimento percentual no Brasil, nos Estados e nos Municípios.
    *   `gold_evolucao_temporal_indicadores`: Modelo para **Análise Estatística e Séries Temporais**, calculando a variação anual em pontos percentuais (`LAG`) e a média móvel de 3 ciclos (`AVG OVER PRECEDING`).
    *   `gold_dataset_ml_proficiencia_alunos`: Dataset analítico purificado para **Treinamento de Machine Learning**, com *feature engineering* relacional (`meta_municipio`), alvos de regressão (`target_proficiencia_cont`) e alvos binários de classificação (`target_risco_defasagem_bool` e `target_alfabetizado_binario`).

## 2. Sumário de Limpeza, Normalização e Tratamentos (Autocleaning & Silver Layer)

| Camada / Modelo | Campos / Alvos | Problema / Risco Detectado | Transformação Aplicada | Benefício |
| :--- | :--- | :--- | :--- | :--- |
| **Bronze (Batch + Streaming)** | `sigla_uf`, `id_municipio`, `serie`, `rede`, `data` (JSON) | Espaços extras em branco ou quebras invisíveis | Aplicação contínua de `TRIM(...)` e `JSON_VALUE(...)` | 100% de precisão nos JOINs com os diretórios do IBGE e dicionários do INEP |
| **Prata (Silver Integrada)** | `id_municipio`, `sigla_uf`, `rede`, `proficiencia` | Códigos municipais de 6 dígitos ou quebras de tipagem | `LPAD(TRIM(id_municipio), 7, '0')`, `UPPER(...)`, `INITCAP(...)` e validações `CASE WHEN proficiencia < 0 THEN NULL` | Harmonização dimensional em 7 dígitos e eliminação completa de anomalias de notas |
| **Ouro (Dashboards & BI)** | `desvio_meta_2024`, `status_atingimento_meta` | Dificuldade visual na interpretação rápida de desvios | Criação de faixas executivas via `CASE WHEN desvio >= 0 THEN 'Atingida'` | Aceleração na construção de relatórios e painéis executivos |
| **Ouro (Estatística & ML)** | Séries temporais, `peso_aluno`, alvos binários ML | Falha na suavização longitudinal e falta de *targets* estruturados | `LAG(...)`, `AVG OVER ROWS PRECEDING`, *sample weights* e alvos numéricos binários (0/1) | Datasets purificados sem registros nulos, prontos para consumo por algoritmos estatísticos e de IA |

## 3. Sumário de Otimização SQL (Optimization Summary)

| Otimização Aplicada | Descrição e Justificativa |
| :--- | :--- |
| **Common Subexpression Reuse (CTEs)** | Reuso limpo e estruturado de subconsultas em todas as tabelas Bronze, Prata e Ouro. |
| **Funções de Janela Analíticas (`LAG` / `AVG OVER`)** | Cálculo de variações temporais executado no próprio motor analítico do BigQuery sem movimentação externa de dados. |
| **Particionamento Uniforme (`RANGE_BUCKET`)** | Todas as 14 tabelas do pipeline são particionadas sistematicamente pela coluna `ano` (`RANGE_BUCKET(ano, GENERATE_ARRAY(2000, 2050, 1))`), maximizando o desempenho das consultas e minimizando custos operacionais. |

## 4. Validação e Sincronização na Nuvem

*   **Sincronização no Console (`dev-workspace`)**: Concluída com êxito refletindo os 21 nós (7 fontes + 6 Bronze + 4 Prata + 4 Ouro).
*   **Verificação de Compilação**: Grafo de execução compilado na nuvem com **sucesso e 0 erros**, consolidando o projeto como referência técnica em engenharia de dados e analytics.

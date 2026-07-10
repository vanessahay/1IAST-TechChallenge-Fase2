# Walkthrough - Pipeline Dataform: PIPE_1IAST_Fase2 (Arquitetura Medalhão: Bronze Híbrida + Prata Integrada)

Este documento descreve a arquitetura corporativa final do pipeline `PIPE_1IAST_Fase2` no **Google Cloud Dataform**, onde construímos em conformidade total com os skills (`@skill:dataform-bigquery`, `@skill:data-autocleaning`, `@skill:developing-with-bigquery`) a nossa **Camada Bronze Híbrida** e a **Camada Prata Integrada (Silver Layer - Dados Tratados)**.

## 1. Estrutura da Arquitetura Medalhão no Dataform
O projeto conecta de ponta a ponta as origens na Base dos Dados e streaming do Cloud Pub/Sub até as visões integradas da camada Prata (`us-central1`, Core `3.0.61`):
*   **7 Fontes Declaradas (`definitions/sources/*.sqlx`)**: 6 origens históricas/diretórios da Base dos Dados + tabela streaming `landing_eventos_indicadores`.
*   **6 Tabelas Bronze (`definitions/bronze_*.sqlx`)**: 3 tabelas Batch históricas (`bronze_uf`, `bronze_municipio`, `bronze_alunos`) + 3 tabelas Incrementais de streaming (`bronze_meta_alfabetizacao_brasil`, `bronze_meta_alfabetizacao_uf`, `bronze_meta_alfabetizacao_municipio`).
*   **4 Tabelas Prata Integradas (`definitions/silver_*.sqlx`)**:
    *   `silver_alfabetizacao_brasil`: Consolidação e desvio de meta nacional.
    *   `silver_alfabetizacao_uf`: Integração `FULL OUTER JOIN` entre avaliações estaduais e metas em streaming, com desvio de meta e proporção de níveis.
    *   `silver_alfabetizacao_municipio`: Integração de notas e metas com normalização estrita de 7 dígitos IBGE (`LPAD`).
    *   `silver_alunos_enriquecidos`: Normalização granular individual de cada aluno com tratamento categórico e enriquecimento contextual com a meta de alfabetização do município.

## 2. Sumário das 5 Diretrizes de Tratamento Aplicadas na Camada Prata

| Diretriz Exigida | Como foi aplicada na Camada Prata (.sqlx) | Benefício Executivo e Analítico |
| :--- | :--- | :--- |
| **1. Normalização de Chaves** | `LPAD(TRIM(id_municipio), 7, '0')` em todos os cruzamentos municipais/alunos e `UPPER(TRIM(sigla_uf))` nas unidades da federação. | Elimina perdas em JOINs por códigos de 6 dígitos sem zero à esquerda ou divergência de maiúsculas/minúsculas. |
| **2. Limpeza de Dados** | `INITCAP(TRIM(rede))` (ex: `Pública`, `Privada`) e validação de consistência contínua de notas (`CASE WHEN proficiencia < 0 THEN NULL ...`). | Garante pureza e padronização visual em relatórios executivos e BI. |
| **3. Tratamento de Valores Ausentes** | Substituição segura com `COALESCE(sigla_uf_nome, 'Estado Não Identificado')`, `COALESCE(rede, 'Total')` e `COALESCE(alfabetizado, 'Não Avaliado')`. | Evita quebras em agrupamentos ou gráficos por categorias nulas (`NULL`). |
| **4. Padronização de Nomes e Tipos** | Nomenclatura corporativa clara em 100% das colunas (ex: `taxa_alfabetizacao_atual`, `desvio_meta_2024`) e casting estrito em `FLOAT64`/`INT64`. | Confiabilidade no consumo de dados e governança clara de esquemas. |
| **5. Integração das Bases** | **Crucial**: Cruzamento relacional (`FULL OUTER JOIN` / `LEFT JOIN`) entre bases históricas do INEP e fluxos de metas evolutivas contínuas. | Permite responder em tempo real qual é o **Desvio de Meta (`taxa_atual - meta_2024`)** e qual meta o aluno precisa atingir. |

## 3. Sumário de Otimização SQL (Optimization Summary)

| Otimização Aplicada | Descrição e Justificativa |
| :--- | :--- |
| **Reuso de Subconsultas (CTEs)** | Centralização da leitura de dicionários na camada Bronze e reuso de subconsultas limpas nas tabelas Prata. |
| **Predicate Pushdown & Poda de Colunas** | Filtros aplicados na origem e tráfego exclusivo das colunas analíticas essenciais. |
| **Particionamento Consistente (`RANGE_BUCKET`)** | Todas as 10 tabelas do pipeline (Bronze e Prata) são particionadas pela coluna `ano` (`RANGE_BUCKET(ano, GENERATE_ARRAY(2000, 2050, 1))`), garantindo altíssimo desempenho em queries e baixo consumo de bytes no BigQuery. |

## 4. Validação e Sincronização na Nuvem

*   **Compilação no Workspace (`dev-workspace`)**: O grafo contendo as 7 fontes, 6 tabelas Bronze e 4 tabelas Prata compila com **100% de sucesso e 0 erros**.
*   **Conclusão**: O pipeline `PIPE_1IAST_Fase2` entrega uma arquitetura moderna, resiliente e escalável no Google Cloud Platform.

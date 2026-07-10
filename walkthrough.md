# Walkthrough - Pipeline Dataform: PIPE_1IAST_Fase2 (Camada Bronze Híbrida: Batch + Streaming Incremental)

Este documento documenta a arquitetura técnica final do pipeline `PIPE_1IAST_Fase2` no **Google Cloud Dataform**, onde a **Camada Bronze** é responsável por integrar em harmonia o histórico consolidado de avaliação (ELT Batch) e a ingestão contínua de metas e resultados do INEP em tempo real (ELT Streaming Incremental), seguindo as diretrizes dos skills `@skill:dataform-bigquery`, `@skill:data-autocleaning` e `@skill:developing-with-bigquery`.

## 1. Estrutura da Camada Bronze Híbrida
O projeto está alinhado entre o GitHub (`dev` e `main`) e o repositório `PIPE_1IAST_Fase2` no console do Google Cloud Dataform (`us-central1`, Core `3.0.61`):
*   **Fontes Batch (`definitions/sources/br_inep_*.sqlx`)**: Dicionários e tabelas históricas do INEP (`dicionario`, `uf`, `municipio`, `alunos`) e diretórios do IBGE (`uf`, `municipio`).
*   **Fonte Streaming (`definitions/sources/vanehay_landing_eventos_indicadores.sqlx`)**: Tabela de aterrissagem (`landing_eventos_indicadores`) alimentada automaticamente via *Pub/Sub Direct Subscription*.
*   **Tabelas Bronze Batch (`definitions/bronze_uf.sqlx`, `bronze_municipio.sqlx`, `bronze_alunos.sqlx`)**: Materializadas em modo `table` e particionadas por `ano` (`RANGE_BUCKET`), reunindo os indicadores estaduais, municipais e individuais históricos.
*   **Tabelas Bronze Streaming Incrementais (`definitions/bronze_meta_alfabetizacao_*.sqlx`)**: Tabelas `bronze_meta_alfabetizacao_brasil`, `bronze_meta_alfabetizacao_uf` e `bronze_meta_alfabetizacao_municipio`, materializadas em modo **`incremental`** (`RANGE_BUCKET(ano, ...)`), processando contínuamente os eventos que aterrissam na tabela de landing.

## 2. Sumário de Limpeza Automática (Autocleaning Summary)

| Camada / Modelo | Campos / Alvos | Problema / Risco Detectado | Transformação Aplicada | Benefício |
| :--- | :--- | :--- | :--- | :--- |
| **Bronze Batch** (`bronze_uf`, `bronze_municipio`, `bronze_alunos`) | `sigla_uf`, `id_municipio`, `id_escola`, `id_aluno`, `serie`, `rede`, `presenca` | Espaços extras em branco ou quebras de linha em bases externas | Aplicação contínua de `TRIM(...)` nas chaves dimensionais e de junção | 100% de precisão nos JOINs com os dicionários do INEP e diretórios do IBGE |
| **Bronze Batch** (`bronze_uf`, `bronze_municipio`, `bronze_alunos`) | `ano`, `taxa_alfabetizacao`, `media_portugues`, `proficiencia`, `peso_aluno` | Falhas de conversão numérica em dados externos brutos (`Bad float/int`) | `SAFE_CAST(coluna AS FLOAT64)` e `SAFE_CAST(ano AS INT64)` | Resiliência total na carga; valores anômalos convertidos em NULL com segurança |
| **Bronze Streaming Incremental** (`bronze_meta_alfabetizacao_*`) | `data` (payload JSON), `publish_time`, `message_id` | Payloads JSON recebidos via Pub/Sub necessitam de parsing seguro e tipagem estruturada | `JSON_VALUE(data, '$.prop')` com `TRIM(...)` para strings e `SAFE_CAST(...)` para numéricos/inteiros | Harmonização instantânea e serverless das metas e taxas em streaming diretamente na Camada Bronze |

## 3. Sumário de Otimização SQL (Optimization Summary)

| Otimização Aplicada | Descrição e Justificativa |
| :--- | :--- |
| **Common Subexpression Reuse (Reuso de Subconsulta)** | Criação de CTEs unificadas nos modelos batch (`dicionario_uf`, `dicionario_municipio`, `dicionario_alunos`, `diretorio_sigla_uf`, `diretorio_id_municipio`) e no streaming (`diretorio_sigla_uf`, `diretorio_id_municipio`) para varreduras limpas. |
| **Predicate Pushdown & Poda de Colunas** | Filtros de `id_tabela` aplicados logo na leitura inicial e eliminação de colunas intermediárias redundantes. |
| **Particionamento Consistente (`RANGE_BUCKET`)** | Todas as 6 tabelas da camada Bronze são particionadas uniformemente pela coluna inteira `ano` via `RANGE_BUCKET(ano, GENERATE_ARRAY(2000, 2050, 1))`. |
| **Processamento Incremental Condicional** | As 3 tabelas de metas processam unicamente eventos com `publish_time > (SELECT MAX(publish_time) FROM ${self()})`, reduzindo drasticamente custos computacionais. |

## 4. Validação e Sincronização do Console

*   **Sincronização do Workspace GCP (`dev-workspace`)**: Concluída via `pull_git_commits` refletindo as 6 tabelas e 0 erros de versionamento (`Core 3.0.61`).
*   **Verificação de Compilação**: Grafo do pipeline compilado na nuvem com **sucesso absoluto**, ilustrando com precisão a convivência harmoniosa do fluxo Batch Histórico e da Ingestão Streaming Incremental na Camada Bronze.

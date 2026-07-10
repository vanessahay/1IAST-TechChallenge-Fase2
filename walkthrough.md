# Walkthrough - Pipeline Dataform: PIPE_1IAST_Fase2 (Arquitetura Híbrida: Batch + Streaming Incremental)

Este documento apresenta a documentação completa da implementação técnica do pipeline `PIPE_1IAST_Fase2` no **Google Cloud Dataform**, segregado em **Camada Bronze Batch** (histórico consolidado) e **Camada Prata Incremental** (ingestão streaming em tempo real), seguindo rigorosamente os skills `@skill:dataform-bigquery`, `@skill:data-autocleaning` e `@skill:developing-with-bigquery`.

## 1. Estrutura e Segregação Arquitetural
O projeto está sincronizado entre o GitHub (`dev` e `main`) e o repositório `PIPE_1IAST_Fase2` no console do Google Cloud Dataform (`us-central1`, Core `3.0.61`):
*   **Declarações de Fontes Batch (`definitions/sources/*.sqlx`)**: Apontam para os dicionários e tabelas históricas do INEP (`dicionario`, `uf`, `municipio`, `alunos`) e diretórios do IBGE (`uf`, `municipio`).
*   **Declaração de Fonte Streaming (`definitions/sources/vanehay_landing_eventos_indicadores.sqlx`)**: Aponta para a tabela de aterrissagem (`landing_eventos_indicadores`) alimentada diretamente pelo tópico do Cloud Pub/Sub.
*   **Modelos Batch Históricos (`definitions/bronze_*.sqlx`)**: Tabelas `bronze_uf`, `bronze_municipio` e `bronze_alunos`, materializadas em modo `table` e particionadas por `ano` escolar (`RANGE_BUCKET`).
*   **Modelo Streaming Incremental (`definitions/silver_atualizacao_medicoes_desempenho.sqlx`)**: Tabela Prata (`silver_atualizacao_medicoes_desempenho`) materializada em modo `incremental` e particionada por `DATE(publish_time)`, processando em tempo real novas medições de desempenho, atualização de indicadores e revisão de metas.

## 2. Sumário de Limpeza Automática (Autocleaning Summary)

| Camada / Modelo | Campos / Alvos | Problema / Risco Detectado | Transformação Aplicada | Benefício |
| :--- | :--- | :--- | :--- | :--- |
| **Batch Bronze** (`bronze_uf`, `bronze_municipio`, `bronze_alunos`) | `sigla_uf`, `id_municipio`, `id_escola`, `id_aluno`, `serie`, `rede`, `presenca` | Espaços em branco e quebras invisíveis podem corromper JOINs e agregações | Aplicação sistêmica de `TRIM(...)` nas chaves dimensionais de junção e dimensionamento | 100% de precisão nos cruzamentos com diretórios IBGE e dicionários INEP |
| **Batch Bronze** (`bronze_uf`, `bronze_municipio`, `bronze_alunos`) | `ano`, `taxa_alfabetizacao`, `media_portugues`, `proficiencia`, `peso_aluno` | Falhas de conversão de tipagem em dados externos brutos (`Bad float/int`) | `SAFE_CAST(coluna AS FLOAT64)` e `SAFE_CAST(ano AS INT64)` | Resiliência total na carga; valores inválidos convertidos para NULL sem quebrar o pipeline |
| **Streaming Prata** (`silver_atualizacao_medicoes_desempenho`) | `data` (payload JSON), `publish_time`, `message_id` | Payloads JSON recebidos via Pub/Sub precisam de extração limpa e tipagem estruturada | `JSON_VALUE(data, '$.prop')` combinado com `TRIM(...)` e `SAFE_CAST(...)` para numéricos | Normalização contínua de eventos sem necessidade de servidores intermediários |

## 3. Sumário de Otimização SQL (Optimization Summary)

| Otimização Aplicada | Descrição e Justificativa |
| :--- | :--- |
| **Common Subexpression Reuse (Reuso de Subconsulta)** | Criação de CTEs unificadas em todos os modelos batch (`dicionario_uf`, `dicionario_municipio`, `dicionario_alunos`, `diretorio_sigla_uf`, `diretorio_id_municipio`) para extração única de dicionários sem leituras redundantes. |
| **Predicate Pushdown & Column Pruning** | Filtros de `id_tabela` (`'uf'`, `'municipio'`, `'alunos'`) aplicados na leitura inicial da CTE e eliminação de colunas desnecessárias. |
| **Particionamento Estratégico** | `RANGE_BUCKET(ano, ...)` nas tabelas históricas batch e `DATE(publish_time)` na tabela de atualização streaming incremental. |
| **Processamento Condicional (`when(incremental(), ...)`)** | A tabela incremental processa apenas eventos novos com `publish_time > MAX(publish_time)`, economizando custos e tempo de varredura no BigQuery. |

## 4. Quality Review & Validação do Workspace

*   **Sincronia do Workspace GCP (`dev-workspace`)**: Concluída via `pull_git_commits` com alinhamento perfeito de versão (`3.0.61`).
*   **Verificação de Compilação (`create_compilation_result`)**: Grafo gerado na nuvem com **sucesso e 0 erros**, refletindo com clareza os nós históricos (Bronze) e o fluxo contínuo de streaming (Prata Incremental).
*   **Conclusão**: O pipeline `PIPE_1IAST_Fase2` está estruturado no estado da arte da engenharia de dados no Google Cloud Platform.

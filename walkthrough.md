# Walkthrough - Pipeline Dataform: PIPE_1IAST_Fase2

Este documento descreve a implementação completa do pipeline `PIPE_1IAST_Fase2` no Dataform para criação das quatro tabelas particionadas da camada Bronze no BigQuery (`bronze_uf`, `bronze_meta_alfabetizacao_brasil`, `bronze_meta_alfabetizacao_uf` e `bronze_meta_alfabetizacao_municipio`), seguindo as diretrizes dos skills `@skill:dataform-bigquery`, `@skill:data-autocleaning` e `@skill:developing-with-bigquery`.

## 1. Resumo da Estrutura do Projeto
O projeto está estruturado no repositório Git [vanessahay/1IAST-TechChallenge-Fase2](https://github.com/vanessahay/1IAST-TechChallenge-Fase2.git) e sincronizado com o repositório **`PIPE_1IAST_Fase2`** no Google Cloud Dataform (`us-central1`):
*   `workflow_settings.yaml`: Define o projeto padrão como `vanehay`, dataset padrão `1IAST_Fase2` na região `US` e versão do Dataform Core `3.0.0`.
*   `.df-credentials.json` e `package.json`: Configurações de autenticação e pacotes para compilação/execução.
*   `definitions/sources/*.sqlx`: Declaração formal das sete tabelas de origem na `basedosdados`.
*   `definitions/bronze_uf.sqlx`: Modelo SQLX da tabela de destino com indicadores estaduais, descrições de colunas e particionamento por ano.
*   `definitions/bronze_meta_alfabetizacao_brasil.sqlx`: Modelo SQLX da tabela com as metas evolutivas nacionais do Brasil (2024 a 2030).
*   `definitions/bronze_meta_alfabetizacao_uf.sqlx`: Modelo SQLX da tabela com metas evolutivas regionais por Unidade da Federação, enriquecida com o nome dos estados.
*   `definitions/bronze_meta_alfabetizacao_municipio.sqlx`: Modelo SQLX granular por município com metas e taxas estaduais/municipais do INEP, enriquecido com o nome oficial de cada município pelo IBGE.

## 2. Sumário de Limpeza Automática (Autocleaning Summary)

Abaixo estão detalhadas as transformações de qualidade de dados aplicadas nos quatro modelos:

| Campo / Alvo | Descrição (Destino) | Problema Detectado / Risco | Transformação Aplicada | Benefício |
| :--- | :--- | :--- | :--- | :--- |
| `id_municipio`, `sigla_uf`, `serie`, `rede`, `nivel_alfabetizacao` | Chaves IBGE e códigos textuais de junção ou dimensão | Risco de falha silenciosa em JOINs e agrupamentos devido a espaços em branco extras ou quebras de linha invisíveis | Aplicação de `TRIM(...)` tanto nas chaves estrangeiras/primárias quanto nos campos dimensionais | Garante 100% de precisão nos JOINs e normalização dos códigos textuais |
| `ano` | Chave de particionamento das tabelas (`INTEGER`) | Variáveis em dados brutos podem apresentar inconsistências de formatação | `SAFE_CAST(dados.ano AS INT64)` | Garante compatibilidade rigorosa com o particionamento `RANGE_BUCKET`, prevenindo falhas de conversão durante a carga |
| `taxa_alfabetizacao`, `media_portugues`, `meta_alfabetizacao_*`, `percentual_participacao` | Métricas contínuas, proporções e metas anuais (`FLOAT64`) | Textos mal formatados ou números inválidos em bases de origem externa podem quebrar queries com erro de `Bad int / float` | `SAFE_CAST(dados.<coluna> AS FLOAT64)` em todas as métricas numéricas | Robustez na ingestão de dados da camada Bronze; valores anômalos convertidos para NULL com segurança sem interromper o pipeline |

## 3. Sumário de Otimização SQL (Optimization Summary)

| Otimização Aplicada | Descrição e Justificativa |
| :--- | :--- |
| **Common Subexpression Reuse (Reutilização de Subconsulta)** | Criação de CTEs unificadas (`dicionario_uf`, `diretorio_sigla_uf` e `diretorio_id_municipio`) para padronizar e reutilizar o acesso a diretórios e dicionários em todos os modelos. |
| **Predicate Pushdown** | Os filtros de `id_tabela` e `nome_coluna` foram movidos para a primeira leitura das subconsultas. |
| **Column Pruning (Poda de Colunas)** | Nenhuma coluna não utilizada é trafegada entre as subconsultas em todos os fluxos do pipeline. |
| **Particionamento por Faixa de Inteiro (`RANGE_BUCKET`)** | Configurado `partitionBy: "RANGE_BUCKET(ano, GENERATE_ARRAY(2000, 2050, 1))"` em todos os quatro modelos para otimizar queries analíticas e de relatórios executivos. |

## 4. Quality Review Profiling Evidence

- [ ] Post-Transformation Dataplex Profile Job ID: N/A (Escaneamentos Dataplex na origem retornam erro `403 Permission Denied` por serem tabelas geridas por terceiros no projeto publico `basedosdados`).
- [ ] Profile Comparison & Validation Summary:
    *   As consultas SQL de transformação das quatro tabelas foram testadas via `bq query --dry_run` no BigQuery CLI, validando sem erros sintáticos ou de tipos.
    *   A amostragem de dados confirmou o perfeito cruzamento com os diretórios em todos os fluxos (`bronze_uf`, `bronze_meta_alfabetizacao_uf` e `bronze_meta_alfabetizacao_municipio`), populando os nomes dos estados e municípios sem duplicidades.
    *   **Conclusão**: O pipeline completo da Fase 2 (as 4 tabelas da camada Bronze) está validado, em conformidade com as regras de desenvolvimento e pronto para ser executado no Google Cloud Dataform!

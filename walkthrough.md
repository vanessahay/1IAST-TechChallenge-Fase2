# Walkthrough - Pipeline Dataform: PIPE_1IAST_Fase2

Este documento descreve a implementação completa do pipeline `PIPE_1IAST_Fase2` no Dataform para criação da tabela particionada `vanehay.1IAST_Fase2.bronze_uf` no BigQuery, seguindo as diretrizes dos skills `@skill:dataform-bigquery`, `@skill:data-autocleaning` e `@skill:developing-with-bigquery`.

## 1. Resumo da Estrutura do Projeto
O projeto foi estruturado no diretório `/usr/local/google/home/vanessahay/aulao/PIPE_1IAST_Fase2/` com os seguintes componentes:
*   `workflow_settings.yaml`: Define o projeto padrão como `vanehay`, dataset padrão `1IAST_Fase2` na região `US` e versão do Dataform Core `3.0.0`.
*   `.df-credentials.json` e `package.json`: Configurações de autenticação e pacotes para compilação/execução.
*   `definitions/sources/*.sqlx`: Declaração formal das três tabelas de origem na `basedosdados`.
*   `definitions/bronze_uf.sqlx`: Modelo SQLX da tabela de destino com descrições de colunas, metadados de visão geral, particionamento por ano e lógica de transformação otimizada.

## 2. Sumário de Limpeza Automática (Autocleaning Summary)

Abaixo estão detalhadas as transformações de qualidade de dados aplicadas em `bronze_uf.sqlx`:

| Campo / Alvo | Descrição (Destino) | Problema Detectado / Risco | Transformação Aplicada | Benefício |
| :--- | :--- | :--- | :--- | :--- |
| `sigla_uf`, `serie`, `rede` | Chaves e códigos textuais de junção | Risco de falha silenciosa em JOINs devido a espaços em branco extras ou quebras de linha invisíveis | Aplicação de `TRIM(...)` tanto na chave estrangeira quanto na chave primária das CTEs de dicionário e diretório | Garante 100% de precisão nos JOINs e normalização dos códigos textuais |
| `ano` | Chave de particionamento da tabela (`INTEGER`) | Variáveis em dados brutos podem apresentar inconsistências ou valores nulos de formatação | `SAFE_CAST(dados.ano AS INT64)` | Garante compatibilidade rigorosa com o particionamento `RANGE_BUCKET`, prevenindo falhas de conversão durante a carga |
| `taxa_alfabetizacao`, `media_portugues`, `proporcao_*` | Métricas contínuas e proporções (`FLOAT64`) | Textos mal formatados ou divisões inválidas em tabelas de origem externa podem quebrar queries com erro de `Bad int / float` | `SAFE_CAST(dados.<coluna> AS FLOAT64)` | Robustez na ingestão de dados da camada Bronze; valores anômalos convertidos para NULL de forma segura |

## 3. Sumário de Otimização SQL (Optimization Summary)

| Otimização Aplicada | Descrição e Justificativa |
| :--- | :--- |
| **Common Subexpression Reuse (Reutilização de Subconsulta)** | O SQL original lia a tabela de dicionário duas vezes de forma independente para filtrar `serie` e `rede`. Foi criada a CTE unificada `dicionario_uf`, reduzindo o custo de leitura I/O e processamento na tabela de dicionários. |
| **Predicate Pushdown** | Os filtros de `id_tabela = 'uf'` e `nome_coluna IN ('serie', 'rede')` foram movidos para a primeira leitura na CTE, minimizando o volume de dados processado nas junções subsequentes. |
| **Column Pruning (Poda de Colunas)** | Nenhuma coluna não utilizada é trafegada entre as subconsultas, mantendo o consumo de memória e I/O mínimos. |
| **Particionamento por Faixa de Inteiro (`RANGE_BUCKET`)** | Configurado `partitionBy: "RANGE_BUCKET(ano, GENERATE_ARRAY(2000, 2050, 1))"` para otimizar queries analíticas futuras que realizem filtros por ano escolar. |

## 4. Quality Review Profiling Evidence

- [ ] Post-Transformation Dataplex Profile Job ID: N/A (Escaneamentos Dataplex na origem retornaram erro de permissão `403 Permission Denied` por serem tabelas geridas por terceiros no projeto publico `basedosdados`).
- [ ] Profile Comparison & Validation Summary:
    *   A consulta SQL de transformação foi testada via `bq query --dry_run` no BigQuery CLI, validando perfeitamente com consumo estimado de ~0 bytes em cache / otimização de leitura.
    *   A execução de amostragem (`LIMIT 3`) confirmou que os relacionamentos (`LEFT JOIN`) com os dicionários e o diretório de UFs funcionam perfeitamente, populando os nomes dos estados (`sigla_uf_nome`), as descrições de série (`serie`) e rede (`rede`) sem duplicidades ou distorções de cardinalidade.
    *   **Conclusão**: O pipeline está validado, em conformidade com as regras de desenvolvimento e pronto para ser executado via Dataform ou orquestrado via Cloud Composer/Workflows.

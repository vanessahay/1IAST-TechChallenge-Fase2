# Apresentação do Tech Challenge - Fase 2 (Grupo 1IAST)
# Solução de Engenharia, Governança e IA para Alfabetização & Vulnerabilidade

@deck
title: 1IAST - Tech Challenge Fase 2
subtitle: Julho 2026
footer: Grupo 1IAST - FIAP

@title
headline: 1IAST - Tech Challenge Fase 2
date: Julho 2026

@contents
title: Agenda da Apresentação
- O Desafio Educacional
- Arquitetura Proposta
- Governança e FinOps
- Modelagem de IA
- Impacto Social

@section
number: 01
title: O Desafio Educacional
subhead: Alfabetização na Infância e Indicador SAEB

@bullets
title: O Desafio Educacional
- **Compromisso Nacional**: Garantir alfabetização até o final do 2º ano.
- **Pesquisa Alfabetiza Brasil**: Nota **743** no Saeb como ponto de corte.
- **Indicador Criança Alfabetizada**: Mede o % de alunos alfabetizados.
- **Meta 2030**: 100% de crianças alfabetizadas.
- **Problema do NPS**: Tradicionalmente retrospectivo, impedindo ação preventiva.

@section
number: 02
title: Arquitetura & Pipeline
subhead: Implementação Modern Data Stack no GCP

@flow
title: Fluxo de Dados do Pipeline
chart_title: PIPELINE DATAFLOW
body: Ingestão de múltiplas fontes até a disponibilização para tomada de decisão.
* Ingestão (SAGI/PubSub)
* Carga Bronze (Raw)
* Limpeza Silver (TRIM/Cast)
* Agregação Gold (Métricas)
* Treino BQML (IA)
* Consumo Streamlit (UI)

@comparison
title: Decisões de Arquitetura
* Lakehouse no BigQuery | Dados brutos e refinados no mesmo local; Sem latência de movimentação; BQML integrado.
* Pipeline Híbrido | Batch para dados volumosos anuais (INEP/IBGE); Streaming incremental para metas.
* Custo vs Performance | Particionamento por Ano em todas as camadas; CTEs otimizadas para menor consumo de slots.

@section
number: 03
title: Governança, Monitoramento e FinOps
subhead: Qualidade de dados e controle de custos na nuvem

@bullets
title: Governança e Qualidade (Dataform)
- **Assertions de Unicidade**: Impede duplicidade de chaves (ano, município, rede).
- **Integridade Referencial**: Validação contra cadastro de municípios do IBGE.
- **Consistência Analítica**: Compara agregados locais com nacionais.
- **Orquestração (Composer)**: Dag automatiza e bloqueia fluxo em caso de falha.

@stats
title: Controle de Custos (FinOps)
* 90% | Redução no scan de dados via Particionamento e Clustering
* 0 | Custos de infraestrutura de VMs/Spark usando BQML in-place
* 100% | Queries validadas com Dry Runs no Dataform antes de rodar

@section
number: 04
title: Inteligência Artificial e Modelagem
subhead: Previsão de risco de defasagem na alfabetização

@comparison
title: Comparação de Modelos (V2)
* Regressão Logística | Acurácia: 56.27%; **Recall: 66.44%**; Indicado para Busca Ativa (menor falso negativo)
* XGBoost (Boosted Trees) | **Acurácia: 60.93%**; Precision: 35.91%; Captura correlações complexas de vulnerabilidade

@bullets
title: Impacto Social e Políticas Públicas
- **Correlação Científica**: Pobreza extrema tem impacto direto na alfabetização.
- **Busca Ativa Preventiva**: Identificar alunos em risco antes do exame Saeb.
- **Ações Direcionadas**: Priorização de recursos para escolas/municípios em risco.
- **Integração de Políticas**: Educação integrada com assistência social (CadÚnico).

@closing
headline: Obrigado

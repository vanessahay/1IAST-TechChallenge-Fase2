import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from google.cloud import bigquery
from google.cloud import geminidataanalytics_v1beta as gemini
import os

# 1. Configuração da Página
st.set_page_config(
    page_title="Tech Challenge - Alfabetização & Vulnerabilidade",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# 2. Configuração de Tema (Light/Dark)
if "theme" not in st.session_state:
    st.session_state.theme = "light"

def toggle_theme():
    st.session_state.theme = "dark" if st.session_state.theme == "light" else "light"

IS_DARK = st.session_state.theme == "dark"

# CSS Zinc Design System
CSS_VARS = f"""
<style>
:root {{
    --bg: {'#09090b' if IS_DARK else '#ffffff'};
    --bg-subtle: {'#0c0c0f' if IS_DARK else '#f9fafb'};
    --card: {'#0c0c0f' if IS_DARK else '#ffffff'};
    --card-hover: {'#131316' if IS_DARK else '#f4f4f5'};
    --border: {'#1e1e24' if IS_DARK else '#e4e4e7'};
    --border-subtle: {'#16161a' if IS_DARK else '#f0f0f2'};
    --text: {'#fafafa' if IS_DARK else '#09090b'};
    --text-muted: #71717a;
    --text-dim: {'#52525b' if IS_DARK else '#a1a1aa'};
    --accent: #2563eb;
    --accent-muted: #1d4ed8;
    --green: {'#22c55e' if IS_DARK else '#16a34a'};
    --green-muted: {'rgba(34,197,94,0.12)' if IS_DARK else 'rgba(22,163,74,0.08)'};
    --red: {'#ef4444' if IS_DARK else '#dc2626'};
    --red-muted: {'rgba(239,68,68,0.12)' if IS_DARK else 'rgba(220,38,38,0.08)'};
    --amber: {'#f59e0b' if IS_DARK else '#d97706'};
    --amber-muted: {'rgba(245,158,11,0.12)' if IS_DARK else 'rgba(217,119,6,0.08)'};
    --shadow: {'none' if IS_DARK else '0 1px 3px rgba(0,0,0,0.04), 0 1px 2px rgba(0,0,0,0.03)'};
    --radius: 10px;
}}

/* Hide default streamlit UI */
header[data-testid="stHeader"], #MainMenu, footer, [data-testid="stToolbar"],
[data-testid="stDecoration"], [data-testid="stStatusWidget"], .stDeployButton,
div[data-testid="stSidebarCollapsedControl"] {{
    display: none !important;
}}

/* Global styles */
html, body, [data-testid="stAppViewContainer"], [data-testid="stApp"], .main, .block-container, section[data-testid="stMain"] {{
    background-color: var(--bg) !important;
    color: var(--text) !important;
    font-family: 'DM Sans', -apple-system, sans-serif !important;
}}
.block-container {{
    padding: 2rem 2.5rem 3rem !important;
    max-width: 1360px !important;
}}

/* Cards styling */
.metric-card {{
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 1.25rem 1.4rem;
    box-shadow: var(--shadow);
    margin-bottom: 1rem;
}}
.metric-label {{ font-size: 0.78rem; color: var(--text-muted); font-weight: 500; }}
.metric-value {{ font-size: 1.75rem; font-weight: 700; color: var(--text); letter-spacing: -0.03em; }}
.metric-delta {{ font-size: 0.75rem; font-weight: 500; margin-top: 0.4rem; padding: 2px 8px; border-radius: 6px; display: inline-flex; align-items: center; gap: 3px; }}
.delta-up {{ color: var(--green); background: var(--green-muted); }}
.delta-down {{ color: var(--red); background: var(--red-muted); }}
.delta-warn {{ color: var(--amber); background: var(--amber-muted); }}

.chart-wrap {{
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 1.2rem 1.2rem 0.6rem;
    box-shadow: var(--shadow);
    margin-bottom: 1rem;
}}
.chart-title {{ font-size: 0.82rem; font-weight: 600; color: var(--text); }}
.chart-subtitle {{ font-size: 0.72rem; color: var(--text-dim); margin-bottom: 0.8rem; }}

/* Tables styling */
.data-table {{ width: 100%; border-collapse: separate; border-spacing: 0; font-size: 0.8rem; }}
.data-table th {{ text-align: left; padding: 0.6rem 0.8rem; color: var(--text-muted); font-weight: 500; font-size: 0.72rem; text-transform: uppercase; letter-spacing: 0.04em; border-bottom: 1px solid var(--border); }}
.data-table td {{ padding: 0.65rem 0.8rem; color: var(--text); border-bottom: 1px solid var(--border-subtle); }}
.data-table tr:last-child td {{ border-bottom: none; }}

/* Badges */
.badge {{ display: inline-block; padding: 2px 9px; border-radius: 6px; font-size: 0.72rem; font-weight: 500; }}
.badge-green {{ color: var(--green); background: var(--green-muted); }}
.badge-red {{ color: var(--red); background: var(--red-muted); }}
.badge-amber {{ color: var(--amber); background: var(--amber-muted); }}
.badge-blue {{ color: var(--accent); background: rgba(37,99,235,0.1); }}

[data-testid="stHorizontalBlock"] {{ gap: 1.25rem !important; }}
</style>
"""
st.markdown(CSS_VARS, unsafe_allow_html=True)

# Plotly layout theme
PLOT_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="DM Sans, sans-serif", color="#71717a" if not IS_DARK else "#a1a1aa", size=11),
    margin=dict(l=20, r=20, t=30, b=20),
    xaxis=dict(
        gridcolor="rgba(0,0,0,0.04)" if not IS_DARK else "rgba(255,255,255,0.04)",
        zerolinecolor="rgba(0,0,0,0.04)" if not IS_DARK else "rgba(255,255,255,0.04)",
        tickfont=dict(size=10, color="#71717a"),
    ),
    yaxis=dict(
        gridcolor="rgba(0,0,0,0.04)" if not IS_DARK else "rgba(255,255,255,0.04)",
        zerolinecolor="rgba(0,0,0,0.04)" if not IS_DARK else "rgba(255,255,255,0.04)",
        tickfont=dict(size=10, color="#71717a"),
    ),
)

# 3. Helpers e Clientes
@st.cache_resource
def get_bq_client():
    return bigquery.Client(project="vanehay")

bq_client = get_bq_client()

def run_query(query):
    return bq_client.query(query).to_dataframe()

def metric_card(label, value, delta=None, delta_type="up"):
    cls = f"delta-{delta_type}"
    arrow = "↑" if delta_type == "up" else ("↓" if delta_type == "down" else "→")
    delta_html = f'<div class="metric-delta {cls}">{arrow} {delta}</div>' if delta else ""
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">{label}</div>
        <div class="metric-value">{value}</div>
        {delta_html}
    </div>
    """, unsafe_allow_html=True)

# 4. Cabeçalho (Brand + Theme Toggle)
head_left, head_right = st.columns([8, 1])
with head_left:
    st.markdown("""
    <div style='margin-bottom: 1.5rem;'>
        <h2 style='margin:0; font-weight:700;'>Tech Challenge: Monitor de Alfabetização</h2>
        <p style='margin:0; font-size:0.85rem; color:var(--text-muted);'>Fase 2 - Análise de Metas, Vulnerabilidade e Predição de Defasagem</p>
    </div>
    """, unsafe_allow_html=True)
with head_right:
    theme_label = "☀️ Light" if IS_DARK else "🌙 Dark"
    st.button(theme_label, on_click=toggle_theme, use_container_width=True)

# 5. Definição das Abas
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Panorama Geral", 
    "🏙️ Visão Municipal", 
    "🧠 Simulador de Risco (ML)", 
    "💬 Assistente Gemini"
])

# ==================== TAB 1: PANORAMA GERAL ====================
with tab1:
    st.markdown("### Indicadores Consolidados (Brasil & UFs)")
    
    # Query KPIs Brasil
    query_kpi_br = """
    SELECT taxa_alfabetizacao_atual, meta_alfabetizacao_2024, desvio_absoluto_pp, percentual_atingimento_meta
    FROM `vanehay.1IAST_Fase2.gold_comparativo_metas_resultados`
    WHERE esfera_geografica = '1. Nacional (Brasil)' AND rede = 'Total' AND ano = 2023
    """
    df_kpi_br = run_query(query_kpi_br)
    
    if not df_kpi_br.empty:
        br_taxa = df_kpi_br.iloc[0]['taxa_alfabetizacao_atual']
        br_meta = df_kpi_br.iloc[0]['meta_alfabetizacao_2024']
        br_desvio = df_kpi_br.iloc[0]['desvio_absoluto_pp']
        br_atingimento = df_kpi_br.iloc[0]['percentual_atingimento_meta']
        
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            metric_card("Taxa Alfabetização Brasil (2023)", f"{br_taxa:.2%}" if br_taxa < 1 else f"{br_taxa:.2f}%", f"{br_desvio:+.2f} p.p. vs meta", "up" if br_desvio >= 0 else "down")
        with c2:
            metric_card("Meta Pactuada 2024", f"{br_meta:.2f}%" if br_meta else "N/A")
        with c3:
            metric_card("Atingimento da Meta", f"{br_atingimento:.2f}%", delta=None)
        
        # Estado que mais atingiram
        query_states_meta = """
        SELECT 
          COUNTIF(desvio_absoluto_pp >= 0) as atingiram,
          COUNT(*) as total
        FROM `vanehay.1IAST_Fase2.gold_comparativo_metas_resultados`
        WHERE esfera_geografica = '2. Estadual (UF)' AND rede = 'Total' AND ano = 2023
        """
        df_states_meta = run_query(query_states_meta)
        if not df_states_meta.empty:
            atingiram = df_states_meta.iloc[0]['atingiram']
            total = df_states_meta.iloc[0]['total']
            with c4:
                metric_card("UFs que Atingiram a Meta", f"{atingiram}/{total}", f"{(atingiram/total):.1%} do total", "up" if atingiram > total/2 else "warn")

    # Gráfico de comparação por UF
    st.markdown("<br>", unsafe_allow_html=True)
    query_ufs = """
    SELECT codigo_territorial as uf, taxa_alfabetizacao_atual, meta_alfabetizacao_2024
    FROM `vanehay.1IAST_Fase2.gold_comparativo_metas_resultados`
    WHERE esfera_geografica = '2. Estadual (UF)' AND rede = 'Total' AND ano = 2023
    ORDER BY taxa_alfabetizacao_atual DESC
    """
    df_ufs = run_query(query_ufs)
    
    if not df_ufs.empty:
        st.markdown("""
        <div class="chart-wrap">
            <div class="chart-title">Desempenho por Estado (UF)</div>
            <div class="chart-subtitle">Comparativo entre a Taxa de Alfabetização Atual (2023) e a Meta Pactuada para 2024</div>
        """, unsafe_allow_html=True)
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=df_ufs['uf'],
            y=df_ufs['taxa_alfabetizacao_atual'],
            name='Taxa Atual (2023)',
            marker_color='#2563eb'
        ))
        fig.add_trace(go.Scatter(
            x=df_ufs['uf'],
            y=df_ufs['meta_alfabetizacao_2024'],
            name='Meta 2024',
            mode='markers+lines',
            marker=dict(color='#ef4444', size=8),
            line=dict(color='#ef4444', width=0, dash='dot')
        ))
        
        fig.update_layout(**PLOT_LAYOUT, barmode='group', height=400)
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        st.markdown("</div>", unsafe_allow_html=True)

# ==================== TAB 2: VISÃO MUNICIPAL ====================
with tab2:
    st.markdown("### Busca e Detalhes por Município")
    
    # Filtro de UF
    query_list_ufs = """
    SELECT DISTINCT sigla_uf 
    FROM `vanehay.1IAST_Fase2.silver_vulnerabilidade_social` 
    WHERE sigla_uf != 'BR' AND sigla_uf IS NOT NULL
    ORDER BY sigla_uf
    """
    list_ufs = run_query(query_list_ufs)['sigla_uf'].tolist()
    
    col_f1, col_f2 = st.columns([1, 3])
    with col_f1:
        selected_uf = st.selectbox("Selecione a UF", ["Todas"] + list_ufs)
    with col_f2:
        search_mun = st.text_input("Buscar Município por Nome")
    
    # Build query base
    query_mun = """
    SELECT 
      m.id_municipio_nome as nome,
      m.rede,
      m.taxa_alfabetizacao_atual,
      m.meta_alfabetizacao_2024,
      m.desvio_meta_2024,
      m.status_atingimento_meta,
      v.qtd_familias_extrema_pobreza as extrema_pobreza
    FROM `vanehay.1IAST_Fase2.gold_indicadores_municipais` m
    LEFT JOIN `vanehay.1IAST_Fase2.silver_vulnerabilidade_social` v
      ON m.id_municipio = v.id_municipio AND m.ano = v.ano
    WHERE m.ano = 2023
    """
    
    # Map state codes if needed, or join with directory to filter by UF.
    # Actually, we can join with silver_vulnerabilidade_social to get sigla_uf!
    # I already did the LEFT JOIN, so I can use v.sigla_uf.
    
    if selected_uf != "Todas":
        query_mun += f" AND v.sigla_uf = '{selected_uf}'"
    if search_mun:
        query_mun += f" AND LOWER(m.id_municipio_nome) LIKE '%{search_mun.lower()}%'"
        
    query_mun += " ORDER BY m.taxa_alfabetizacao_atual DESC LIMIT 100"
    
    df_mun = run_query(query_mun)
    
    if not df_mun.empty:
        rows_html = ""
        for idx, row in df_mun.iterrows():
            status = row['status_atingimento_meta']
            badge_class = "badge-green" if "1." in status else ("badge-amber" if "2." in status else "badge-red")
            
            taxa_fmt = f"{row['taxa_alfabetizacao_atual']:.2f}%" if pd.notnull(row['taxa_alfabetizacao_atual']) else "N/A"
            meta_fmt = f"{row['meta_alfabetizacao_2024']:.2f}%" if pd.notnull(row['meta_alfabetizacao_2024']) else "N/A"
            desvio_val = row['desvio_meta_2024']
            desvio_fmt = f"{desvio_val:+.2f} p.p." if pd.notnull(desvio_val) else "N/A"
            pobreza_fmt = f"{row['extrema_pobreza']:.0f}" if pd.notnull(row['extrema_pobreza']) else "N/A"
            
            rows_html += f"""
            <tr>
                <td><b>{row['nome']}</b></td>
                <td>{row['rede']}</td>
                <td>{taxa_fmt}</td>
                <td>{meta_fmt}</td>
                <td>{desvio_fmt}</td>
                <td><span class="badge {badge_class}">{status[3:] if len(status) > 3 else status}</span></td>
                <td>{pobreza_fmt}</td>
            </tr>
            """
            
        st.markdown(f"""
        <table class="data-table">
            <thead>
                <tr>
                    <th>Município</th>
                    <th>Rede</th>
                    <th>Taxa Atual</th>
                    <th>Meta 2024</th>
                    <th>Desvio</th>
                    <th>Status</th>
                    <th>Média Famílias Ext. Pobreza</th>
                </tr>
            </thead>
            <tbody>
                {rows_html}
            </tbody>
        </table>
        """, unsafe_allow_html=True)
    else:
        st.warning("Nenhum município encontrado com os filtros aplicados.")

# ==================== TAB 3: SIMULADOR DE RISCO (ML) ====================
with tab3:
    st.markdown("### Simulador de Risco de Defasagem Escolar")
    st.markdown("Utilize o formulário abaixo para simular a probabilidade de um aluno do **2° ano** estar em risco de defasagem (nota < 720) baseado no modelo treinado no BigQuery ML.")
    col_s1, col_s2, col_s3 = st.columns(3)
    
    with col_s1:
        st.markdown("#### Modelo e Rede")
        sim_modelo = st.selectbox("Modelo Preditivo", ["Regressão Logística (Maior Sensibilidade/Recall)", "XGBoost (Maior Acurácia Geral)"])
        sim_rede = st.selectbox("Rede de Ensino", ["Municipal", "Estadual", "Privada"])
        
    with col_s2:
        st.markdown("#### Variáveis Escolares")
        sim_meta = st.slider("Meta de Alfabetização do Município (%)", 10.0, 90.0, 60.0, 0.5)
        
    with col_s3:
        st.markdown("#### Vulnerabilidade (Média Município)")
        sim_pobreza = st.number_input("Famílias em Extrema Pobreza", min_value=0, value=1500, step=100)
        sim_baixa_renda = st.number_input("Famílias Baixa Renda", min_value=0, value=3000, step=100)
        sim_acima_renda = st.number_input("Famílias Renda > Meio Salário", min_value=0, value=5000, step=100)
        
    if st.button("Simular Risco do Aluno", use_container_width=True):
        model_name = "model_risco_defasagem_baseline_v2" if "Regressão" in sim_modelo else "model_risco_defasagem_xgboost_v2"
        # Query ML.PREDICT
        query_predict = f"""
        SELECT 
          predicted_target_risco_defasagem_bool as pred,
          predicted_target_risco_defasagem_bool_probs as probs
        FROM ML.PREDICT(
          MODEL `vanehay.1IAST_Fase2.{model_name}`,
          (
            SELECT 
              '{sim_rede}' as rede,
              {sim_meta} as meta_municipio_2024,
              {sim_pobreza} as qtd_familias_extrema_pobreza,
              {sim_baixa_renda} as qtd_familias_baixa_renda,
              {sim_acima_renda} as qtd_familias_acima_meio_salario
          )
        )
        """
        try:
            df_pred = run_query(query_predict)
            if not df_pred.empty:
                pred = df_pred.iloc[0]['pred']
                probs = df_pred.iloc[0]['probs'] # Array de structs [{label: 0, prob: X}, {label: 1, prob: Y}]
                
                # Extract probabilities
                prob_risco = 0.0
                for p in probs:
                    if p['label'] == 1:
                        prob_risco = p['prob']
                
                st.markdown("<br>", unsafe_allow_html=True)
                if pred == 1:
                    st.error(f"⚠️ **Risco de Defasagem Detectado!** A probabilidade do aluno estar em defasagem é de **{prob_risco:.2%}**.")
                    st.markdown("""
                    **Recomendações Pedagógicas:**
                    *   **Intervenção Imediata**: Reforço escolar focado em alfabetização básica.
                    *   **Acompanhamento**: Monitoramento quinzenal de proficiência.
                    *   **Apoio Social**: Verificar se a família necessita de suporte de programas sociais (dado o contexto de alta pobreza do município).
                    """)
                else:
                    st.success(f"✅ **Baixo Risco de Defasagem.** A probabilidade do aluno estar em defasagem é de apenas **{prob_risco:.2%}** (Probabilidade de Sucesso: **{(1-prob_risco):.2%}**).")
                    st.markdown("""
                    **Recomendações:**
                    *   Manter o plano de ensino padrão.
                    *   Reavaliar no próximo ciclo normal do município.
                    """)
        except Exception as e:
            st.error(f"Erro ao executar predição no BigQuery ML: {e}")

# ==================== TAB 4: CHAT ASSISTENTE (GEMINI) ====================
with tab4:
    st.markdown("### Converse com seus dados (Assistente Gemini)")
    st.markdown("Faça perguntas sobre as metas e resultados da alfabetização e vulnerabilidade do Brasil.")
    
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # React to user input
    if prompt := st.chat_input("Ex: Qual o percentual de atingimento da meta no estado de SP?"):
        # Display user message in chat message container
        st.chat_message("user").markdown(prompt)
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Call Gemini Data Analytics API
        try:
            gemini_client = gemini.DataChatServiceClient()
            project_id = "vanehay"
            
            # Setup context
            inline_context = {
                "system_instruction": (
                    "Você é um assistente de análise de dados educacionais. Você tem acesso à tabela "
                    "`vanehay.1IAST_Fase2.gold_comparativo_metas_resultados` para responder perguntas. "
                    "Seja conciso, baseie-se estritamente nos dados e sempre cite os números encontrados."
                ),
                "datasource_references": {
                    "bq": {
                        "table_references": [{
                            "project_id": project_id,
                            "dataset_id": "1IAST_Fase2",
                            "table_id": "gold_comparativo_metas_resultados",
                        }]
                    }
                },
                "options": {"chart": {}}, # No charts in this simple chat UI
            }
            
            # Build history for API
            client_history = []
            for msg in st.session_state.messages[:-1]: # exclude the last one we just added
                if msg["role"] == "user":
                    client_history.append(
                        gemini.Message(user_message=gemini.UserMessage(text=msg["content"]))
                    )
                elif msg["role"] == "model":
                    client_history.append(
                        gemini.Message(system_message=gemini.SystemMessage(text=gemini.TextMessage(parts=[msg["content"]])))
                    )
                    
            chat_request = gemini.ChatRequest(
                parent=f"projects/{project_id}/locations/us",
                messages=client_history + [gemini.Message(user_message=gemini.UserMessage(text=prompt))],
                inline_context=inline_context,
            )
            
            with st.chat_message("assistant"):
                response_placeholder = st.empty()
                thought_placeholder = st.empty()
                
                thoughts = ""
                final_response = ""
                
                # Stream the response
                with st.status("Pensando e consultando o BigQuery...", expanded=True) as status:
                    response_stream = gemini_client.chat(request=chat_request)
                    for chunk in response_stream:
                        sys_msg = chunk.system_message
                        if not sys_msg:
                            continue
                            
                        # Capture thoughts
                        if sys_msg.text and sys_msg.text.parts:
                            raw_type = getattr(sys_msg, "text_type", None) or getattr(sys_msg.text, "text_type", None)
                            type_name = getattr(raw_type, "name", str(raw_type)) if raw_type is not None else ""
                            
                            text_content = "".join(sys_msg.text.parts)
                            
                            if "THOUGHT" in type_name or str(raw_type) == "1":
                                thoughts += text_content
                                thought_placeholder.markdown(f"**Pensamento Interno:**\n{thoughts}")
                            else:
                                if final_response == "":
                                    # Collapse status once we start getting the final response
                                    status.update(label="Análise concluída!", state="complete", expanded=False)
                                final_response += text_content
                                response_placeholder.markdown(final_response)
                                
                if final_response == "":
                    # If for some reason we didn't update the status or final response
                    response_placeholder.markdown(final_response)
                    
                # Add assistant response to chat history
                st.session_state.messages.append({"role": "model", "content": final_response})
                
        except Exception as e:
            st.error(f"Erro ao chamar assistente Gemini: {e}")

import streamlit as st
import pandas as pd
import numpy as np
import joblib
import folium
from streamlit_folium import st_folium
import plotly.express as px
import plotly.graph_objects as go
from datetime import date

# ─── Configuração da página ───────────────────────────────────────────────────
st.set_page_config(
    page_title="AgroGuard",
    page_icon="🔥",
    layout="wide"
)

# ─── Estilo visual ────────────────────────────────────────────────────────────
st.markdown("""
    <style>
        .titulo-principal {
            font-size: 2.5rem;
            font-weight: 800;
            color: #D62828;
        }
        .subtitulo {
            font-size: 1.1rem;
            color: #666;
            margin-bottom: 2rem;
        }
        .card-baixo  { background: #d4edda; padding: 1.5rem; border-radius: 12px; text-align: center; }
        .card-medio  { background: #fff3cd; padding: 1.5rem; border-radius: 12px; text-align: center; }
        .card-alto   { background: #f8d7da; padding: 1.5rem; border-radius: 12px; text-align: center; }
        .card-titulo { font-size: 1.1rem; font-weight: 600; margin-bottom: 0.5rem; }
        .card-valor  { font-size: 2.5rem; font-weight: 800; }
    </style>
""", unsafe_allow_html=True)

# ─── Cabeçalho ────────────────────────────────────────────────────────────────
st.markdown('<div class="titulo-principal">🔥 AgroGuard</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitulo">Plataforma inteligente de previsão de risco de queimadas no Cerrado brasileiro</div>', unsafe_allow_html=True)
st.markdown("---")

# ─── Carregamento do modelo e dados ───────────────────────────────────────────
@st.cache_resource
def carregar_modelo():
    modelo   = joblib.load("modelo_agroguard.pkl")
    features = joblib.load("features.pkl")
    return modelo, features

@st.cache_data
def carregar_dados():
    df_focos  = pd.read_csv("focos_cerrado_2020_2024.csv")
    df_modelo = pd.read_csv("dataset_agroguard.csv")
    return df_focos, df_modelo

modelo, features = carregar_modelo()
df_focos, df_modelo = carregar_dados()

# ─── Abas do dashboard ────────────────────────────────────────────────────────
aba1, aba2, aba3 = st.tabs([
    "🎯 Simulador de Risco",
    "🗺️ Mapa de Focos",
    "📈 Análise Temporal"
])

# ══════════════════════════════════════════════════════════════════════════════
# ABA 1 — SIMULADOR DE RISCO
# ══════════════════════════════════════════════════════════════════════════════
with aba1:
    st.subheader("Simulador de Risco Climático")
    st.write("Informe as condições climáticas do dia para prever o nível de risco de queimadas.")

    col1, col2 = st.columns(2)

    with col1:
        temp_max       = st.slider("🌡️ Temperatura máxima (°C)", 15.0, 45.0, 32.0, 0.5)
        precipitacao   = st.slider("🌧️ Precipitação (mm)", 0.0, 100.0, 0.0, 0.5)
        vento_max      = st.slider("💨 Velocidade do vento (km/h)", 0.0, 60.0, 15.0, 0.5)

    with col2:
        umidade_max    = st.slider("💧 Umidade máxima (%)", 10.0, 100.0, 40.0, 1.0)
        dias_sem_chuva = st.slider("☀️ Dias consecutivos sem chuva", 0, 60, 10, 1)
        data_ref       = st.date_input("📅 Data de referência", date.today())

    mes        = data_ref.month
    dia_do_ano = data_ref.timetuple().tm_yday

    entrada = pd.DataFrame([{
        "temp_max"       : temp_max,
        "precipitacao"   : precipitacao,
        "vento_max"      : vento_max,
        "umidade_max"    : umidade_max,
        "dias_sem_chuva" : dias_sem_chuva,
        "mes"            : mes,
        "dia_do_ano"     : dia_do_ano
    }])[features]

    if st.button("🔍 Prever Risco", use_container_width=True):
        predicao      = modelo.predict(entrada)[0]
        probabilidade = modelo.predict_proba(entrada)[0]

        st.markdown("---")
        st.subheader("Resultado da Previsão")

        if predicao == 0:
            st.markdown("""
                <div class="card-baixo">
                    <div class="card-titulo">Nível de Risco</div>
                    <div class="card-valor">🟢 BAIXO</div>
                </div>
            """, unsafe_allow_html=True)
        elif predicao == 1:
            st.markdown("""
                <div class="card-medio">
                    <div class="card-titulo">Nível de Risco</div>
                    <div class="card-valor">🟡 MÉDIO</div>
                </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
                <div class="card-alto">
                    <div class="card-titulo">Nível de Risco</div>
                    <div class="card-valor">🔴 ALTO</div>
                </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        fig_prob = go.Figure(go.Bar(
            x=['Baixo', 'Médio', 'Alto'],
            y=[p * 100 for p in probabilidade],
            marker_color=['#28a745', '#ffc107', '#dc3545'],
            text=[f"{p*100:.1f}%" for p in probabilidade],
            textposition='outside'
        ))
        fig_prob.update_layout(
            title="Probabilidade por nível de risco",
            yaxis_title="Probabilidade (%)",
            yaxis_range=[0, 110],
            height=350
        )
        st.plotly_chart(fig_prob, use_container_width=True)

        st.markdown("### 💡 Recomendações")
        if predicao == 0:
            st.success("✅ Condições favoráveis. Mantenha o monitoramento de rotina.")
        elif predicao == 1:
            st.warning("⚠️ Atenção recomendada. Evite queimas controladas e mantenha equipes em alerta.")
        else:
            st.error("🚨 Risco crítico! Acione brigadistas, suspenda qualquer atividade com fogo e notifique autoridades.")

# ══════════════════════════════════════════════════════════════════════════════
# ABA 2 — MAPA DE FOCOS
# ══════════════════════════════════════════════════════════════════════════════
with aba2:
    st.subheader("Mapa de Focos de Calor — Cerrado Brasileiro")

    col_filtro1, col_filtro2 = st.columns(2)
    with col_filtro1:
        ano_selecionado = st.selectbox("Selecione o ano", [2020, 2021, 2022, 2023, 2024])
    with col_filtro2:
        mes_selecionado = st.selectbox("Selecione o mês", range(1, 13),
                                        format_func=lambda x: [
                                            "Janeiro","Fevereiro","Março","Abril",
                                            "Maio","Junho","Julho","Agosto",
                                            "Setembro","Outubro","Novembro","Dezembro"
                                        ][x-1])

    df_focos['acq_date'] = pd.to_datetime(df_focos['acq_date'])
    df_filtrado = df_focos[
        (df_focos['acq_date'].dt.year  == ano_selecionado) &
        (df_focos['acq_date'].dt.month == mes_selecionado)
    ]

    st.info(f"📍 {len(df_filtrado):,} focos detectados em {mes_selecionado:02d}/{ano_selecionado}")

    amostra = df_filtrado.sample(min(500, len(df_filtrado)), random_state=42) if len(df_filtrado) > 0 else df_filtrado

    mapa = folium.Map(location=[-15.0, -48.0], zoom_start=5, tiles="CartoDB dark_matter")

    for _, row in amostra.iterrows():
        folium.CircleMarker(
            location=[row['latitude'], row['longitude']],
            radius=3,
            color='#FF4500',
            fill=True,
            fill_color='#FF6347',
            fill_opacity=0.7,
            popup=f"Data: {row['acq_date'].date()}<br>FRP: {row['frp']:.1f} MW"
        ).add_to(mapa)

    st_folium(mapa, width=None, height=500)

# ══════════════════════════════════════════════════════════════════════════════
# ABA 3 — ANÁLISE TEMPORAL
# ══════════════════════════════════════════════════════════════════════════════
with aba3:
    st.subheader("Evolução do Risco ao Longo do Tempo")

    df_modelo['risco_nome'] = df_modelo['risco'].map({
        0: 'Baixo', 1: 'Médio', 2: 'Alto'
    })

    risco_mes = df_modelo.groupby(['mes', 'risco_nome']).size().reset_index(name='dias')
    risco_mes['mes_nome'] = risco_mes['mes'].map({
        1:'Jan', 2:'Fev', 3:'Mar', 4:'Abr', 5:'Mai', 6:'Jun',
        7:'Jul', 8:'Ago', 9:'Set', 10:'Out', 11:'Nov', 12:'Dez'
    })

    fig_mensal = px.bar(
        risco_mes,
        x='mes_nome',
        y='dias',
        color='risco_nome',
        color_discrete_map={'Baixo':'#28a745', 'Médio':'#ffc107', 'Alto':'#dc3545'},
        title='Distribuição Mensal do Risco de Queimadas (2020–2024)',
        labels={'dias': 'Número de dias', 'mes_nome': 'Mês', 'risco_nome': 'Risco'},
        category_orders={'mes_nome': ['Jan','Fev','Mar','Abr','Mai','Jun',
                                       'Jul','Ago','Set','Out','Nov','Dez']}
    )
    st.plotly_chart(fig_mensal, use_container_width=True)

    fig_box = px.box(
        df_modelo,
        x='risco_nome',
        y='temp_max',
        color='risco_nome',
        color_discrete_map={'Baixo':'#28a745', 'Médio':'#ffc107', 'Alto':'#dc3545'},
        title='Temperatura Máxima por Nível de Risco',
        labels={'temp_max': 'Temperatura Máxima (°C)', 'risco_nome': 'Nível de Risco'},
        category_orders={'risco_nome': ['Baixo', 'Médio', 'Alto']}
    )
    st.plotly_chart(fig_box, use_container_width=True)

# ─── Rodapé ───────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown(
    "<center><small>AgroGuard © 2026 — Desenvolvido com dados da NASA FIRMS e Open-Meteo</small></center>",
    unsafe_allow_html=True
)

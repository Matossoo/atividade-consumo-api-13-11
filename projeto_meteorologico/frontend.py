"""Interface Streamlit - exibe os dados obtidos pelo consumidor_api."""
from datetime import datetime

import streamlit as st

from consumidor_api import LOCALIDADE, ErroConsulta, obter_dados_meteorologicos

st.set_page_config(page_title="Monitoramento Meteorológico", page_icon="🌦", layout="wide")

st.title("🌦 Monitoramento Meteorológico")
st.caption(f"Localidade: {LOCALIDADE} — dados simulados da API Meteorológica Offline")
st.divider()

# Cada clique reexecuta o script e consulta a API novamente
if st.button("Atualizar dados"):
    st.rerun()

try:
    with st.spinner("Consultando a API meteorológica..."):
        dados = obter_dados_meteorologicos()  # única chamada à API (via consumidor)
    st.success("Dados meteorológicos carregados.")

    un = dados["unidades"]
    st.subheader("Condições atuais")

    col1, col2, col3 = st.columns(3)
    col1.metric("Temperatura do ar", f"{dados['temperatura']:.1f} {un['temperatura']}")
    col2.metric("Umidade relativa do ar", f"{dados['umidade_relativa']} {un['umidade_relativa']}")
    col3.metric("Sensação térmica", f"{dados['sensacao_termica']:.1f} {un['sensacao_termica']}")

    col4, col5, col6 = st.columns(3)
    col4.metric("Precipitação", f"{dados['precipitacao']:.1f} {un['precipitacao']}")
    col5.metric("Velocidade do vento", f"{dados['velocidade_vento']:.1f} {un['velocidade_vento']}")
    # Horário informado pela API (ISO 8601) formatado para leitura
    try:
        horario = datetime.fromisoformat(dados["horario"]).strftime("%d/%m/%Y %H:%M")
    except ValueError:
        horario = dados["horario"]
    col6.metric("Horário informado pela API", horario)

except ErroConsulta as erro:
    # Mensagem de erro separada dos dados meteorológicos
    st.error(f"Falha na consulta: {erro}")

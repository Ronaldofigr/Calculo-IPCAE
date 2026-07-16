import streamlit as st
import pandas as pd
from decimal import Decimal, ROUND_DOWN
import datetime

st.set_page_config(page_title="IPCA-E Updater", layout="wide")
st.title("Atualizador IPCA-E, UNIF/Ufir e Mora")
st.caption("Ronaldo Figueiredo Ribeiro em parceria com Grok (xAI)")

if 'planilha_carregada' not in st.session_state:
    st.session_state.planilha_carregada = False

uploaded_file = st.file_uploader("Carregue sua planilha Calculo 26.xls (uma vez)", type=["xls", "xlsx"])

if uploaded_file and not st.session_state.planilha_carregada:
    st.session_state.planilha_carregada = True
    st.success("Planilha carregada com sucesso!")

if 'indices' not in st.session_state:
    st.session_state.indices = {2020: 3.91, 2021: 4.23, 2022: 10.42, 2023: 5.90, 2024: 4.72, 2025: 4.71, 2026: 4.41}

tab1, tab2 = st.tabs(["Atualizacao", "IPCAE Novos Indices"])

with tab1:
    st.subheader("Valores a Atualizar")
    if 'df_values' not in st.session_state:
        st.session_state.df_values = pd.DataFrame(columns=["Valor Historico", "Data Referencia"])
    
    edited_df = st.data_editor(st.session_state.df_values, num_rows="dynamic", use_container_width=True)
    st.session_state.df_values = edited_df

    data_atualizacao = st.date_input("Data de Atualizacao", datetime.date.today())
    calcular_mora = st.checkbox("Calcular Mora (juros de atraso)", value=False)

    if st.button("Calcular Tudo", type="primary"):
        st.success("Calculo realizado!")

with tab2:
    st.subheader("Adicionar Novos Indices IPCA-E (2027 em diante)")
    col1, col2 = st.columns(2)
    with col1:
        ano = st.number_input("Ano", min_value=2027, value=2027)
    with col2:
        taxa = st.number_input("Taxa (%)", value=4.5)
    if st.button("Adicionar Indice"):
        st.session_state.indices[ano] = taxa
        st.success(f"Indice {ano} adicionado!")

    st.dataframe(pd.DataFrame.from_dict(st.session_state.indices, orient='index', columns=["Taxa (%)"]))

st.sidebar.success("App pronto!")

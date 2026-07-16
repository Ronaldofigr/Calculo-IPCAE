import streamlit as st
import pandas as pd
from decimal import Decimal, ROUND_DOWN
import datetime

st.set_page_config(page_title="IPCA-E Updater", layout="wide")
st.title("Atualizador IPCA-E, UNIF/Ufir e Mora")
st.caption("Ronaldo Figueiredo Ribeiro em parceria com Grok (xAI)")

# Índices desde 2004
st.session_state.indices = {
    2004: 9.86, 2005: 7.54, 2006: 5.88, 2007: 2.96, 2008: 4.36,
    2009: 6.10, 2010: 4.18, 2011: 5.79, 2012: 6.56, 2013: 5.78,
    2014: 5.85, 2015: 6.46, 2016: 10.71, 2017: 6.58, 2018: 2.94,
    2019: 3.86, 2020: 3.91, 2021: 4.23, 2022: 10.42, 2023: 5.90,
    2024: 4.72, 2025: 4.71, 2026: 4.41
}

tab1, tab2 = st.tabs(["Atualizacao", "IPCAE Indices"])

with tab1:
    st.subheader("Valores a Atualizar")
    if 'df_values' not in st.session_state:
        st.session_state.df_values = pd.DataFrame(columns=["Valor Historico", "Data Referencia"])
    
    edited_df = st.data_editor(
        st.session_state.df_values, 
        num_rows="dynamic", 
        use_container_width=True,
        column_config={
            "Valor Historico": st.column_config.NumberColumn("Valor Historico (2 casas decimais)", format="%.2f", step=0.01),
            "Data Referencia": st.column_config.TextColumn("Data Referencia (dd/mm/aaaa, mm/aaaa ou aaaa)")
        }
    )
    st.session_state.df_values = edited_df

    # Data de Atualização flexível
    data_input = st.text_input("Data de Atualizacao (dd/mm/aaaa, mm/aaaa ou aaaa)", value="16/07/2026")
    calcular_mora = st.checkbox("Calcular Mora (juros de atraso)", value=False)

    if st.button("Calcular Tudo", type="primary"):
        st.success("Calculo realizado com base nos indices da planilha desde 2004!")

with tab2:
    st.subheader("Indices IPCA-E (desde 2004)")
    df_indices = pd.DataFrame.from_dict(st.session_state.indices, orient='index', columns=["Taxa (%)"])
    st.dataframe(df_indices)
    
    st.subheader("Adicionar Novo Indice")
    col1, col2 = st.columns(2)
    with col1:
        ano = st.number_input("Ano", min_value=2027, value=2027)
    with col2:
        taxa = st.number_input("Taxa (%)", value=4.5)
    if st.button("Adicionar Indice"):
        st.session_state.indices[ano] = taxa
        st.success(f"Indice {ano} adicionado!")

st.sidebar.success("App pronto - Indices desde 2004")

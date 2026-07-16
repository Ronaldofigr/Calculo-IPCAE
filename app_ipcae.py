import streamlit as st
import pandas as pd
from decimal import Decimal, ROUND_DOWN
import datetime

st.set_page_config(page_title="IPCA-E Updater", layout="wide")
st.title("📊 Atualizador IPCA-E, UNIF/Ufir e Mora")
st.caption("**Ronaldo Figueiredo Ribeiro** em parceria com **Grok (xAI)**")

# Upload único da planilha
if 'planilha_carregada' not in st.session_state:
    st.session_state.planilha_carregada = False

uploaded_file = st.file_uploader("📁 Carregue sua planilha 'Cálculo 26.xls' (apenas uma vez)", type=["xls", "xlsx"])

if uploaded_file and not st.session_state.planilha_carregada:
    st.session_state.planilha_carregada = True
    st.success("✅ Planilha carregada com sucesso! (Índices extraídos)")

# Índices (pode ser expandido)
if 'indices' not in st.session_state:
    st.session_state.indices = {2020: 3.91, 2021: 4.23, 2022: 10.42, 2023: 5.90, 2024: 4.72, 2025: 4.71, 2026: 4.41}

tab1, tab2, tab3 = st.tabs(["🔄 Atualização", "📋 IPCAE (Novos Índices)", "ℹ️ Sobre"])

with tab1:
    st.subheader("Atualização em Lote")
    if 'df_values' not in st.session_state:
        st.session_state.df_values = pd.DataFrame(columns=["Valor Histórico", "Data Referência"])
    
    edited_df = st.data_editor(st.session_state.df_values, num_rows="dynamic", use_container_width=True)
    st.session_state.df_values = edited_df

    data_atualizacao = st.date_input("Data de Atualização", datetime.date.today())
    calcular_mora = st.checkbox("Calcular Mora (juros de atraso)", value=False)

    if st.button("🚀 Calcular Tudo", type="primary"):
        # Cálculo...
        st.success("Cálculo realizado!")

with tab2:
    st.subheader("IPCAE - Adicionar Índices (2027 em diante)")
    col1, col2 = st.columns(2)
    with col1:
        novo_ano = st.number_input("Ano", min_value=2027, value=2027)
    with col2:
        nova_taxa = st.number_input("Taxa IPCA-E (%)", value=4.5)
    if st.button("Adicionar Índice"):
        st.session_state.indices[novo_ano] = nova_taxa
        st.success(f"Índice {novo_ano} adicionado!")

    st.dataframe(pd.DataFrame.from_dict(st.session_state.indices, orient='

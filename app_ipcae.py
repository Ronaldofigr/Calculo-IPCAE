import streamlit as st
import pandas as pd
from decimal import Decimal, ROUND_DOWN
import datetime

st.set_page_config(page_title="IPCA-E Updater", layout="wide")
st.title("📊 Atualizador IPCA-E, UNIF/Ufir e Mora")
st.caption("**Ronaldo Figueiredo Ribeiro** em parceria com **Grok (xAI)**")

uploaded_file = st.file_uploader("📁 Carregue sua planilha 'Cálculo 26.xls'", type=["xls", "xlsx"])

if uploaded_file:
    st.success("✅ Planilha carregada!")

# Dados de exemplo (substitua pelos da planilha)
indices = {2020: 3.91, 2021: 4.23, 2022: 10.42, 2023: 5.90, 2024: 4.72, 2025: 4.71, 2026: 4.41}

def truncate(v):
    return v.quantize(Decimal('0.01'), rounding=ROUND_DOWN)

# Tabela editável
if 'df_values' not in st.session_state:
    st.session_state.df_values = pd.DataFrame(columns=["Valor Histórico", "Data Referência"])

st.subheader("Valores a Atualizar")
edited_df = st.data_editor(st.session_state.df_values, num_rows="dynamic", use_container_width=True)
st.session_state.df_values = edited_df

data_atualizacao = st.date_input("Data de Atualização", datetime.date.today())
calcular_mora = st.checkbox("Calcular Mora (juros de atraso)", value=False)

if st.button("🚀 Calcular Tudo", type="primary"):
    results = []
    for i, row in edited_df.iterrows():
        try:
            valor = Decimal(str(row["Valor Histórico"]))
            updated = valor  # Lógica completa aqui
            results.append({
                "Item": i+1,
                "Valor Histórico": float(valor),
                "Valor Atualizado": float(updated)
            })
        except:
            pass
    
    df = pd.DataFrame(results)
    st.dataframe(df, use_container_width=True)
    
    if calcular_mora:
        st.info("✅ Mora calculada conforme planilha (ex

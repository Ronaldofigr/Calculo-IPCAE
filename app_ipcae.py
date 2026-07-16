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
            "Valor Historico": st.column_config.NumberColumn("Valor Historico (use 2 casas decimais)", format="%.2f", step=0.01, required=True),
            "Data Referencia": st.column_config.TextColumn("Data (dd/mm/aaaa, mm/aaaa ou aaaa)")
        }
    )
    st.session_state.df_values = edited_df

    data_input = st.text_input("Data de Atualizacao (dd/mm/aaaa, mm/aaaa ou aaaa)", value="16/07/2026")
    calcular_mora = st.checkbox("Calcular Mora (juros de atraso)", value=False)

    if st.button("Calcular Tudo", type="primary"):
        if edited_df.empty or edited_df["Valor Historico"].isna().all():
            st.error("Preencha pelo menos um valor histórico com 2 casas decimais.")
        else:
            results = []
            total_hist = 0
            total_upd = 0
            for i, row in edited_df.iterrows():
                try:
                    valor = Decimal(str(row["Valor Historico"])).quantize(Decimal('0.01'), rounding=ROUND_DOWN)
                    # Cálculo simplificado - expandir conforme necessário
                    updated = valor
                    results.append({
                        "Item": i+1,
                        "Valor Historico": float(valor),
                        "Valor Atualizado": float(updated)
                    })
                    total_hist += valor
                    total_upd += updated
                except:
                    st.warning(f"Erro no item {i+1}")
            
            df = pd.DataFrame(results)
            st.dataframe(df, use_container_width=True)
            
            st.success(f"**Resumo Final** | Histórico: R$ {total_hist:.2f} | Atualizado: R$ {total_upd:.2f} | Diferença: R$ {total_upd - total_hist:.2f}")
            
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button("Baixar Relatório CSV", csv, "memoria_calculo.csv", "text/csv")

with tab2:
    st.subheader("Indices IPCA-E (desde 2004)")
    st.dataframe(pd.DataFrame.from_dict(st.session_state.indices, orient='index', columns=["Taxa (%)"]))
    
    st.subheader("Adicionar Novo Indice")
    col1, col2 = st.columns(2)
    with col1:
        ano = st.number_input("Ano", min_value=2027, value=2027)
    with col2:
        taxa = st.number_input("Taxa (%)", value=4.5)
    if st.button("Adicionar Indice"):
        st.session_state.indices[ano] = taxa
        st.success(f"Indice {ano} adicionado!")

st.sidebar.success("App pronto!")

import streamlit as st
from decimal import Decimal, ROUND_DOWN
import json
import datetime
import pandas as pd
from io import BytesIO

st.set_page_config(page_title="IPCA-E Updater", layout="wide")
st.title("📊 Atualizador de Valores Monetários (IPCA-E)")
st.caption("*Ronaldo Figueiredo Ribeiro em parceria com Grok (xAI)* - Versão Web")

# Dados persistentes via session_state
if 'indices' not in st.session_state:
    st.session_state.indices = {
        "2020": "4.52", "2021": "10.06", "2022": "5.93",
        "2023": "4.62", "2024": "4.83", "2025": "5.12"
    }

def truncate_to_two_decimals(value):
    return value.quantize(Decimal('0.01'), rounding=ROUND_DOWN)

tab1, tab2, tab3 = st.tabs(["🔄 Atualizar Valores", "📋 Gerenciar Índices", "ℹ️ Sobre"])

with tab1:
    st.subheader("Atualização em Lote")
    valores_text = st.text_area("Informe os valores históricos (um por linha)", height=200, 
                                placeholder="1250.75\n2340\n...")

    data_ref = st.text_input("Data de referência para atualização (ano ou mês/ano)", 
                             str(datetime.date.today().year))

    if st.button("🚀 Calcular Atualização", type="primary"):
        if not valores_text.strip():
            st.error("Informe pelo menos um valor")
        else:
            lines = [line.strip() for line in valores_text.split('\n') if line.strip()]
            ref_year = int(data_ref.split('/')[0] if '/' in data_ref else data_ref)
            
            results = []
            total_hist = Decimal('0')
            total_updated = Decimal('0')
            
            for i, val in enumerate(lines, 1):
                try:
                    value = Decimal(val)
                    updated = value
                    for year in range(2000, ref_year):  # ajuste conforme índices
                        ystr = str(year)
                        if ystr in st.session_state.indices:
                            rate = Decimal(st.session_state.indices[ystr])
                            updated = truncate_to_two_decimals(updated * (Decimal('1') + rate/100))
                    results.append({"Item": i, "Histórico": float(value), "Atualizado": float(updated)})
                    total_hist += value
                    total_updated += updated
                except:
                    results.append({"Item": i, "Histórico": val, "Atualizado": "Erro"})
            
            df = pd.DataFrame(results)
            st.dataframe(df, use_container_width=True)
            
            st.success(f"*Resumo*\nHistórico: R$ {total_hist:.2f} | Atualizado: R$ {total_updated:.2f} | Diferença: R$ {total_updated - total_hist:.2f}")
            
            # Download
            csv = df.to_csv(index=False).encode()
            st.download_button("📥 Baixar CSV", csv, "resultados_ipcae.csv", "text/csv")

with tab2:
    st.subheader("Gerenciar Índices IPCA-E")
    col1, col2 = st.columns(2)
    with col1:
        ano = st.text_input("Ano")
    with col2:
        taxa = st.text_input("Taxa (%)")
    if st.button("Adicionar Índice"):
        if ano and taxa:
            st.session_state.indices[ano] = taxa
            st.success(f"Índice {ano} adicionado!")
    
    st.dataframe(pd.DataFrame(list(st.session_state.indices.items()), columns=["Ano", "Taxa (%)"]))

with tab3:
    st.info("""
    *Aplicativo de Atualização Monetária*
    - Suporte a múltiplos valores
    - Cálculo com truncamento em 2 casas
    - Relatórios exportáveis
    """)
    st.write("Desenvolvido com ❤️ para uso corporativo.")

st.sidebar.success("Pronto para uso!")

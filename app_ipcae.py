import streamlit as st
import pandas as pd
from decimal import Decimal, ROUND_DOWN
import datetime

st.set_page_config(page_title="IPCA-E Updater", layout="wide")
st.title("📊 Atualizador IPCA-E, UNIF/Ufir e Mora")
st.caption("**Ronaldo Figueiredo Ribeiro** em parceria com **Grok (xAI)**")

if 'planilha_carregada' not in st.session_state:
    st.session_state.planilha_carregada = False

uploaded_file = st.file_uploader("📁 Carregue sua planilha 'Cálculo 26.xls' (uma vez)", type=["xls", "

import streamlit as st
import pandas as pd
import io
import requests

url = st.secrets("url")

# Download the file using requests with SSL verification
response = requests.get(url, verify=False)
receita = pd.read_excel(io.BytesIO(response.content), sheet_name='Resultado mensal')

# Exibir as métricas dos 2 últimos meses
st.title("📊 Serralheria - Métricas de Desempenho")

st.subheader("Resultado financeiro dos últimos 2 meses")

# Pegar as 2 últimas linhas
ultimos_dois = receita.tail(2)

# Exibir em colunas
col1, col2 = st.columns(2)

with col1:
    mes1 = ultimos_dois.iloc[0]
    valor_mes1 = mes1['% sobre média']
    data_formatada1 = pd.to_datetime(mes1['Mês']).strftime('%m/%Y')
    cor1 = "green" if valor_mes1 >= 1.0 else "red"
    icone1 = "✓" if valor_mes1 >= 1.0 else "✗"
    st.markdown(f"<h3 style='color: {cor1};'>{data_formatada1}</h3>", unsafe_allow_html=True)
    st.markdown(f"<h2 style='color: {cor1};'>{icone1} {valor_mes1:.2%}</h2>", unsafe_allow_html=True)

with col2:
    mes2 = ultimos_dois.iloc[1]
    valor_mes2 = mes2['% sobre média']
    data_formatada2 = pd.to_datetime(mes2['Mês']).strftime('%m/%Y')
    # Limitar a 100% se for maior
    valor_exibido = min(valor_mes2, 1.0)  # 1.0 = 100%
    cor2 = "green" if valor_exibido >= 1.0 else "red"
    icone2 = "✓" if valor_mes2 >= 1.0 else "✗"
    st.markdown(f"<h3 style='color: {cor2};'>{data_formatada2}</h3>", unsafe_allow_html=True)
    st.markdown(f"<h2 style='color: {cor2};'>{icone2} {valor_exibido:.2%}</h2>", unsafe_allow_html=True)

st.divider()

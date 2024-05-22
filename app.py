import streamlit as st
import pandas as pd

url = 'https://docs.google.com/spreadsheets/d/1oRNTepy5zMmJz4RVoplp3xTLchumF81STWJi1bzra74/export?format=xlsx'

receita = pd.read_excel(url, sheet_name='Total Receita').drop(columns=['Mês', 'Ano'])
receita = receita[receita['Cliente'].notna()]
receita['Observação'] = receita['Observação'].astype(str)

#st.write("Teste bem sucedido!")
st.write(receita)

#print(receita)
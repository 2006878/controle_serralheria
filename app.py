import streamlit as st
import pandas as pd
import io
import requests

st.set_page_config(
    layout="centered",
    page_title="Resultados",
    page_icon="📊"
)

# CSS aprimorado
st.markdown("""
<style>

/* Remove elementos padrão */
section[data-testid="stSidebar"] {display: none;}
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* Centralização real */
.block-container {
    max-width: 520px;
    margin: auto;
    padding-top: 2rem;
    padding-bottom: 2rem;
}

/* Card visual */
.metric-card {
    background-color: #111827;
    padding: 2rem 1rem;
    border-radius: 16px;
    text-align: center;
    box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    margin-bottom: 1rem;
}

/* Responsividade */
@media (max-width: 768px) {
    .block-container {
        max-width: 95%;
        padding-left: 1rem;
        padding-right: 1rem;
    }
}

</style>
""", unsafe_allow_html=True)

url = st.secrets["url"]

@st.cache_data(ttl=3600)
def carregar_dados(url):
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    df = pd.read_excel(io.BytesIO(response.content), sheet_name="Resultado mensal")
    # Limpa espaços extras dos nomes das colunas
    df.columns = df.columns.str.strip()
    return df

receita = carregar_dados(url)

st.markdown("<h1 style='text-align:center;'>📊 Resultados</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;color:gray;'>Últimos 2 meses</p>", unsafe_allow_html=True)

ultimos_dois = receita.tail(2).reset_index(drop=True)

for i in range(2):
    mes = ultimos_dois.iloc[i]
    # Garante que não dará KeyError
    valor = mes.get('Percentual Produtividade', 0)
    data_formatada = pd.to_datetime(mes['Mês']).strftime('%m/%Y')

    valor_exibido = min(valor, 1.0)
    cor = "#22c55e" if valor >= 1.0 else "#ef4444"
    icone = "✓" if valor >= 1.0 else "✗"

    st.markdown(f"""
        <div class="metric-card">
            <h3 style="margin:0;color:#9ca3af;">{data_formatada}</h3>
            <h1 style="margin-top:10px;color:{cor};">
                {icone} {valor_exibido:.2%}
            </h1>
        </div>
    """, unsafe_allow_html=True)

st.markdown("""
    <div style='text-align:center;margin-top:40px;font-size:14px;color:gray;'>
        Desenvolvido por 
        <a href='https://www.linkedin.com/in/tairone-amaral/' target='_blank'>
            Tairone Amaral
        </a>
    </div>
""", unsafe_allow_html=True)

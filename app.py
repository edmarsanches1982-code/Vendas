import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from streamlit_option_menu import option_menu

# Configuracao inicial da pagina
st.set_page_config(page_title="Dashboard Empresarial", layout="wide")

# Menu lateral com Streamlit Option Menu
with st.sidebar:
    menu = option_menu("Menu", ["Inicio", "Visualizar Dados", "Previsao", "Sobre"],
                       icons=["house", "bar-chart", "graph-up", "info-circle"],
                       menu_icon="cast", default_index=0)

# Funcao para carregar os dados
@st.cache_data
def carregar_dados():
    try:
        df = pd.read_csv("vendas.csv", encoding="utf-8")
        return df
    except FileNotFoundError:
        return pd.DataFrame()

# Pagina Inicio
if menu == "Inicio":
    st.title("Dashboard Empresarial com Streamlit")
    st.markdown("""
    Bem-vindo! Esta aplicacao demonstra o uso de **Streamlit** para:
    
    - Visualizar dados de vendas por setor;
    - Simular uma previsao com base em investimento;
    - Publicar o app via GitHub e Streamlit Cloud.
    
    Use o menu a esquerda para navegar entre as secoes.
    """)

# Pagina Visualizar Dados
elif menu == "Visualizar Dados":
    st.title("Visualizacao de Dados de Vendas")
    df = carregar_dados()

    if df.empty:
        st.warning("Arquivo 'vendas.csv' nao encontrado.")
    else:
        setor = st.selectbox("Filtrar por setor:", df["setor"].unique())
        df_setor = df[df["setor"] == setor]

        print(df_setor)

        st.dataframe(df_setor)

        print(df_setor.keys())

        # Grafico
        fig, ax = plt.subplots()
        ax.plot(df_setor["mes"], df_setor["vendas"], marker="o", linestyle="-", color="blue")
        ax.set_title(f"Evolucao de Vendas - {setor}")
        ax.set_xlabel("Mes")
        ax.set_ylabel("Vendas (R$)")
        st.pyplot(fig)

# Pagina Previsao
elif menu == "Previsao":
    st.title("Simulador de Previsao de Vendas")

    col1, col2 = st.columns(2)

    with col1:
        setor = st.selectbox("Setor", ["Tecnologia", "Varejo", "Saude"])
        trimestre = st.radio("Trimestre", ["Q1", "Q2", "Q3", "Q4"])
    
    with col2:
        investimento = st.slider("Investimento em Marketing (R$ mil)", 0, 200, 50)
        taxa_crescimento = st.slider("Taxa de Crescimento Esperada (%)", 0, 100, 20)

    if st.button("Prever Vendas"):
        base = 1000
        fatores_setor = {"Tecnologia": 1.2, "Varejo": 1.0, "Saude": 0.9}
        fatores_trim = {"Q1": 1.1, "Q2": 1.0, "Q3": 0.95, "Q4": 1.3}

        fator = fatores_setor[setor] * fatores_trim[trimestre]
        previsao = base * fator + investimento * 10 + (taxa_crescimento / 100) * 1000

        st.success(f"Previsao estimada de vendas: R$ {previsao:,.2f}")

# Pagina Sobre
elif menu == "Sobre":
    st.title("Sobre o Projeto")
    st.markdown("""
    Esta aplicacao foi desenvolvida como exemplo de uso do **Streamlit** para dashboards empresariais.

    **Funcionalidades**:
    - Menu lateral com `streamlit_option_menu`;
    - Leitura de dados CSV com `pandas`;
    - Graficos com `matplotlib`;
    - Simulador de previsao ajustavel;
    - Publicacao via GitHub + Streamlit Cloud.

    **Autor:** Nilson Moreira 
    """)

import streamlit as st
import pandas as pd

from recursos.funcoes import ler_bancodedados

st.set_page_config(
    layout="wide",
    page_title="Ciencia de Dados",
    initial_sidebar_state="expanded"
)

ler_bancodedados()

pages = {
    'CIENCIA DE DADOS': [],
    'Tabela de Dados': [
        st.Page(
            page="tabela/dadosoriginais.py",
            title="Dados Originais",
            icon=":material/table:"
        ),
    ],
    'Estatística - Univariada': [
        st.Page(
            page="estatistica/univariada/curvaabc.py",
            title="Curva ABC",
            icon=":material/leaderboard:"
        ),
        st.Page(
            page="estatistica/univariada/classes.py",
            title="Classes",
            icon=":material/equalizer:"
        ),
        st.Page(
            page="estatistica/univariada/anova.py",
            title="Análise de Variancia (ANOVA)",
            icon=":material/candlestick_chart:"
        ),
    ],
    'Estatística - Multivariada': [
        st.Page(
            page="estatistica/multivariada/correlacao.py",
            title="Correlação",
            icon=":material/pivot_table_chart:"
        ),
        st.Page(
            page="estatistica/multivariada/regressaolinear.py",
            title="Regressão Linear Simples",
            icon=":material/show_chart:"
        ),
        st.Page(
            page="estatistica/multivariada/vif.py",
            title="Fator de Variação de Inflação",
            icon=":material/table_chart:"
        ),
        st.Page(
            page="estatistica/multivariada/desviopadrao.py",
            title="Ranking (Desvio-Padrão)",
            icon=":material/monitoring:"
        ),
    ],
    'Aprendizado de Máquina - Não Supervisionado': [
        st.Page(
            page="aprendizadodemaquina/naosupervisionado/cluster.py",
            title="Agrupamento (Cluster)",
            icon=":material/donut_small:"
        ),
        st.Page(
            page="aprendizadodemaquina/naosupervisionado/pca.py",
            title="Escalonamento Multidimensional (PCA)",
            icon=":material/scatter_plot:"
        ),
        st.Page(
            page="aprendizadodemaquina/naosupervisionado/anomalias.py",
            title="Detecção de Anomalias (Outliers)",
            icon=":material/troubleshoot:"
        ),
        st.Page(
            page="aprendizadodemaquina/naosupervisionado/knn.py",
            title="Vizinhos mais próximos (KNN)",
            icon=":material/bubble_chart:"
        ),
    ],
    'Aprendizado de Máquina - Supervisionado': [
        st.Page(
            page="aprendizadodemaquina/supervisionado/classificacao.py",
            title="Classificação",
            icon=":material/analytics:"
        ),
        st.Page(
            page="aprendizadodemaquina/supervisionado/regressao.py",
            title="Regressão",
            icon=":material/chart_data:"
        ),

    ],
    'Projeto de Ciencia de Dados': [

    ]
}

pg = st.navigation(
    pages,
    expanded=True
)
pg.run()




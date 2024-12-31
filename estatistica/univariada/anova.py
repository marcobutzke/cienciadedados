import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
from itertools import combinations
from statsmodels.stats.multicomp import pairwise_tukeyhsd
from streamlit_extras.tags import tagger_component

def analise_variancia(df, var):
    tukey = pairwise_tukeyhsd(
        endog=df[var], groups=df['Região'], alpha=0.05
    )
    tuk = []
    combinacao = combinations(tukey.groupsunique,2)
    for grupo in list(combinacao):
        tuk.insert(len(tuk), [grupo[0],grupo[1]])
    tuk = pd.DataFrame(tuk, columns=['grupo1', 'grupo2'])
    tuk['diferenca'] = tukey.reject
    tuk['valor'] = tukey.meandiffs
    return tuk


tagger_component(
    content='',
    tags=[
        'Ciencia de Dados',
        'Estatística',
        'Univariada',
        'Análise de Variancia (ANOVA)'
    ],
    color_name=['blue', 'green', 'gray', 'lightgray']
)
variavel = st.segmented_control(
    label='Selecione a Coluna',
    options=st.secrets.continuas,
    selection_mode='single'
)
if variavel is not None:
    col1, col2 = st.columns([1 ,2])
    regioes_diferentes = analise_variancia(
        st.session_state['estados'],
        variavel
    )
    if col1.toggle('Mostrar todas as regiões'):
        col1.dataframe(
            regioes_diferentes,
            hide_index=True,
            use_container_width=True
        )
    else:
        col1.dataframe(
            regioes_diferentes[regioes_diferentes['diferenca'] == 1],
            hide_index=True,
            use_container_width=True
        )
    col2.plotly_chart(
        px.box(
            st.session_state['estados'],
            x="Região",
            y=variavel
        )
    )
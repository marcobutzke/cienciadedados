import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
from streamlit_extras.tags import tagger_component
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler

tagger_component(
    content='',
    tags=[
        'Ciencia de Dados',
        'Aprendizado de Máquina',
        'Supervisionado',
        'Regressão'
    ],
    color_name=['blue', 'green', 'gray', 'lightgray']
)
colunas = st.segmented_control(
    label='Selecione as Colunas',
    options=st.secrets.continuas,
    selection_mode='multi'
)
dependente = st.segmented_control(
    label='Selecione a Coluna Dependente',
    options=st.secrets.continuas,
    selection_mode='single'
)
if (len(colunas) > 2) & (dependente is not None) & (dependente not in colunas):
    regrestados = st.session_state['estados'][colunas + [dependente]].copy()
    X_Train = regrestados.drop(columns=[dependente], axis=1)
    X_Test = regrestados.drop(columns=[dependente], axis=1)
    y_Train = regrestados[dependente]
    y_Test = regrestados[dependente]
    rf = RandomForestRegressor(n_estimators=100, random_state=42)
    rf.fit(X_Train, y_Train)
    previsao = rf.predict(X_Test)
    regrestados['Previsão'] = previsao
    regrestados = pd.merge(
        st.session_state['estados'][st.secrets.descritivas],
        regrestados,
        left_index=True,
        right_index=True
    )
    regrestados['Diferença'] = regrestados[dependente] - regrestados['Previsão']
    st.dataframe(
        regrestados,
        hide_index=True,
        use_container_width=True,
        height=1000
    )

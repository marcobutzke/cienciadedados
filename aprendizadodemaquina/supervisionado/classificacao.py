import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
from streamlit_extras.tags import tagger_component
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler

tagger_component(
    content='',
    tags=[
        'Ciencia de Dados',
        'Aprendizado de Máquina',
        'Supervisionado',
        'Classificação'
    ],
    color_name=['blue', 'green', 'gray', 'lightgray']
)
colunas = st.segmented_control(
    label='Selecione as Colunas',
    options=st.secrets.continuas,
    selection_mode='multi'
)
if len(colunas) > 2:
    estados = st.session_state['estados'].copy()
    estados['Dep'] = estados['Região'].apply(
        lambda x: 1 if x == 'Norte' else (
            2 if x == 'Nordeste' else (
                3 if x == 'Sudeste' else (
                    4 if x == 'Sul' else 5
                )
            )
        )
    )
    clasestados = estados[['Dep'] + colunas].copy()
    X_Train = clasestados.drop(columns=['Dep'], axis=1)
    X_Test = clasestados.drop(columns=['Dep'], axis=1)
    y_Train = clasestados['Dep']
    y_Test = clasestados['Dep']
    X_Train = StandardScaler().fit_transform(X_Train)
    X_Test = StandardScaler().fit_transform(X_Test)
    logreg = LogisticRegression(solver="lbfgs", max_iter=500)
    logreg.fit(X_Train, y_Train)
    pred_logreg = logreg.predict(X_Test)
    pred_proba = logreg.predict_proba(X_Test)
    clasestados["Previsão"] = pred_logreg
    clasestados['Região Previsão'] = clasestados['Previsão'].apply(
        lambda x: 'Norte' if x == 1 else (
            'Nordeste' if x == 2 else (
                'Sudeste' if x == 3 else (
                    'Sul' if x == 4 else 'Centro Oeste')))
    )
    clasestados = pd.merge(
        estados[st.secrets.descritivas],
        clasestados,
        left_index=True,
        right_index=True
    )
    probabilidades = pd.DataFrame()
    index = 0
    for proba in pred_proba.tolist():
        for i in range(0, len(proba)):
            probabilidades = pd.concat(
                [
                    probabilidades,
                    pd.DataFrame(
                        data=[[index, i, round(proba[i], 4)]],
                        columns=[
                            'index',
                            'regiao',
                            'probabilidade'
                        ]
                    )
                ]
            )
        index += 1
    probabilidades = probabilidades.pivot_table(
        index="index",
        columns="regiao",
        values="probabilidade",
        aggfunc="sum"
    ).reset_index()
    probabilidades = probabilidades.set_index("index")
    probabilidades.columns = ['Norte', 'Nordeste', 'Sudeste', 'Sul', 'Centro Oeste']
    clasestados = pd.merge(
        clasestados,
        probabilidades,
        left_index=True,
        right_index=True
    )
    if st.toggle('Todos os estados'):
        st.dataframe(
            clasestados,
            hide_index=True,
            use_container_width=True,
            height=1000
        )
    else:
        st.dataframe(
            clasestados[clasestados['Região'] != clasestados['Região Previsão']],
            hide_index=True,
            use_container_width=True
        )

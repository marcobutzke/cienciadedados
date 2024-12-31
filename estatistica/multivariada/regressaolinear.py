import pandas as pd
import numpy as np
import streamlit as st
import seaborn as sns
from streamlit_extras.tags import tagger_component
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression

tagger_component(
    content='',
    tags=[
        'Ciencia de Dados',
        'Estatística',
        'Multivarada',
        'Regressão Linear'
    ],
    color_name=['blue', 'green', 'gray', 'lightgray']
)
varx = st.segmented_control(
    label='Selecione o Eixo X',
    options=st.secrets.continuas,
    selection_mode='single',
    key='varx'
)
vary = st.segmented_control(
    label='Selecione o Eixo Y',
    options=st.secrets.continuas,
    selection_mode='single',
    key='vary'
)
if (varx is not None) & (vary is not None) & (varx != vary):
    X = np.array(st.session_state['estados'][varx]).reshape(-1, 1)
    y = np.array(st.session_state['estados'][vary]).reshape(-1, 1)
    reg = LinearRegression().fit(X, y)
    cols = st.columns([1,1,3])
    cols[0].metric(
        label='Valor do Intercepto',
        value=round(reg.intercept_[0],4),
        border=True,
    )
    cols[1].metric(
        label='Valor do Coeficiente',
        value=round(reg.coef_[0][0],4),
        border=True,
    )
    cols[2].pyplot(
        sns.regplot(
            data=st.session_state['estados'],
            x=varx,
            y=vary
        ).get_figure()
    )

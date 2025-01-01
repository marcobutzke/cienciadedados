import pandas as pd
import streamlit as st
from streamlit_extras.tags import tagger_component
from statsmodels.stats.outliers_influence import variance_inflation_factor


def varianceinflationfactor(df, colunas):
    df = df[colunas]
    vif = pd.DataFrame()
    vif["variavel"] = df.columns
    vif["VIF"] = [variance_inflation_factor(df.values, i) for i in range(len(df.columns))]
    return vif


def highlight_class_vif(s):
    if s.VIF > 20:
        return ['background-color: #f8c291']*len(s)
    else:
        return ['background-color: #b8e994']*len(s)


tagger_component(
    content='',
    tags=[
        'Ciencia de Dados',
        'Estatística',
        'Multivarada',
        'Fator de Variação de Inflação'
    ],
    color_name=['blue', 'green', 'gray', 'lightgray']
)
colunas = st.segmented_control(
    label='Selecione as Colunas',
    options=st.secrets.continuas,
    selection_mode='multi'
)
if len(colunas) > 2:
    cols = st.columns([1,3])
    st.dataframe(
        varianceinflationfactor(
            df=st.session_state['estados'],
            colunas=colunas
        ).style.apply(
            highlight_class_vif,
            axis=1
        ),
        hide_index=True,
        use_container_width=True
    )

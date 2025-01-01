import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import altair as alt
from streamlit_extras.tags import tagger_component


def classificacao_valores_padronizados(data):
    dataz = pd.DataFrame()
    for col in data.columns:
        media = data[col].mean()
        dp = data[col].std()
        dataz[col] = data[col].apply(lambda x: (x - media) / dp)
    dataz['total'] = dataz.sum(
        axis=1,
        skipna=True
    )
    dataz['ranking'] = dataz['total'].rank(ascending=False)
    iqr = dataz['total'].quantile(0.75) - dataz['total'].quantile(0.25)
    out_min = dataz['total'].quantile(0.25) - (1.5 * iqr)
    out_max = dataz['total'].quantile(0.75) + (1.5 * iqr)
    erro = 1.96 * dataz['total'].std() / np.sqrt(len(data))
    li = dataz['total'].mean() - erro
    ls = dataz['total'].mean() + erro
    dataz['zscore'] = (dataz['total'] - dataz['total'].mean()) / dataz['total'].std()
    dataz['stars'] = round(dataz['zscore'], 0) + 3
    dataz['outlier_min'] = dataz['total'].apply(
        lambda x: 1 if x < out_min
        else 0
    )
    dataz['outlier_max'] = dataz['total'].apply(
        lambda x: 1 if x > out_max
        else 0
    )
    media = dataz['total'].mean()
    dataz['class_media'] = dataz['total'].apply(
        lambda x: 'abaixo' if x < media
        else 'acima'
    )
    dataz['class_lc'] = dataz['total'].apply(
        lambda x: 'abaixo' if x < li
        else (
            'acima' if x > ls
            else 'media'
        )
    )
    datac = st.session_state['estados'][st.secrets.descritivas].copy()
    datac = datac.merge(dataz, left_index=True, right_index=True)
    data_sort = datac.sort_values(by='ranking')
    return data_sort


def cor_classe(s):
    if s.outlier_max == 1:
        return ['background-color: #82ccdd']*len(s)
    elif s.class_lc == 'acima':
        return ['background-color: #b8e994']*len(s)
    elif s.class_lc == 'media':
        return ['background-color: #fad390']*len(s)
    else:
        return ['background-color: #f8c291']*len(s)


tagger_component(
    content='',
    tags=[
        'Ciencia de Dados',
        'Estatística',
        'Multivarada',
        'Ranking (padronização)'
    ],
    color_name=['blue', 'green', 'gray', 'lightgray']
)
colunas = st.segmented_control(
    label='Selecione as Colunas',
    options=st.secrets.continuas,
    selection_mode='multi'
)
if len(colunas) > 2:
    tabs = st.tabs(['Tabela', 'Gráfico'])
    with tabs[0]:
        st.dataframe(
            classificacao_valores_padronizados(
                st.session_state['estados'][colunas]
            ).style.apply(cor_classe, axis=1),
            use_container_width=True,
            hide_index=True,
            height=1000
        )
    with tabs[1]:
        st.plotly_chart(
            px.bar(
                classificacao_valores_padronizados(
                    st.session_state['estados'][colunas]
                ),
                x=st.secrets.descritivas[0],
                y=colunas,
                color_discrete_sequence=px.colors.qualitative.Antique
            )
        )

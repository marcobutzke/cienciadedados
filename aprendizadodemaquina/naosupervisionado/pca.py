import pandas as pd
import numpy as np
import streamlit as st
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.decomposition import PCA
import altair as alt
from streamlit_extras.tags import tagger_component


def silhouette(df):
    silhouette_scores = []
    for k in range(3, 10):
        kmeans = KMeans(n_clusters=k, random_state=42)
        kmeans.fit(df)
        score = silhouette_score(df, kmeans.labels_)
        silhouette_scores.append(score)
    return  silhouette_scores.index(max(silhouette_scores)) + 3


tagger_component(
    content='',
    tags=[
        'Ciencia de Dados',
        'Aprendizado de Máquina',
        'Não-supervisionado',
        'Escalonamento Multidimensional (PCA)'
    ],
    color_name=['blue', 'green', 'gray', 'lightgray']
)
colunas = st.segmented_control(
    label='Selecione as Colunas',
    options=st.secrets.continuas,
    selection_mode='multi'
)
if len(colunas) > 2:
    pca = PCA(
        n_components=2
    ).fit(
        st.session_state['estados'][colunas]
    ).transform(
        st.session_state['estados'][colunas]
    )
    estados_pca = st.session_state['estados'][st.secrets.descritivas + colunas].copy()
    estados_pca['escalaX'] = pca[:, 0]
    estados_pca['escalaY'] = pca[:, 1]
    kmeans = KMeans(
        n_clusters=silhouette(st.session_state['estados'][colunas]),
        random_state=0
    ).fit(st.session_state['estados'][colunas])
    estados_pca['cluster'] = kmeans.labels_.astype(str)
    ed = alt.Chart(estados_pca).mark_circle(size=100).encode(
        alt.X(
            shorthand='escalaX',
            scale=alt.Scale(zero=False)
        ),
        alt.Y(
            shorthand='escalaY',
            scale=alt.Scale(zero=False, padding=1)
        ),
        color='cluster:N',
    ).encode(
        tooltip=[
            'Estado',
            'Sigla'
        ]
    ).properties(
        width=1200,
        height=800
    )
    tx = alt.Chart(estados_pca).mark_text(dy=-10).encode(
        alt.X(
            shorthand='escalaX',
            scale=alt.Scale(zero=False)
        ),
        alt.Y(
            shorthand='escalaY',
            scale=alt.Scale(zero=False, padding=1)
        ),
        text='Estado'
    ).encode(
        tooltip=[
            'Estado',
            'Sigla'
        ]
    ).properties(
        width=1200,
        height=800
    )
    st.altair_chart(ed + tx)

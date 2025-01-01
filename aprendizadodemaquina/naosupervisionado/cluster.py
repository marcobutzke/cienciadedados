import pandas as pd
import numpy as np
import streamlit as st
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import plotly.express as px
import plotly.graph_objects as go
from streamlit_extras.tags import tagger_component


def silhouette(df):
    silhouette_scores = []
    for k in range(3, 10):
        kmeans = KMeans(n_clusters=k, random_state=42)
        kmeans.fit(df)
        score = silhouette_score(df, kmeans.labels_)
        silhouette_scores.append(score)
    return  silhouette_scores.index(max(silhouette_scores)) + 3


def cor_cluster(s):
    return [f'background-color: {px.colors.qualitative.Pastel2[int(s['cluster'])]}'] * len(s)


tagger_component(
    content='',
    tags=[
        'Ciencia de Dados',
        'Aprendizado de Máquina',
        'Não-supervisionado',
        'Agrupamento (Cluster)'
    ],
    color_name=['blue', 'green', 'gray', 'lightgray']
)
colunas = st.segmented_control(
    label='Selecione as Colunas',
    options=st.secrets.continuas,
    selection_mode='multi'
)
if len(colunas) > 2:
    estados_clusters = st.session_state['estados'][
        st.secrets.descritivas + colunas
    ].set_index(
        st.secrets.descritivas
    )
    kmeans = KMeans(
        n_clusters=silhouette(estados_clusters),
        random_state=0
    ).fit(estados_clusters)
    estados_clusters['cluster'] = kmeans.labels_.astype(str)
    estados_clusters = estados_clusters.reset_index()
    cluster_centers = pd.DataFrame(kmeans.cluster_centers_).reset_index()
    cluster_centers.columns = ['cluster'] + colunas
    st.write('Centróides')
    st.dataframe(
        cluster_centers.style.apply(cor_cluster, axis=1),
        hide_index=True,
        use_container_width=True
    )
    tabs = st.tabs(['Tabela', 'Mapa'])
    with tabs[0]:
        st.dataframe(
            estados_clusters.style.apply(
                cor_cluster,
                axis=1
            ),
            hide_index=True,
            use_container_width=True,
            height=1000
        )
    with tabs[1]:
        mapa_px = px.choropleth_mapbox(
            data_frame=estados_clusters,
            geojson=st.session_state['geo'],
            locations='Sigla',
            featureidkey='properties.sigla',
            color='cluster',
            color_discrete_sequence=px.colors.qualitative.Pastel2,
            mapbox_style='carto-positron',
            zoom=2.5,
            center={
                "lat": -15.76,
                "lon": -47.88
            },
            opacity=1,
            width=640,
            height=480,
        )
        mapa_px.update_layout(margin={'r': 0, 't': 0, 'l': 0, 'b': 0})
        mapa_px.update_traces(marker_line_width=1)
        st.plotly_chart(mapa_px)


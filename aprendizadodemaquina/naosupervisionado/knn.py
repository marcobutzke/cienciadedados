import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
from streamlit_extras.tags import tagger_component
from pyod.models.knn import KNN
from sklearn.neighbors import NearestNeighbors

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
estado = st.segmented_control(
    label='Selecione a Estado',
    options=st.session_state['estados']['Sigla'],
    selection_mode='single'
)
if len(colunas) > 2 and estado is not None:
    estado_vmp = st.session_state['estados'][
        st.session_state['estados']['Sigla'] == estado
    ][colunas]
    estados_vmp = st.session_state['estados'][colunas]
    neighbors_alg = NearestNeighbors(
        n_neighbors=min(
            6,
            len(estados_vmp)
        )
    ).fit(estados_vmp)
    similar = neighbors_alg.kneighbors(
        estado_vmp,
        return_distance=False
    )[0]
    estados_similares = list(st.session_state['estados'].iloc[similar]['Sigla'])
    estados_knn = st.session_state['estados'][st.secrets.descritivas + colunas].copy()
    estados_knn['Similar'] = estados_knn.apply(
        lambda x: '1' if x['Sigla'] in estados_similares else '0',
        axis=1
    )
    st.dataframe(
        estados_knn[estados_knn['Similar'] == '1'],
        hide_index=True,
        use_container_width=True
    )
    similar_cores = {
        '0': 'white',
        '1': 'blue'
    }
    mapa_px = px.choropleth_mapbox(
        data_frame=estados_knn,
        geojson=st.session_state['geo'],
        locations='Sigla',
        featureidkey='properties.sigla',
        color='Similar',
        color_discrete_map=similar_cores,
        mapbox_style='carto-positron',
        zoom=2.5,
        center={"lat": -15.76, "lon": -47.88},
        opacity=1, width=640, height=480,
    )
    mapa_px.update_layout(margin={'r': 0, 't': 0, 'l': 0, 'b': 0})
    mapa_px.update_traces(marker_line_width=1)
    st.plotly_chart(mapa_px)

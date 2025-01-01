import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
from streamlit_extras.tags import tagger_component
from pyod.models.knn import KNN
from sklearn.preprocessing import StandardScaler

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
    clf = KNN().fit(
        StandardScaler().fit_transform(
            st.session_state['estados'][colunas]
        )
    )
    estados_anm = st.session_state['estados'][st.secrets.descritivas + colunas].copy()
    estados_anm['Outlier'] = clf.predict(
        StandardScaler().fit_transform(
            st.session_state['estados'][colunas]
        )
    ).astype(str)
    st.dataframe(
        estados_anm[estados_anm['Outlier'] == '1'],
        hide_index=True,
        use_container_width=True
    )
    outliers_cores = {
        '0': 'white',
        '1': 'blue'
    }
    mapa_px = px.choropleth_mapbox(
        data_frame=estados_anm,
        geojson=st.session_state['geo'],
        locations='Sigla',
        featureidkey='properties.sigla',
        color='Outlier',
        color_discrete_map=outliers_cores,
        mapbox_style='carto-positron',
        zoom=2.5,
        center={"lat": -15.76, "lon": -47.88},
        opacity=1, width=640, height=480,
    )
    mapa_px.update_layout(margin={'r': 0, 't': 0, 'l': 0, 'b': 0})
    mapa_px.update_traces(marker_line_width=1)
    st.plotly_chart(mapa_px)

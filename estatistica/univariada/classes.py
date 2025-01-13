import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import altair as alt
from streamlit_extras.tags import tagger_component

def classificacao_estados_variavel(bra_var, variavel):
    iqr = bra_var[variavel].quantile(0.75) - bra_var[variavel].quantile(0.25)
    out_min = bra_var[variavel].quantile(0.25) - (1.5 * iqr)
    out_max = bra_var[variavel].quantile(0.75) + (1.5 * iqr)
    limite_inferior = bra_var[variavel].mean() - (1.96 * bra_var[variavel].std() / np.sqrt(len(bra_var)))
    limite_superior = bra_var[variavel].mean() + (1.96 * bra_var[variavel].std() / np.sqrt(len(bra_var)))
    bra_var['outlier_min'] = bra_var[variavel].apply(lambda x : 1 if x < out_min else 0)
    bra_var['outlier_max'] = bra_var[variavel].apply(lambda x : 1 if x > out_max else 0)
    bra_var['class_lc'] = bra_var[variavel].apply(
        lambda x : 'abaixo'
        if x < limite_inferior
        else (
            'acima'
            if x > limite_superior
            else 'media'
        )
    )
    return bra_var


def cor_classe(s):
    if s.outlier_max == 1:
        return ['background-color: #6a89cc']*len(s)
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
        'Univariada',
        'Classe e Outliers'
    ],
    color_name=['blue', 'green', 'gray', 'lightgray']
)
variavel = st.segmented_control(
    label='Selecione a Coluna',
    options=st.secrets.continuas,
    selection_mode='single'
)
if variavel is not None:
    estados_cla = classificacao_estados_variavel(
        st.session_state['estados'][st.secrets.descritivas + [variavel]].copy(),
        variavel
    )
    tabl, mapa, graf = st.tabs(['Tabela', 'Mapas', 'Gráfico'])
    with tabl:
        st.dataframe(
            estados_cla.style.apply(cor_classe, axis=1),
            hide_index=True,
            height=1000,
            use_container_width=True
        )
    with mapa:
        cl1, cl2 = st.columns(2)
        minimo = st.session_state['estados'][variavel].min()
        maximo = st.session_state['estados'][variavel].max()
        mapa_px = px.choropleth_mapbox(
            data_frame=st.session_state['estados'],
            geojson=st.session_state['geo'],
            locations='Sigla',
            featureidkey='properties.sigla',
            color=variavel,
            color_continuous_scale='blues',
            range_color=(minimo, maximo),
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
        cl1.plotly_chart(mapa_px)
        classe_cores = {
            'acima': '#b8e994',
            'media': '#fad390',
            'abaixo': '#f8c291'
        }
        mapa_px = px.choropleth_mapbox(
            data_frame=estados_cla,
            geojson=st.session_state['geo'],
            locations='Sigla',
            featureidkey='properties.sigla',
            color='class_lc',
            color_discrete_map=classe_cores,
            mapbox_style='carto-positron',
            zoom=2.5,
            center={"lat": -15.76, "lon": -47.88},
            opacity=1, width=640, height=480,
        )
        mapa_px.update_layout(margin={'r': 0, 't': 0, 'l': 0, 'b': 0})
        mapa_px.update_traces(marker_line_width=1)
        evento = cl2.plotly_chart(mapa_px, on_select='rerun')
        if len(evento['selection']['points']) > 0:
            st.write(evento['selection'])
    with graf:
        st.altair_chart(
            alt.Chart(estados_cla).mark_bar().encode(
                x="Estado:O",
                y=variavel + ':Q',
                color='class_lc:N'
            ).properties(
                height=600,
                width=1200
            )
        )

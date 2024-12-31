import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import altair as alt
from streamlit_extras.tags import tagger_component

def classificacao_abc_variavel(abc, variavel):
    abc['percentual'] = abc[variavel] / abc[variavel].sum()
    abc_sort = abc.sort_values(by=variavel, ascending=False).copy()
    abc_sort['percentual_acumulado'] = abc_sort['percentual'].cumsum()
    abc_sort['acumulado'] = abc_sort[variavel].cumsum()
    abc_sort['classe'] = abc_sort['percentual_acumulado'].apply(
        lambda x : 'A' if x <= 0.65 else (
            'B' if x <= 0.90 else 'C'
        )
    )
    return abc_sort

def cor_abc(s):
    if s.classe == 'A':
        return ['background-color: #00cc96']*len(s)
    elif s.classe == 'B':
        return ['background-color: #fecb52']*len(s)
    else:
        return ['background-color: #ef553b']*len(s)


tagger_component(
    content='',
    tags=[
        'Ciencia de Dados',
        'Estatística',
        'Univariada',
        'Análise de Variancia (ANOVA)'
    ],
    color_name=['blue', 'green', 'gray', 'lightgray']
)
variavel = st.segmented_control(
    label='Selecione a Coluna',
    options=st.secrets.continuas,
    selection_mode='single'
)
if variavel is not None:
    estados_abc = classificacao_abc_variavel(
        st.session_state['estados'][st.secrets.descritivas + [variavel]].copy(),
        variavel
    )
    tabs = st.tabs(['Tabela', 'Mapa', 'Gráfico'])
    with tabs[0]:
        st.dataframe(
            estados_abc.style.apply(cor_abc, axis=1),
            hide_index=True,
            height=1000,
            use_container_width=True
        )
    with tabs[1]:
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
                "lon": -47.88},
            opacity=1,
            width=640,
            height=480,
        )
        mapa_px.update_layout(margin={'r': 0, 't': 0, 'l': 0, 'b': 0})
        mapa_px.update_traces(marker_line_width=1)
        cl1, cl2 = st.columns(2)
        cl1.plotly_chart(mapa_px)
        abc_cores = {'A': '#00cc96', 'B': '#fecb52', 'C': '#ef553b'}
        mapa_px = px.choropleth_mapbox(
            data_frame=estados_abc,
            geojson=st.session_state['geo'],
            locations='Sigla',
            featureidkey='properties.sigla',
            color='classe',
            color_discrete_map=abc_cores,
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
        cl2.plotly_chart(mapa_px)
    with tabs[2]:
        sort_order = estados_abc["Estado"].tolist()
        base = alt.Chart(estados_abc).encode(
            x=alt.X("Estado:O", sort=sort_order),
        ).properties(width=1200, height=600)
        bars = base.mark_bar(size=15).encode(
            y=alt.Y(variavel + ':Q'), color='classe:N'
        ).properties(width=1200, height=600)
        line = base.mark_line(strokeWidth=1.5, color="#cb4154").encode(
            y=alt.Y('percentual_acumulado:Q', title='valores acumulados', axis=alt.Axis(format=".0%")),
            text=alt.Text('percentual_acumulado:Q'))
        points = base.mark_circle(strokeWidth=3, color="#cb4154").encode(
            y=alt.Y('percentual_acumulado:Q', axis=None))
        point_text = points.mark_text(align='left', baseline='middle', dx=-10, dy=-10).encode(
            y=alt.Y('percentual_acumulado:Q', axis=None), text=alt.Text('percentual_acumulado:Q', format="0.0%"),
            color=alt.value("#cb4154"))
        st.altair_chart((bars + line + points + point_text).resolve_scale(y='independent'))

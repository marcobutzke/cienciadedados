import datetime as dt
import itertools
import pandas as pd
import geopandas as gpd
import numpy as np
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from streamlit_extras.tags import tagger_component
from streamlit_extras.metric_cards import style_metric_cards
import json


from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from statsmodels.stats.outliers_influence import variance_inflation_factor
from sklearn.cluster import KMeans
from yellowbrick.cluster import KElbowVisualizer
from prophet import Prophet
from pmdarima.arima import auto_arima


style_metric_cards(
    border_left_color="gray",
    background_color="white",
    border_size_px=2,
    border_color="gray",
    border_radius_px=10,
    box_shadow=True
)

@st.cache_data
def load_world_data():
    return json.load(
        open(
            st.secrets.world
        )
    )


def rfm(df):
    today_date = df["Order Date"].max()
    return df.groupby('Country').agg(
        {
            'Order Date': lambda date: (today_date - date.max()).days,
            'Order ID': lambda num: num.nunique(),
            'Profit': lambda lucro: lucro.sum(),
            'Sales': lambda vendas: vendas.sum(),
        }
    )


def regressaolinear(df):
    regressao = []
    for index, row in df.iterrows():
        X = np.array(list(range(1,13))).reshape(-1, 1)
        y = np.array(list(row)).reshape(-1, 1)
        reg = LinearRegression().fit(X, y)
        regressao.insert(
            len(regressao),
            [
                index,
                round(reg.intercept_[0],4),
                round(reg.coef_[0][0],4)
            ]
        )
    regressao = pd.DataFrame(
        regressao,
        columns = [
            'Country',
            'intercepto',
            'coeficiente'
        ]
    ).set_index('Country')
    return regressao


def varianceinflationfactor(df, colunas):
    df = df[colunas]
    vif = pd.DataFrame()
    vif["variavel"] = df.columns
    vif["VIF"] = [variance_inflation_factor(df.values, i) for i in range(len(df.columns))]
    return vif


def colunas_modelo(df, variaveis):
    combinacoes = []
    colunas = []
    for i in range(len(variaveis)):
        combinacoes += itertools.combinations(variaveis, i + 1)
    for combinacao in [list(t) for t in combinacoes]:
        if len(combinacao) > 3:
            vif = varianceinflationfactor(
                df=df,
                colunas=combinacao
            )
            if vif['VIF'].mean() <= 20:
                colunas = combinacao
    return colunas


def numero_cluster(df):
    model = KMeans()
    visualizer = KElbowVisualizer(
        model,
        k=(4, 12)
    )
    visualizer.fit(df)
    return visualizer.elbow_value_



tagger_component(
    content='',
    tags=[
        'Ciencia de Dados',
        'Projeto',
        'Dashboard',
    ],
    color_name=['blue', 'green', 'lightgray']
)
if 'status' not in st.session_state:
    st.session_state['status'] = 0
if st.session_state['status'] == 0:
    with st.status('Pipeline - Cluster', expanded=True) as status:
        st.write('RFM Analisys')
        st.session_state['ecommerce']['mes'] = st.session_state['ecommerce']['Order Date'].dt.month
        st.session_state['cluster'] = rfm(st.session_state['ecommerce'])
        st.session_state['mensal'] = st.session_state['ecommerce'].pivot_table(
            index='Country',
            columns='mes',
            values='Sales',
            aggfunc='sum',
            fill_value=0
        )
        st.write('Regressao Linear')
        st.session_state['cluster'] = pd.merge(
            left=st.session_state['cluster'],
            right=regressaolinear(st.session_state['mensal']),
            left_index=True,
            right_index=True
        )
        st.write('Médias')
        st.session_state['cluster'] = pd.merge(
            left=st.session_state['cluster'],
            right=st.session_state['ecommerce'].groupby('Country')['Aging'].mean(),
            left_index=True,
            right_index=True
        )
        st.session_state['cluster'].columns = [
            'dias',
            'quantidade',
            'venda',
            'lucro',
            'intercepto',
            'coeficiente',
            'entrega'
        ]
        st.write('VIF - Choose columns')
        colunas = colunas_modelo(
            st.session_state['cluster'],
            st.session_state['cluster'].columns
        )
        st.session_state['cluster_colunas'] = st.session_state['cluster'][colunas].copy()
        st.write('Cluster Model')
        kmeans = KMeans(
            n_clusters=numero_cluster(st.session_state['cluster_colunas']),
            random_state=0
        ).fit(st.session_state['cluster_colunas'])
        st.session_state['cluster_colunas']['cluster'] = kmeans.labels_.astype(str)
        st.session_state['cluster_colunas'] = st.session_state['cluster_colunas'].reset_index()
        st.session_state['cluster_centers'] = pd.DataFrame(kmeans.cluster_centers_).reset_index()
        st.session_state['cluster_centers'].columns = ['cluster'] + colunas
        st.session_state['cluster']['cluster'] = kmeans.labels_.astype(str)
        status.update(
            label="Process complete!", state="complete", expanded=False
        )
        st.session_state['status'] = 1
        st.rerun()
if st.session_state['status'] == 1:
    pais = None
    cluster = st.session_state['cluster'].reset_index()
    with st.spinner('Construindo o Mapa...'):
        world = load_world_data()
        mapa_px = px.choropleth_mapbox(
            data_frame=cluster,
            geojson=world,
            locations='Country',
            featureidkey='properties.ADMIN',
            color='cluster',
            color_discrete_sequence=px.colors.qualitative.G10,
            mapbox_style='carto-positron',
            zoom=1,
            center={"lat": 0, "lon": 0},
            opacity=1, #width=640, height=480,
        )
        mapa_px.update_layout(margin={'r': 0, 't': 0, 'l': 0, 'b': 0})
        mapa_px.update_traces(marker_line_width=1)
        evento = st.plotly_chart(mapa_px, on_select='rerun')
    if len(evento['selection']['points']) > 0:
        pais = st.session_state['ecommerce'][
            st.session_state['ecommerce']['Country'] == evento['selection']['points'][0]['properties']['ADMIN']
        ]
        dados_pais = cluster[cluster['Country'] == evento['selection']['points'][0]['properties']['ADMIN']].reset_index()
        mensal = st.session_state['mensal'].reset_index()
        mensal_pais = mensal[mensal['Country'] == dados_pais['Country'].values[0]].set_index('Country').T.reset_index()
        mensal_pais.columns = ['mes', 'lucro']
        mensal_pais['tipo'] = 'realizado'
        mensal_pais = pd.concat(
            [
                mensal_pais,
                pd.DataFrame(
                    data=[
                        [
                            m,
                            dados_pais['intercepto'].values[0] + (dados_pais['coeficiente'].values[0]) * m,
                            'projetado'
                        ] for m in range(1, 13)
                    ],
                    columns=['mes', 'lucro', 'tipo']
                )
            ]
        )
        st.subheader(f'Métricas do Cluster {int(dados_pais['cluster'].values[0])}')
        cols = st.columns(len(st.session_state['cluster_centers']) - 3)
        for c in range(0, len(cols)):
            cols[c].metric(
                st.session_state['cluster_centers'].columns[c+1],
                round(
                    st.session_state['cluster_centers'][
                        st.session_state['cluster_centers']['cluster'] == int(dados_pais['cluster'].values[0])
                    ][st.session_state['cluster_centers'].columns[c+1]].values[0],
                    2
                ),
                border=True
            )
        st.header(evento['selection']['points'][0]['properties']['ADMIN'])
        medidas = ['dias', 'quantidade', 'venda', 'lucro', 'intercepto', 'coeficiente', 'entrega']
        cols = st.columns(len(medidas))
        c = 0
        for medida in medidas:
            cols[c].metric(
                label=medida,
                value=round(
                    dados_pais[medida].values[0],
                    2
                ),
                delta=round(
                    cluster[medida].mean(),
                    2
                ),
                border=True
            )
            c += 1
        cols = st.columns([2,1,1])
        with cols[0].container(border=True):
            st.write('Tendencia')
            st.plotly_chart(
                px.line(
                    data_frame=mensal_pais,
                    x='mes',
                    y='lucro',
                    color='tipo',
                    height=600
                )
            )
        c = 1
        for coluna in ['Ship Mode', 'Product Category', 'Order Priority', 'Segment']:
            with cols[c].container(border=True):
                st.write(coluna)
                st.plotly_chart(
                    px.pie(
                        data_frame=pais.groupby(coluna)['Profit'].sum().reset_index(),
                        names=coluna,
                        values='Profit',
                        hole=0.5,
                        height=250
                    )
                )
            if c == 1:
                c = 2
            else:
                c = 1





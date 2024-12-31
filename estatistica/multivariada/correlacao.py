import streamlit as st
import seaborn as sns
from streamlit_extras.tags import tagger_component

tagger_component(
    content='',
    tags=[
        'Ciencia de Dados',
        'Estatística',
        'Multivarada',
        'Correlação'
    ],
    color_name=['blue', 'green', 'gray', 'lightgray']
)
colunas = st.segmented_control(
    label='Selecione as Colunas',
    options=st.secrets.continuas,
    selection_mode='multi'
)
if len(colunas) > 2:
    st.pyplot(
        sns.heatmap(
            data=st.session_state['estados'][colunas].corr(),
            annot=True,
            fmt='.4f'
        ).get_figure()
    )
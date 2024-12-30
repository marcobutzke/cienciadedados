import pandas as pd
import json
import streamlit as st

@st.cache_data
def ler_bancodedados():
    st.session_state['estados'] = pd.read_parquet(
        st.secrets.dados
    )
    st.session_state['geo'] = json.load(
        open(
            st.secrets.mapa
        )
    )
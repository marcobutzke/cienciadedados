import streamlit as st
from great_tables import GT


with st.popover('Variáveis', use_container_width=True):
    colunas = st.pills(
        label='Selecione as Colunas',
        options=st.secrets.continuas,
        selection_mode='multi'
    )

tabs = st.tabs(
    [
        'Dados Originais',
        'Formato Tabela',
        'Tabela por Regiao',
        'Região e Estados'
    ]
)

with tabs[0]:
    st.dataframe(
        st.session_state['estados'][
            st.secrets.descritivas + colunas
        ],
        use_container_width=True,
        hide_index=True,
        height=1000
    )
with tabs[1]:
    if len(colunas) > 0:
        st.html(
            GT(
                st.session_state['estados'][
                    st.secrets.descritivas + colunas
                ]
            ).tab_header(
                title='Estados do Brasil'
            ).tab_source_note(
                source_note='Fonte: IBGE Cidades'
            ).tab_spanner(
                label='Descrição',
                columns=st.secrets.descritivas,
            ).tab_spanner(
                label='Variáves',
                columns=colunas,
            )
        )
with tabs[2]:
    if len(colunas) > 0:
        st.html(
            GT(
                st.session_state['estados'][
                    st.secrets.descritivas + colunas
                ],
                groupname_col='Região'
            ).tab_header(
                title='Estados do Brasil'
            ).tab_source_note(
                source_note='Fonte: IBGE Cidades'
            ).tab_stub(rowname_col='Estado', groupname_col="Região").tab_stubhead(label='Região')
        )

with tabs[3]:
    if st.toggle('Média'):
        regioes = st.session_state['estados'].groupby(st.secrets.descritivas[1])[colunas].mean().reset_index()
    else:
        regioes = st.session_state['estados'].groupby(st.secrets.descritivas[1])[colunas].sum().reset_index()
    evento = st.dataframe(
        data=regioes,
        use_container_width=True,
        hide_index=True,
        selection_mode='single-row',
        on_select='rerun'
    )
    if len(evento['selection']['rows']) > 0:
        st.dataframe(
            st.session_state['estados'][
                st.session_state['estados']['Região'] == regioes[
                    evento['selection']['rows'][0]:evento['selection']['rows'][0] + 1
                ]['Região'].values[0]
            ][
                st.secrets.descritivas + colunas
            ],
            use_container_width=True,
            hide_index=True
        )

from pathlib import Path
import streamlit as st

st.set_page_config(
    page_title="Apresentação | Mobilidade em Dados",
    page_icon="🚌",
    layout="wide",
)

st.caption("TESTE TÉCNICO · ANÁLISE DE DEMANDA NO TRANSPORTE PÚBLICO")
st.title("Mobilidade em dados")

imagem_onibus = Path(__file__).resolve().parent / "assets" / "onibus_integra_ottrans.jpg"
st.image(str(imagem_onibus), width="stretch")
st.caption(
    "Imagem ilustrativa: frota da OT Trans no sistema Integra, em Salvador (BA). "
    "[Fonte: OT Trans](https://ottrans.com.br/"
    "nova-frota-de-onibus-da-ot-trans-amplia-renovacao-do-transporte-publico-de-salvador/)"
)

periodo, fonte, recortes = st.columns(3)

with periodo:
    st.markdown("**Período analisado**")
    st.write("Janeiro e fevereiro de 2022")

with fonte:
    st.markdown("**Fonte dos dados**")
    st.markdown(
        "[Portal Brasileiro de Dados Abertos]"
        "(https://dados.gov.br/dados/conjuntos-dados/demanda)"
    )

with recortes:
    st.markdown("**Recortes da análise**")
    st.write("Datas, linhas e categorias de passageiros")

st.divider()
st.caption("Tecnologias do projeto: Python · pandas · PostgreSQL · Airflow · Docker · Streamlit")

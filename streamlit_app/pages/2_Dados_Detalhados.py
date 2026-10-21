import pandas as pd
import streamlit as st

st.set_page_config(page_title="Dados detalhados", page_icon="📋", layout="wide")

st.title("Dados detalhados")
st.caption("Consulte os registros por mês e por código da linha.")

mes = st.selectbox("Mês", ["Janeiro", "Fevereiro", "Ambos"])

conn = st.connection("postgresql", type="sql")

df_janeiro = conn.query(
    """
    SELECT
        data_movimento_jan AS data_movimento,
        codigo_linha_jan AS codigo_linha,
        nome_linha_jan AS nome_linha,
        tipo_passageiro_jan AS tipo_passageiro,
        nome_passageiro_jan AS nome_passageiro,
        demanda_jan AS demanda
    FROM public.demanda_janeiro_2022
    """,
    ttl="10m",
)

df_fevereiro = conn.query(
    """
    SELECT
        data_movimento_fev AS data_movimento,
        codigo_linha_fev AS codigo_linha,
        nome_linha_fev AS nome_linha,
        tipo_passageiro_fev AS tipo_passageiro,
        nome_passageiro_fev AS nome_passageiro,
        demanda_fev AS demanda
    FROM public.demanda_fevereiro_2022
    """,
    ttl="10m",
)

if mes == "Janeiro":
    df_dados = df_janeiro
elif mes == "Fevereiro":
    df_dados = df_fevereiro
else:
    df_dados = pd.concat([df_janeiro, df_fevereiro], ignore_index=True)

linhas = df_dados["codigo_linha"].dropna().unique().tolist()
linhas.sort()

linha = st.selectbox("Código da linha", ["Todas"] + linhas)

if linha != "Todas":
    df_dados = df_dados[df_dados["codigo_linha"] == linha]

df_dados = df_dados.sort_values(["data_movimento", "codigo_linha"])

df_exibicao = df_dados.copy()
df_exibicao["data_movimento"] = pd.to_datetime(df_exibicao["data_movimento"])
df_exibicao["data_movimento"] = df_exibicao["data_movimento"].dt.strftime("%d/%m/%Y")

df_exibicao.rename(
    columns={
        "data_movimento": "Data",
        "codigo_linha": "Código da linha",
        "nome_linha": "Nome da linha",
        "tipo_passageiro": "Código do tipo de passageiro",
        "nome_passageiro": "Tipo de passageiro",
        "demanda": "Demanda",
    },
    inplace=True,
)

quantidade_registros = f"{len(df_exibicao):,}".replace(",", ".")
st.caption(f"{quantidade_registros} registros encontrados.")

if df_exibicao.empty:
    st.info("Nenhum registro encontrado para os filtros selecionados.")
else:
    st.dataframe(df_exibicao, hide_index=True)

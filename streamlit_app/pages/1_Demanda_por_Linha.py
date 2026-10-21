import pandas as pd
import streamlit as st

st.set_page_config(page_title="Análise da demanda", page_icon="🚌", layout="wide")

st.title("Análise da demanda")
st.caption("Demanda de passageiros por linha · Janeiro e fevereiro de 2022")

mes = st.selectbox("Mês", ["Janeiro", "Fevereiro", "Ambos"])

conn = st.connection("postgresql", type="sql")


df_janeiro = conn.query(
    """
    SELECT
        data_movimento_jan AS data_movimento,
        codigo_linha_jan AS codigo_linha,
        SUM(demanda_jan) AS demanda
    FROM public.demanda_janeiro_2022
    GROUP BY data_movimento_jan, codigo_linha_jan
    """,
    ttl="10m",
)

df_fevereiro = conn.query(
    """
    SELECT
        data_movimento_fev AS data_movimento,
        codigo_linha_fev AS codigo_linha,
        SUM(demanda_fev) AS demanda
    FROM public.demanda_fevereiro_2022
    GROUP BY data_movimento_fev, codigo_linha_fev
    """,
    ttl="10m",
)

if mes == "Janeiro":
    df_demanda = df_janeiro
elif mes == "Fevereiro":
    df_demanda = df_fevereiro
else:
    df_demanda = pd.concat([df_janeiro, df_fevereiro], ignore_index=True)

total_demanda = int(df_demanda["demanda"].sum())
quantidade_linhas = int(df_demanda["codigo_linha"].nunique())
quantidade_dias = int(df_demanda["data_movimento"].nunique())

if quantidade_dias > 0:
    media_diaria = total_demanda / quantidade_dias
else:
    media_diaria = 0

total_formatado = f"{total_demanda:,}".replace(",", ".")
media_formatada = f"{media_diaria:,.0f}".replace(",", ".")

coluna_total, coluna_linhas, coluna_media = st.columns(3)

with coluna_total:
    st.metric("Demanda total", total_formatado, border=True)

with coluna_linhas:
    st.metric(
        "Linhas com registros",
        quantidade_linhas,
        help="Quantidade de códigos de linha distintos no período selecionado.",
        border=True,
    )

with coluna_media:
    st.metric(
        "Média diária de demanda",
        media_formatada,
        help="Demanda total dividida pelos dias com registros. Valor arredondado.",
        border=True,
    )

df_demanda_diaria = df_demanda.groupby("data_movimento", as_index=False)["demanda"].sum()
df_demanda_diaria = df_demanda_diaria.sort_values("data_movimento")

df_ranking = df_demanda.groupby("codigo_linha", as_index=False)["demanda"].sum()
df_ranking = df_ranking.sort_values("demanda", ascending=False)
df_ranking = df_ranking.head(10)

df_ranking["codigo_linha"] = df_ranking["codigo_linha"].astype(str)

st.divider()
coluna_evolucao, coluna_ranking = st.columns(2)

with coluna_evolucao:
    st.subheader("Evolução diária da demanda")
    st.line_chart(
        df_demanda_diaria,
        x="data_movimento",
        y="demanda",
        x_label="Data",
        y_label="Demanda",
        color="#0D683F",
        height=380,
    )

with coluna_ranking:
    st.subheader("10 linhas com maior demanda")
    st.bar_chart(
        df_ranking,
        x="codigo_linha",
        y="demanda",
        x_label="Linha",
        y_label="Demanda",
        horizontal=True,
        sort=False,
        color="#0D683F",
        height=380,
    )

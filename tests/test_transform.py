import pandas as pd
from datetime import date
import pytest
from src.transform import (
    drop_duplicates,
    rename_columns_janeiro,
    validate_data_fevereiro,
    validate_data_janeiro,
    validate_dates,
)


def test_remover_duplicados_dos_dois_meses():
    df_janeiro = pd.DataFrame({
        "codigo_linha_jan": [10, 10, 10],
        "demanda_jan": [5, 5, 8],
    })
    df_fevereiro = pd.DataFrame({
        "codigo_linha_fev": [20, 20, 20],
        "demanda_fev": [6, 6, 9],
    })

    janeiro, fevereiro = drop_duplicates(df_janeiro, df_fevereiro)

    assert janeiro["demanda_jan"].tolist() == [5, 8]
    assert fevereiro["demanda_fev"].tolist() == [6, 9]


def test_limpar_textos_e_converter_numeros_de_janeiro():
    df = pd.DataFrame({
        "nome_linha_jan": ["  CENTRO  ", None],
        "nome_passageiro_jan": ["  ESTUDANTE  ", None],
        "codigo_linha_jan": ["10", "20"],
        "tipo_passageiro_jan": ["1", "2"],
    })

    resultado = validate_data_janeiro(df)

    assert resultado["nome_linha_jan"].tolist() == ["Centro", "Dado Não Informado"]
    assert resultado["nome_passageiro_jan"].tolist() == ["Estudante", "Dado Não Informado"]
    assert resultado["codigo_linha_jan"].tolist() == [10, 20]
    assert resultado["tipo_passageiro_jan"].tolist() == [1, 2]


def test_limpar_textos_e_converter_numeros_de_fevereiro():
    df = pd.DataFrame({
        "nome_linha_fev": ["  BARRA  ", None],
        "nome_passageiro_fev": ["  INTEIRA  ", None],
        "codigo_linha_fev": ["30", "40"],
        "tipo_passageiro_fev": ["3", "4"],
    })

    resultado = validate_data_fevereiro(df)

    assert resultado["nome_linha_fev"].tolist() == ["Barra", "Dado Não Informado"]
    assert resultado["nome_passageiro_fev"].tolist() == ["Inteira", "Dado Não Informado"]
    assert resultado["codigo_linha_fev"].tolist() == [30, 40]
    assert resultado["tipo_passageiro_fev"].tolist() == [3, 4]


def test_converter_datas_dos_dois_meses():
    df_janeiro = pd.DataFrame({
        "data_movimento_jan": ["2022-01-01", "2022-01-31"],
    })
    df_fevereiro = pd.DataFrame({
        "data_movimento_fev": ["01/02/2022", "13/02/2022"],
    })

    janeiro, fevereiro = validate_dates(df_janeiro, df_fevereiro)

    assert janeiro["data_movimento_jan"].tolist() == [date(2022, 1, 1), date(2022, 1, 31)]
    assert fevereiro["data_movimento_fev"].tolist() == [date(2022, 2, 1), date(2022, 2, 13)]


def test_identificar_datas_invalidas():
    df_janeiro = pd.DataFrame({
        "data_movimento_jan": ["2022-01-15", "2022-01-32"],
    })
    df_fevereiro = pd.DataFrame({
        "data_movimento_fev": ["13/02/2022", "31/02/2022"],
    })

    janeiro, fevereiro = validate_dates(df_janeiro, df_fevereiro)

    assert janeiro.loc[0, "data_movimento_jan"] == date(2022, 1, 15)
    assert fevereiro.loc[0, "data_movimento_fev"] == date(2022, 2, 13)
    assert pd.isna(janeiro.loc[1, "data_movimento_jan"])
    assert pd.isna(fevereiro.loc[1, "data_movimento_fev"])


def test_avisar_quando_falta_coluna_obrigatoria():
    df = pd.DataFrame({
        "DataMovimento": ["2022-01-01"],
        "CodLinha": [10],
        "NomeLinha": ["Centro"],
        "TipoPassageiro": [1],
        "NomePassageiro": ["Inteira"],
    })

    with pytest.raises(KeyError, match="Demanda"):
        rename_columns_janeiro(df)


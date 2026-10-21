import pandas as pd 
import logging as log 

logger = log.getLogger(__name__)

def rename_columns_janeiro(df_janeiro: pd.DataFrame) -> pd.DataFrame:
    
    logger.info("Renomeando colunas do mes de janeiro")

    try:

        columns_rename = {
            "DataMovimento" : "data_movimento_jan",
            "CodLinha" : "codigo_linha_jan",
            "NomeLinha" :"nome_linha_jan",
            "TipoPassageiro" : "tipo_passageiro_jan",
            "NomePassageiro" : "nome_passageiro_jan",
            "Demanda" : "demanda_jan"
        }

    
        df_janeiro.rename(columns= columns_rename, inplace= True, errors= "raise")
        logger.info(f"Colunas: {df_janeiro.shape[1]} / Linhas: {len(df_janeiro)}")
            
    except Exception:
        logger.exception("Erro ao renomear colunas")
        raise
        
    return df_janeiro

def rename_columns_fevereiro(df_fevereiro: pd.DataFrame) -> pd.DataFrame:

    logger.info("Renomeando colunas do mes de fevereiro")
    
    try:
    
        columns_rename = {
            "DataMovimento" : "data_movimento_fev",
            "CodLinha" : "codigo_linha_fev",
            "NomeLinha" :"nome_linha_fev",
            "TipoPassageiro" : "tipo_passageiro_fev",
            "NomePassageiro" : "nome_passageiro_fev",
            "Demanda" : "demanda_fev"
        }


        df_fevereiro.rename(columns= columns_rename, inplace= True, errors= "raise")
        logger.info(f"Colunas: {df_fevereiro.shape[1]} / Linhas: {len(df_fevereiro)}")
                
    except Exception:
        logger.exception("Erro ao renomear colunas")
        raise
            
    return df_fevereiro

def drop_duplicates(df_janeiro: pd.DataFrame, df_fevereiro: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:

    logger.info("Removendo registros duplicados")
    
    dfs = [
        
        ("janeiro", df_janeiro),
        ("fevereiro", df_fevereiro)
    ]
    
    try: 
        for mes, df in dfs:
            
            linhas_antes = len(df)
            df.drop_duplicates(inplace= True)
            linhas_depois = len(df)
        
            logger.warning(f"{mes} Dados removidos: {linhas_antes - linhas_depois} / Linhas depois: {linhas_depois}")

    except Exception:
        logger.exception("Erro ao remover dados duplicados")
        raise 
    
    return df_janeiro, df_fevereiro
        
def validate_data_janeiro(df_janeiro: pd.DataFrame) -> pd.DataFrame:
    
    logger.info("Validação dos dados de janeiro")
    
    cols_string = [
        "nome_linha_jan",
        "nome_passageiro_jan"
    ]
    
    cols_int = [
        "codigo_linha_jan",
        "tipo_passageiro_jan"
        
    ]
    
    try: 
        for cols in cols_string:
            if cols in df_janeiro.columns:
                df_janeiro[cols] = df_janeiro[cols].fillna("Dado não informado").str.strip().str.title()
    
        for cols in cols_int:
            if cols in df_janeiro.columns:
                df_janeiro[cols] = pd.to_numeric(df_janeiro[cols], errors= "coerce")

                valores_invalidos = int(df_janeiro[cols].isna().sum())
                
                if valores_invalidos:
                    logger.warning(f"Valores invalidos do mes de janeiro: {valores_invalidos}")
                    
            logger.info(f"Validações do mes de janeiro realizadas")
            
    except Exception:
        logger.exception("Erro ao validar dados do mes de janeiro")
        raise 
    
    return df_janeiro
        
def validate_data_fevereiro(df_fevereiro: pd.DataFrame) -> pd.DataFrame:
    
    logger.info("Validação dos dados de fevereiro")
    
    cols_string = [
        "nome_linha_fev",
        "nome_passageiro_fev"
    ]
    
    cols_int = [
        "codigo_linha_fev",
        "tipo_passageiro_fev"
        
    ]
    
    try: 
        for cols in cols_string:
            if cols in df_fevereiro.columns:
                df_fevereiro[cols] = df_fevereiro[cols].fillna("Dado não informado").str.strip().str.title()
    
        for cols in cols_int:
            if cols in df_fevereiro.columns:
                df_fevereiro[cols] = pd.to_numeric(df_fevereiro[cols], errors= "coerce")

                valores_invalidos = int(df_fevereiro[cols].isna().sum())
                
                if valores_invalidos:
                    logger.warning(f"Valores invalidos do mes de fevereiro: {valores_invalidos}")
                    
            logger.info(f"Validações do mes de fevereiro realizadas")
            
    except Exception:
        logger.exception("Erro ao validar dados do mes de fevereiro")
        raise 
    
    return df_fevereiro

def validate_dates(df_janeiro: pd.DataFrame, df_fevereiro: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    
    logger.info("Iniciando validações de datas")
    
    dfs = [
        ("janeiro", df_janeiro, "data_movimento_jan", "%Y-%m-%d"),
        ("fevereiro", df_fevereiro, "data_movimento_fev", "%d/%m/%Y")
    ]

    try:
        
        for mes, df, data, formato in dfs:
            
            df[data] = pd.to_datetime(df[data], errors= "coerce", format= formato).dt.date
            data_invalida = int(df[data].isna().sum())
            
            if data_invalida:
                logger.warning(f"Mês:{mes} / Datas invalidas: {data_invalida}")
        
    except Exception:
        logger.exception("Erro ao validar datas")
        raise 
    
    return df_janeiro, df_fevereiro

def transform(df_janeiro: pd.DataFrame, df_fevereiro: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    
    logger.info("Iniciando transformações")
    
    df_janeiro = rename_columns_janeiro(df_janeiro)
    df_fevereiro = rename_columns_fevereiro(df_fevereiro)
    df_janeiro, df_fevereiro = drop_duplicates(df_janeiro, df_fevereiro)
    df_janeiro, df_fevereiro = validate_dates(df_janeiro, df_fevereiro)
    df_janeiro = validate_data_janeiro(df_janeiro)
    df_fevereiro = validate_data_fevereiro(df_fevereiro) 
    
    dfs = [
        ("janeiro", df_janeiro),
        ("fevereiro", df_fevereiro)
    ]
    
    for mes, df in dfs:
        logger.info(f"Transformações realizadas / Mês: {mes} / Colunas: {df.shape[1]} / Linhas: {len(df)}")
    
    return df_janeiro, df_fevereiro
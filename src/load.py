import pandas as pd 
import logging as log 
from sqlalchemy import create_engine, text, inspect
from sqlalchemy import Engine
from dotenv import load_dotenv
import os

load_dotenv(".env.docker")
logger = log.getLogger(__name__)

def credentials() -> Engine: 
    
    user = os.getenv("POSTGRES_USER")
    password = os.getenv("POSTGRES_PASSWORD") 
    host = os.getenv("POSTGRES_HOST")    
    port = os.getenv("POSTGRES_PORT") 
    dbname = os.getenv("POSTGRES_DB") 
    
    if not all ([user, password, host, port, dbname]):
        logger.error("Variaveis não definidas no .env")
        raise ValueError("Variaveis não encontradas")
    
    url_banco = f"postgresql+psycopg://{user}:{password}@{host}:{port}/{dbname}"
    engine = create_engine(url_banco)
    return engine 

def load(df_janeiro: pd.DataFrame, df_fevereiro: pd.DataFrame, engine: Engine) -> None:
    
    logger.info("Iniciando carregamento no banco de dados")
    
    dfs_tabela = [
                ("demanda_janeiro_2022", df_janeiro),
                ("demanda_fevereiro_2022", df_fevereiro)
            ]
    
    try:
        with engine.begin() as con:
            inspector = inspect(con)
        
            for nome_tabela, df in dfs_tabela:
                if inspector.has_table(nome_tabela):
                        con.execute(text(F"TRUNCATE TABLE {nome_tabela}"))
                        
                df.to_sql(name= nome_tabela, con= con, index= False, chunksize= 5000, if_exists= "append")
                logger.info("Carga dos dois meses concluida")
            
    except Exception:
        logger.exception("Erro ao inserir dados")
        raise 
    
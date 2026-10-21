import pandas as pd 
import logging as log
from typing import Dict
import os 
from dotenv import load_dotenv 

load_dotenv(".env.docker")
logger = log.getLogger(__name__)

def extract() -> tuple[pd.DataFrame, pd.DataFrame]:
    
    logger.info("Iniciando extração dos dados")

    try:
        
        janeiro = os.getenv("ARQUIVO_JANEIRO_2022")
        fevereiro = os.getenv("ARQUIVO_FEVEREIRO_2022")
        
        if not janeiro or not fevereiro:
            logger.error("Arquivos não definidos no .env")
            raise ValueError("Variaveis de ambiente não definidas")
        
        colunas_janeiro = [
            "DataMovimento",
            "CodLinha",
            "NomeLinha",
            "TipoPassageiro",
            "NomePassageiro",
            "Demanda"
        ]
        
        df_janeiro = pd.read_csv(janeiro, encoding= "utf-8", low_memory= False, delimiter= ";" ,header=None, names=colunas_janeiro)
        df_fevereiro = pd.read_csv(fevereiro, encoding= "utf-8", low_memory= False, delimiter= ";")
        
    
    except Exception:
        logger.exception("Erro ao extrair arquivos")
        raise 
    
    return df_janeiro, df_fevereiro
        
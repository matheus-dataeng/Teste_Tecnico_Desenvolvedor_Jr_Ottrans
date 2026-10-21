from extract import extract
from transform import transform
from load import credentias, load
from utils.log_config import logging_setup
import logging as log

logging_setup()
logger = log.getLogger(__name__)

def main() -> None:
    
    logger.info("Iniciando Pipeline ETL")
    
    try:
        
        engine_load = credentias()
        
        df_janeiro_extract, df_fevereiro_extract = extract()
        df_janeiro_transform, df_fevereiro_transform = transform(df_janeiro_extract, df_fevereiro_extract)
        load(df_janeiro=df_janeiro_transform, df_fevereiro=df_fevereiro_transform, engine=engine_load)

        logger.info("Pipeline executado com sucesso!")
        
    except Exception:
        logger.exception("Erro ao executar Pipeline")
        raise

if __name__ == "__main__":
    main()
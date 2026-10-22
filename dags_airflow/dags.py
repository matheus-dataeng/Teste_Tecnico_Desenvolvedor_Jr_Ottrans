import pendulum 
import pandas as pd
from airflow import DAG
from airflow.operators.python import PythonOperator
from src.extract import extract
from src.transform import transform
from src.load import credentials, load
from tests.test_transform import (
    test_remover_duplicados_dos_dois_meses,
    test_limpar_textos_e_converter_numeros_de_janeiro,
    test_limpar_textos_e_converter_numeros_de_fevereiro,
    test_converter_datas_dos_dois_meses,
    test_identificar_datas_invalidas,
    test_avisar_quando_falta_coluna_obrigatoria
)

def extract_pipeline():
    
    df_janeiro, df_fevereiro = extract()
    
    return df_janeiro, df_fevereiro

def test_transform_pipeline():

    test_remover_duplicados_dos_dois_meses()
    test_limpar_textos_e_converter_numeros_de_janeiro()
    test_limpar_textos_e_converter_numeros_de_fevereiro()
    test_converter_datas_dos_dois_meses()
    test_identificar_datas_invalidas()
    test_avisar_quando_falta_coluna_obrigatoria()
    
def transform_pipeline(ti):
    df_janeiro, df_fevereiro = ti.xcom_pull(task_ids="extract")
    transform(df_janeiro, df_fevereiro)
 
    return  df_janeiro, df_fevereiro
    
def load_pipeline(ti):
    df_janeiro_transform, df_fevereiro_transform = ti.xcom_pull(task_ids="transform")
    engine_load = credentials()
    
    try:
        load(
            df_janeiro_transform,
            df_fevereiro_transform,
            engine_load
        )
    finally: 
        engine_load.dispose()
        
with DAG(
    dag_id = "Teste_Tecnico_Ottrans",
    start_date = pendulum.datetime(2026, 1, 1, tz="America/Sao_Paulo"),
    catchup= False,
    schedule= None
) as dag:
    
    extract_task = PythonOperator(
        task_id = "extract",
        python_callable = extract_pipeline
    )

    test_transform_task = PythonOperator(
        task_id = "test_transform",
        python_callable = test_transform_pipeline
    )
        
    
    transform_task = PythonOperator(
        task_id = "transform",
        python_callable = transform_pipeline
    )

    
    load_task = PythonOperator(
        task_id = "load",
        python_callable = load_pipeline
    )

extract_task >> test_transform_task >>transform_task >> load_task
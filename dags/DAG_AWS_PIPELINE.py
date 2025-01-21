# Airflow imports
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.dummy import DummyOperator
from airflow.providers.amazon.aws.transfers.local_to_s3 import LocalFilesystemToS3Operator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.providers.amazon.aws.hooks.redshift_sql import RedshiftSQLHook
from airflow.providers.amazon.aws.operators.glue import GlueJobOperator
from airflow.providers.amazon.aws.operators.redshift_data import RedshiftDataOperator
from datetime import datetime, timedelta


#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
##Funciones 
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Librerías para la extracción de datos
import requests
import pandas as pd
import time
import logging
from tempfile import NamedTemporaryFile
import os

# Configuración del sistema de logs
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()

def fetch_articulos_and_transform_data(api_url, file_name="articulos.csv", max_pages=10):
    articles = []
    next_url = api_url
    page = 1

    while next_url and page <= max_pages:
        logger.info(f"Recuperando página {page}...")
        response = requests.get(next_url)

        if response.status_code == 200:
            data = response.json()
            articles.extend(data['results'])

            # Deduplicación basada en el ID del artículo (usando un diccionario)
            unique_articles = {article['id']: article for article in articles}
            articles = list(unique_articles.values())
            logger.info(f"Artículos recuperados: {len(data['results'])}, total acumulado: {len(articles)}")

            next_url = data['next']  # Paginación
            page += 1
        elif response.status_code == 429:  # Rate limit
            logger.warning("Rate limit alcanzado. Esperando 60 segundos...")
            time.sleep(60)  # Espera de 60 segundos
        else:
            logger.error(f"Error al recuperar los datos. Código de estado: {response.status_code}")
            break

    # Transformar los datos en un DataFrame
    logger.info("Transformando los datos a CSV...")
    df = pd.DataFrame(articles, columns=['id', 'title', 'url', 'image_url', 'news_site', 'summary', 'published_at', 'updated_at'])

    # Crear archivo temporal con nombre específico
    tmp_file_path = os.path.join("/tmp", file_name)
    df.to_csv(tmp_file_path, index=False)

    logger.info(f"CSV guardado temporalmente en: {tmp_file_path}")
    return tmp_file_path



 ##blogs
def fetch_blogs_and_transform_data(api_url, file_name="blogs.csv", max_pages=10):
    blogs = []
    next_url = api_url
    page = 1

    while next_url and page <= max_pages:
        logger.info(f"Recuperando página {page}...")
        response = requests.get(next_url)

        if response.status_code == 200:
            data = response.json()
            blogs.extend(data['results'])

            # Deduplicación basada en el ID del blog
            unique_blogs = {blog['id']: blog for blog in blogs}
            blogs = list(unique_blogs.values())
            logger.info(f"Blogs recuperados: {len(data['results'])}, total acumulado: {len(blogs)}")

            next_url = data['next']  # Paginación
            page += 1
        elif response.status_code == 429:  # Rate limit
            logger.warning("Rate limit alcanzado. Esperando 60 segundos...")
            time.sleep(60)  # Espera de 60 segundos
        else:
            logger.error(f"Error al recuperar los datos. Código de estado: {response.status_code}")
            break

    # Transformar los datos en un DataFrame
    logger.info("Transformando los datos a CSV...")
    df = pd.DataFrame(blogs, columns=['id', 'title', 'url', 'image_url', 'news_site', 'summary', 'published_at', 'updated_at'])

    # Crear archivo temporal con nombre específico
    tmp_file_path = os.path.join("/tmp", file_name)
    df.to_csv(tmp_file_path, index=False)

    logger.info(f"CSV guardado temporalmente en: {tmp_file_path}")
    return tmp_file_path

##reports

# Configuración del sistema de logs
#logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
#logger = logging.getLogger()

def fetch_reports_and_transform_data(api_url, file_name="reports.csv", max_pages=10):
    reports = []
    next_url = api_url
    page = 1

    while next_url and page <= max_pages:
        logger.info(f"Recuperando página {page}...")
        response = requests.get(next_url)

        if response.status_code == 200:
            data = response.json()
            reports.extend(data['results'])

            # Deduplicación basada en el ID del reporte
            unique_reports = {report['id']: report for report in reports}
            reports = list(unique_reports.values())
            logger.info(f"Reportes recuperados: {len(data['results'])}, total acumulado: {len(reports)}")

            next_url = data['next']  # Paginación
            page += 1
        elif response.status_code == 429:  # Rate limit
            logger.warning("Rate limit alcanzado. Esperando 60 segundos...")
            time.sleep(60)  # Espera de 60 segundos
        else:
            logger.error(f"Error al recuperar los datos. Código de estado: {response.status_code}")
            break

    # Transformar los datos en un DataFrame
    logger.info("Transformando los datos a CSV...")
    df = pd.DataFrame(reports, columns=['id', 'title', 'url', 'image_url', 'news_site', 'summary', 'published_at', 'updated_at'])

    # Crear archivo temporal con nombre específico
    tmp_file_path = os.path.join("/tmp", file_name)
    df.to_csv(tmp_file_path, index=False)

    logger.info(f"CSV guardado temporalmente en: {tmp_file_path}")
    return tmp_file_path



    
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

# Default arguments
default_args = {
    'owner': 'Wilfrido Rondon',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=2),
}

# DAG definition
with DAG(
    dag_id='DAG_AWS_PIPELINE',
    start_date=datetime(2025, 1, 19),  # Fecha inicial
    default_args=default_args,
    description='Creación de un DAG ETL PostgreSQL',
    schedule_interval=None,
    catchup=False,
    tags=['ETL', 'Ingeniería', 'PostgreSQL'],
) as dag:
    
    # Start and end DummyOperators
    start = DummyOperator(task_id="start")
    end = DummyOperator(task_id="end")

    # PythonOperator for API extraction
    extract_articles = PythonOperator(
        task_id="extract_articles",
        python_callable=fetch_articulos_and_transform_data,
        op_args=["https://api.spaceflightnewsapi.net/v4/articles/", "articulos.csv"],  # Pasa la URL de la API y el nombre del archivo
    )

    extract_blogs = PythonOperator(
        task_id="extract_blogs",
        python_callable=fetch_blogs_and_transform_data,
        op_args=["https://api.spaceflightnewsapi.net/v4/blogs/", "blogs.csv"],  # Pasa la URL de la API y el nombre del archivo
    )

    extract_reports = PythonOperator(
        task_id="extract_events",
        python_callable=fetch_reports_and_transform_data,
        op_args=["https://api.spaceflightnewsapi.net/v4/reports/", "reports.csv"],  # Pasa la URL de la API y el nombre del archivo
    )
    
    # Definir el operador de GlueJob
    Load_Bronze_to_Silver = GlueJobOperator(
       task_id="Load_Bronze_to_Silver", 
       job_name="Transform_from_Bronze_to_Silver",
       script_location = 's3://aws-glue-assets-408069808361-us-east-2/notebooks/Transform_from_Bronze_to_Silver.ipynb',  
       job_desc = 'Job para  datos en Glue',
       retry_limit=3,  # Número de reintentos
       retry_delay=timedelta(minutes=5),  # Espera entre reintentos
       aws_conn_id='aws_conn',
       region_name = 'us-east-2' ,
    )

   
    Load_Silver_to_Gold = GlueJobOperator(
       task_id="Load_Silver_to_Gold", 
       job_name="Load_from_Silver_to_Gold",
       script_location = 's3://aws-glue-assets-408069808361-us-east-2/notebooks/Load_from_Silver_to_Gold.ipynb',  
       job_desc = 'Job para procesar datos en Glue',
       retry_limit=3,  # Número de reintentos
       retry_delay=timedelta(minutes=5),  # Espera entre reintentos
       aws_conn_id='aws_conn',
       region_name = 'us-east-2' ,
    )

   
  
     # Procedimiento almacenado a ejecutar
    procedure_sql = "CALL public.load_data_spaceWD();"
    procedure_sql_stg = 'CALL stg.reload_spaceflight_data()'

# Crear tarea usando el RedshiftSQLOperator
    Execute_procedure_stg = RedshiftDataOperator(
       task_id='Execute_procedure_stg',
       sql=procedure_sql_stg,  # SQL con el procedimiento almacenado a ejecutar
       aws_conn_id ='aws_conn',  # Nombre de la conexión a Redshift configurada en Airflow
       database='warehousepaceflight',
       workgroup_name='default-workgroup',
       region_name='us-east-2',
       dag=dag
)
    
    # Crear tarea usando el RedshiftSQLOperator
    Execute_procedure_warehouse = RedshiftDataOperator(
       task_id='Execute_procedure_warehouse',
       sql=procedure_sql,  # SQL con el procedimiento almacenado a ejecutar
       aws_conn_id ='aws_conn',  # Nombre de la conexión a Redshift configurada en Airflow
       database='warehousepaceflight',
       workgroup_name='default-workgroup',
       region_name='us-east-2',
       dag=dag
)
     # Transfer local file to S3
    transf_articles = LocalFilesystemToS3Operator(
        task_id='transf_articles',
        filename='/tmp/articulos.csv',  # El archivo temporal generado
        dest_key='Bronze/data_articules.csv',
        dest_bucket='spaceflightbuckes2025',
        aws_conn_id='aws_conn',
        replace=True,
    )

    transf_blogs = LocalFilesystemToS3Operator(
        task_id='transf_blogs',
        filename='/tmp/blogs.csv',  # El archivo temporal generado
        dest_key='Bronze/data_blogs.csv',
        dest_bucket='spaceflightbuckes2025',
        aws_conn_id='aws_conn',
        replace=True,
    )

    transf_reports = LocalFilesystemToS3Operator(
        task_id='transf_reports',
        filename='/tmp/reports.csv',  # El archivo temporal generado
        dest_key='Bronze/data_reports.csv',
        dest_bucket='spaceflightbuckes2025',
        aws_conn_id='aws_conn',
        replace=True,
    )
    

    # Task dependencies
    start >> [extract_articles, extract_blogs,extract_reports]
    extract_articles >> transf_articles 
    extract_blogs >> transf_blogs 
    extract_reports >> transf_reports 
    [transf_articles, transf_blogs, transf_reports] >> Load_Bronze_to_Silver>> Load_Silver_to_Gold >> Execute_procedure_stg >>Execute_procedure_warehouse>> end

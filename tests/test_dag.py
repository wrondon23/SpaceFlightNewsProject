import pytest
from unittest.mock import patch, MagicMock
from airflow.models import DagBag
from datetime import datetime
from my_dag_file import fetch_articulos_and_transform_data, fetch_blogs_and_transform_data, fetch_reports_and_transform_data

# Test para verificar si el DAG se carga correctamente
def test_dag_loaded():
    dag_bag = DagBag()
    dag = dag_bag.get_dag(dag_id='DAG_AWS_PIPELINE')
    assert dag is not None, "El DAG 'DAG_AWS_PIPELINE' no fue cargado correctamente."
    assert len(dag.tasks) > 0, "El DAG no contiene tareas."

# Test para validar que todas las tareas tienen dependencias definidas
def test_task_dependencies():
    dag_bag = DagBag()
    dag = dag_bag.get_dag(dag_id='DAG_AWS_PIPELINE')
    for task_id, task in dag.task_dict.items():
        upstream = task.upstream_task_ids
        downstream = task.downstream_task_ids
        assert upstream or downstream, f"La tarea {task_id} no tiene dependencias definidas."

# Test de las funciones Python
@patch('my_dag_file.requests.get')
def test_fetch_articulos_and_transform_data(mock_get):
    # Mock de la respuesta de requests
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        'results': [{'id': 1, 'title': 'Articulo 1', 'url': 'http://example.com', 'image_url': '', 'news_site': '', 'summary': '', 'published_at': '', 'updated_at': ''}],
        'next': None
    }
    mock_get.return_value = mock_response

    # Llamada a la función y validación
    result = fetch_articulos_and_transform_data(api_url="https://fake-url.com")
    assert result.endswith("articulos.csv"), "El archivo CSV no fue creado correctamente."

@patch('my_dag_file.requests.get')
def test_fetch_blogs_and_transform_data(mock_get):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        'results': [{'id': 1, 'title': 'Blog 1', 'url': 'http://example.com', 'image_url': '', 'news_site': '', 'summary': '', 'published_at': '', 'updated_at': ''}],
        'next': None
    }
    mock_get.return_value = mock_response

    result = fetch_blogs_and_transform_data(api_url="https://fake-url.com")
    assert result.endswith("blogs.csv"), "El archivo CSV no fue creado correctamente."

@patch('my_dag_file.requests.get')
def test_fetch_reports_and_transform_data(mock_get):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        'results': [{'id': 1, 'title': 'Report 1', 'url': 'http://example.com', 'image_url': '', 'news_site': '', 'summary': '', 'published_at': '', 'updated_at': ''}],
        'next': None
    }
    mock_get.return_value = mock_response

    result = fetch_reports_and_transform_data(api_url="https://fake-url.com")
    assert result.endswith("reports.csv"), "El archivo CSV no fue creado correctamente."

# Test de configuración de operadores
@patch('airflow.providers.amazon.aws.operators.glue.GlueJobOperator')
def test_glue_job_operator_config(mock_glue_job):
    from my_dag_file import glue_sparkJob
    assert glue_sparkJob.job_name == "JoSpaceFligthV2", "El nombre del Glue Job no coincide."
    assert glue_sparkJob.region_name == "us-east-2", "La región configurada en el Glue Job es incorrecta."

@patch('airflow.providers.amazon.aws.operators.redshift_data.RedshiftDataOperator')
def test_redshift_operator_config(mock_redshift_operator):
    from my_dag_file import Execute_procedure_Redshift
    assert Execute_procedure_Redshift.database == "desarrollo", "El nombre de la base de datos es incorrecto."
    assert Execute_procedure_Redshift.sql == "CALL public.load_data_from_s3();", "El procedimiento almacenado no coincide."

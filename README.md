README del Pipeline de Datos: Análisis de Tendencias en la Industria Espacial
Descripción del Proyecto
Este pipeline de datos extrae, transforma y carga información desde la API de Spaceflight News para generar insights sobre la industria espacial. Utiliza servicios de AWS y Apache Airflow para manejar la orquestación, almacenamiento, procesamiento y análisis de datos.
________________________________________
Componentes del Pipeline
1.	Apache Airflow:
o	Orquesta el flujo de trabajo desde la extracción hasta la carga de datos.
o	Define y programa tareas como DAGs.
2.	Amazon S3:
o	Bucket Raw: Almacena los datos extraídos sin procesar.
o	Bucket Processed: Almacena los datos transformados.
o	Estructura del bucket: 
	s3://spaceflight-news/raw/year=YYYY/month=MM/day=DD/
	s3://spaceflight-news/processed/year=YYYY/month=MM/day=DD/
3.	AWS Glue (con Spark):
o	Realiza transformaciones y limpieza de datos en formato raw.
o	Escribe los datos procesados en S3 en formato Parquet.
4.	Amazon Redshift:
o	Almacena datos transformados para análisis rápido y consultas complejas.
________________________________________
Instalación y Configuración
1.	Prerequisitos:
o	Cuenta activa de AWS con permisos para S3, Glue y Redshift.
o	Entorno de Apache Airflow configurado.
2.	Configuración de Airflow:
o	Variables necesarias: 
	API_ENDPOINT: URL de la API de Spaceflight News.
	S3_BUCKET: Nombre del bucket en S3.
	REDSHIFT_CLUSTER: Nombre del clúster de Redshift.
o	Configurar conexiones en Airflow: 
	AWS Connection: Configurar credenciales de AWS.
	Redshift Connection: Proveer credenciales y endpoint de Redshift.
3.	Glue Job:
o	Escribir el script ETL en PySpark y cargarlo en AWS Glue.
o	Configurar los siguientes recursos: 
	Rol IAM con permisos para leer/escribir en S3.
	Unidad de capacidad DPU adecuada.
________________________________________
Ejecución del Pipeline
1.	Inicio:
o	Programar o ejecutar manualmente el DAG de Airflow.
2.	Flujo:
o	Extracción: Recuperar datos de la API y almacenarlos en s3://raw/.
o	Transformación: Glue procesa los datos y los almacena en s3://processed/.
o	Carga: Los datos transformados se cargan desde S3 a Redshift.
3.	Verificación:
o	Validar que los datos en Redshift estén correctos ejecutando consultas de prueba.
________________________________________
Monitoreo y Mantenimiento
1.	Logs:
o	Verificar logs en Airflow y Glue para identificar posibles errores.
2.	Alertas:
o	Configurar notificaciones en Airflow y Amazon CloudWatch.
3.	Optimización:
o	Revisar regularmente las consultas en Redshift y optimizar si es necesario.
________________________________________
Problemas Comunes y Soluciones
1.	Error en la conexión a Redshift:
o	Verificar credenciales y configuración de red.
2.	Glue Job falla:
o	Revisar el script PySpark y verificar permisos de IAM.
3.	Fallas en la API:
o	Implementar reintentos automáticos en la tarea de extracción.
________________________________________
Contribución
1.	Crear un branch en el repositorio.
2.	Realizar cambios y enviar un Pull Request.
3.	Asegurarse de que el código pase las pruebas antes de hacer merge.
________________________________________




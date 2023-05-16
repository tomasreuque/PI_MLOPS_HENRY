# Proyecto de Análisis de Datos de Películas

Este proyecto consiste en un análisis de datos de películas utilizando Python y las bibliotecas pandas y fastapi. El objetivo principal es obtener información estadística y realizar consultas sobre las películas, como la cantidad de películas lanzadas en un día específico, las ganancias de una franquicia, y más.

## Estructura del Proyecto

El proyecto está organizado de la siguiente manera:

- `ETL.ipynb`: Jupyter Notebook utilizado para el proceso de extracción, transformación y carga de los datos en un DataFrame.
- `app.py`: Archivo Python que contiene una API RESTful desarrollada con la biblioteca fastapi para realizar consultas sobre las películas.
- `archivo.csv`: Archivo CSV utilizado como fuente de datos para el análisis.
- `requirements.txt`: Archivo que especifica las dependencias del proyecto.

## Funcionalidades Principales

El proyecto incluye las siguientes funcionalidades principales:

- Consulta de películas por día: Permite obtener la cantidad de películas lanzadas en un día específico.
- Consulta de ganancias de una franquicia: Permite calcular la cantidad de películas, la ganancia total y la ganancia promedio de una franquicia en particular.

## Cómo Usar

1. Asegúrate de tener instalado Python en tu sistema.
2. Clona este repositorio en tu máquina local.
3. Instala las dependencias del proyecto ejecutando el siguiente comando: `pip install -r requirements.txt`.
4. Ejecuta el archivo `app.py` para iniciar el servidor de la API.
5. Accede a la API en tu navegador o utilizando herramientas como Postman para realizar las consultas.

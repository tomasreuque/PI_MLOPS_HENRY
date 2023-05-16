from fastapi import FastAPI
import uvicorn
import locale
import numpy as np
import calendar
from datetime import datetime
import pandas as pd

df = pd.read_csv('/home/tomas/Desktop/PI_MLOPS_HENRY/archivo.csv') 
df = df.fillna(0)

#Creo una instancia de fastapi
app = FastAPI()


@app.get("/peliculas_mes/{mes}")
def peliculas_mes(mes):
    # Establecer el idioma a español
    locale.setlocale(locale.LC_ALL, 'es_AR.utf8')
    # Convertir la columna 'release_date' a tipo fecha y hora
    df['release_date'] = pd.to_datetime(df['release_date'])
    # Crear una columna auxiliar con el número de mes
    df['mes'] = df['release_date'].dt.month
    # Obtener el número del mes en base al nombre en español
    numero_mes = None
    for i, nombre_mes in enumerate(calendar.month_name):
        if nombre_mes.lower() == mes.lower():
            numero_mes = i
            break
    if numero_mes is None or numero_mes == 0:
        return {'error': 'Mes inválido'}
    # Filtrar el DataFrame para obtener las películas que se estrenaron en el mes especificado
    peliculas_mes = df[df['mes'] == numero_mes]
    # Obtener la cantidad de películas
    cantidad = len(peliculas_mes)
    return {'mes': mes, 'cantidad': cantidad}

@app.get("/peliculas_dia/{dia}")
def peliculas_dia(dia):
    # Establecer el idioma a español
    locale.setlocale(locale.LC_ALL, 'es_AR.utf8')
    # Convertir la columna 'release_date' a tipo fecha y hora
    df['release_date'] = pd.to_datetime(df['release_date'])
    # Crear una columna auxiliar con el nombre del día en español
    df['dia'] = df['release_date'].dt.strftime('%A').str.lower()
    # Obtener la cantidad de películas para el día especificado
    cantidad = len(df[df['dia'] == dia.lower()])
    return {'dia': dia, 'cantidad': cantidad}

@app.get("/franquicia/{nombre}")
def franquicia(franquicia):
    # Filtrar las películas de la franquicia y donde el budget y el revenue no sean cero
    franquicia_df = df[(df['belongs_to_collection'] == franquicia) & (df['budget'] != 0) & (df['revenue'] != 0)]
    # Calcular la cantidad de películas
    cantidad = len(franquicia_df)
    # Calcular la ganancia total
    ganancia_total = franquicia_df['revenue'].sum() - franquicia_df['budget'].sum()
    # Calcular la ganancia promedio
    ganancia_promedio = ganancia_total / cantidad
    
    return {
        'franquicia': franquicia,
        'cantidad': cantidad,
        'ganancia_total': ganancia_total,
        'ganancia_promedio': ganancia_promedio 
    }

@app.get("/pais/{pais}")
def peliculas_pais(pais):
    count = sum(df['production_countries'].apply(lambda x: pais in x))
    return {'pais': pais, 'cantidad': count}

@app.get("/productoras/{productora}")
def productoras(productora):
    filtered_df = df[(df['production_companies'].apply(lambda x: productora in x)) & (df['budget'] != 0) & (df['revenue'] != 0)]
    ganancia_total = filtered_df['revenue'].sum()
    cantidad = filtered_df.shape[0]
    return {'productora': productora, 'ganancia_total': ganancia_total, 'cantidad': cantidad}

@app.get("/retorno_pelicula/{pelicula}")
def retorno(pelicula):
    selected_movie = df[df['title'] == pelicula]
    inversion = selected_movie['budget'].values[0].item()
    ganancia = selected_movie['revenue'].values[0].item()
    retorno = (ganancia - inversion) / inversion
    anio = selected_movie['release_year'].values[0].item()
    return {'pelicula': pelicula, 'inversion': inversion, 'ganancia': ganancia, 'retorno': retorno, 'anio': anio}


#scpript para correr localmente el codigo
#if __name__ == "__main__":
#    uvicorn.run(app, host="0.0.0.0", port=8000)



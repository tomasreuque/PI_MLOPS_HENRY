from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
from fastapi import FastAPI
import uvicorn
import numpy as np
import ast
import pandas as pd

df = pd.read_csv('archivo.csv') 
df = df.fillna(0)

#Creo una instancia de fastapi
app = FastAPI()


@app.get("/peliculas_mes/{mes}")
def peliculas_mes(mes):
    # Diccionario con los nombres de los meses en español y su correspondiente número
    meses = {
        'enero': 1,
        'febrero': 2,
        'marzo': 3,
        'abril': 4,
        'mayo': 5,
        'junio': 6,
        'julio': 7,
        'agosto': 8,
        'septiembre': 9,
        'octubre': 10,
        'noviembre': 11,
        'diciembre': 12
    }
    # Verificar si el mes especificado es válido
    numero_mes = meses.get(mes.lower())
    if not numero_mes:
        return {'error': 'Mes inválido'}
    # Convertir la columna 'release_date' a tipo fecha y hora (si aún no está convertida)
    if not pd.api.types.is_datetime64_any_dtype(df['release_date']):
        df['release_date'] = pd.to_datetime(df['release_date'], errors='coerce')
    # Filtrar el DataFrame para obtener las películas que se estrenaron en el mes especificado
    peliculas_mes = df[df['release_date'].dt.month == numero_mes]
    # Obtener la cantidad de películas
    cantidad = len(peliculas_mes)

    return {'mes': mes, 'cantidad': cantidad}


@app.get("/peliculas_dia/{dia}")
def peliculas_dia(dia):
    # Diccionario con los nombres de los días en español y su correspondiente nombre en inglés
    dias = {
        'lunes': 'Monday',
        'martes': 'Tuesday',
        'miércoles': 'Wednesday',
        'jueves': 'Thursday',
        'viernes': 'Friday',
        'sábado': 'Saturday',
        'domingo': 'Sunday'
    }
    # Verificar si el día especificado es válido
    nombre_dia = dias.get(dia.lower())
    if not nombre_dia:
        return {'error': 'Día inválido'}
    # Convertir la columna 'release_date' a tipo fecha y hora (si aún no está convertida)
    if not pd.api.types.is_datetime64_any_dtype(df['release_date']):
        df['release_date'] = pd.to_datetime(df['release_date'], errors='coerce')
    # Obtener la cantidad de películas para el día especificado
    cantidad = len(df[df['release_date'].dt.strftime('%A').str.lower() == nombre_dia.lower()])

    return {'dia': dia, 'cantidad': cantidad}

@app.get("/franquicia/{franquicia}")
def franquicia(franquicia):
    # Filtrar las películas de la franquicia y donde el budget y el revenue no sean cero
    franquicia_df = df[(df['belongs_to_collection'].notna()) & (df["belongs_to_collection"].str.contains(franquicia))]
    # si no se encuentra la franquicia
    if franquicia_df.empty:
        return "No se encontro la franquicia solicitada"
    
    # Calcular la cantidad de películas
    cantidad = franquicia_df.shape[0]
    # Calcular la ganancia total
    ganancia_total = franquicia_df['revenue'].sum()
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
    # Filtrar las películas que contienen la productora especificada
    filtered_df = df[df['production_companies'].apply(lambda x: productora in ast.literal_eval(x))]

    # Calcular la ganancia total sumando los valores de 'revenue' para todas las películas filtradas
    ganancia_total = filtered_df['revenue'].sum()

    # Obtener la cantidad de películas que cumplen con los filtros
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


## Modelo de recomendacion basado en contenido
# Cargar el DataFrame original desde el archivo CSV
df = pd.read_csv("archivo.csv")

# Obtener características relevantes de las películas
features = df['overview'].fillna('')

# Crear una matriz de características utilizando la representación Bag-of-Words
vectorizer = CountVectorizer()
feature_matrix = vectorizer.fit_transform(features)

# Calcular la similitud del coseno entre las películas
similarity_matrix = cosine_similarity(feature_matrix)

# Definir la función de recomendación
def recomendacion(titulo):
    # Buscar el índice de la película con el título dado
    movie_index = df[df['title'] == titulo].index[0]

    # Obtener los puntajes de similitud para la película dada
    movie_scores = similarity_matrix[movie_index]

    # Obtener los índices de las películas similares en orden descendente
    similar_movies_indices = movie_scores.argsort()[::-1]

    # Obtener los títulos y valores de voto de las películas similares
    similar_movies_data = df.iloc[similar_movies_indices[:5]][['title', 'vote_average']]

    # Ordenar las películas por voto en orden descendente
    similar_movies_data = similar_movies_data.sort_values(by='vote_average', ascending=False)

    # Obtener los títulos de las películas recomendadas en una lista
    similar_movies_titles = similar_movies_data['title'].tolist()

    # Devolver el resultado como un diccionario
    return {'lista_recomendada': similar_movies_titles}

# Ruta para la recomendación de películas
@app.get("/recomendacion/{titulo}")
def get_recomendacion(titulo: str):
    return recomendacion(titulo)


#scpript para correr localmente el codigo
#if __name__ == "__main__":
#    uvicorn.run(app, host="0.0.0.0", port=8000)



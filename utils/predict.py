import os
import pickle
import numpy as np
import pandas as pd
from functools import lru_cache


BASE_DIR = os.path.dirname(os.path.dirname(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "models", "modelo_ventas.pkl")
DATA_DIR = os.path.join(BASE_DIR, "data")


FEATURES = [
    "Year_of_Release",
    "Platform_encoded",
    "Genre_encoded",
    "Publisher_encoded",
    "Critic_Score",
    "Critic_Count",
    "User_Score",
    "User_Count",
    "has_critic_score",
    "has_user_score"
]


GENRE_TRANSLATIONS = {
    "Action": "Acción",
    "Adventure": "Aventura",
    "Fighting": "Pelea",
    "Misc": "Misceláneo",
    "Platform": "Plataformas",
    "Puzzle": "Puzzle",
    "Racing": "Carreras",
    "Role-Playing": "RPG",
    "Shooter": "Shooter",
    "Simulation": "Simulación",
    "Sports": "Deportes",
    "Strategy": "Estrategia"
}


@lru_cache(maxsize=1)
def load_model():
    with open(MODEL_PATH, "rb") as f:
        return pickle.load(f)


def find_dataset_path():
    """
    Busca automáticamente un archivo .csv dentro de la carpeta data.
    Se queda con el primer CSV que encuentre.
    """
    if not os.path.exists(DATA_DIR):
        raise FileNotFoundError("No existe la carpeta data.")

    csv_files = [
        file for file in os.listdir(DATA_DIR)
        if file.lower().endswith(".csv")
    ]

    if not csv_files:
        raise FileNotFoundError("No se encontró ningún archivo CSV dentro de la carpeta data.")

    return os.path.join(DATA_DIR, csv_files[0])


@lru_cache(maxsize=1)
def load_reference_data():
    """
    Carga el dataset usado como referencia para traducir nombres reales
    a códigos numéricos usados por el modelo.
    """
    data_path = find_dataset_path()
    df = pd.read_csv(data_path)

    required_columns = [
        "Platform",
        "Platform_encoded",
        "Genre",
        "Genre_encoded",
        "Publisher",
        "Publisher_encoded"
    ]

    missing_columns = [
        col for col in required_columns
        if col not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            "Faltan columnas en el dataset: " + ", ".join(missing_columns)
        )

    return df


def create_mapping(df, text_column, encoded_column):
    """
    Crea un diccionario del tipo:
    nombre real -> código usado por el modelo.
    """
    mapping = (
        df[[text_column, encoded_column]]
        .dropna()
        .drop_duplicates()
        .set_index(text_column)[encoded_column]
        .to_dict()
    )

    return mapping


def get_form_options():
    """
    Entrega las opciones que aparecerán en el formulario.
    El usuario verá nombres reales, no códigos.
    """
    try:
        df = load_reference_data()

        platforms = sorted(df["Platform"].dropna().unique().tolist())
        genres_raw = sorted(df["Genre"].dropna().unique().tolist())
        publishers = sorted(df["Publisher"].dropna().unique().tolist())

        genres = [
            {
                "value": genre,
                "label": GENRE_TRANSLATIONS.get(genre, genre)
            }
            for genre in genres_raw
        ]

        return {
            "platforms": platforms,
            "genres": genres,
            "publishers": publishers
        }

    except Exception:
        return {
            "platforms": [],
            "genres": [],
            "publishers": []
        }


def make_prediction(datos):
    """
    Recibe datos del formulario en formato amigable:
    plataforma, género y editora con nombres reales.

    Luego los transforma a las variables codificadas que necesita el modelo.
    """

    try:
        model = load_model()
        df_ref = load_reference_data()

        platform_map = create_mapping(df_ref, "Platform", "Platform_encoded")
        genre_map = create_mapping(df_ref, "Genre", "Genre_encoded")
        publisher_map = create_mapping(df_ref, "Publisher", "Publisher_encoded")

        platform = datos["Platform"]
        genre = datos["Genre"]
        publisher = datos["Publisher"]

        if platform not in platform_map:
            return f"No se encontró la plataforma '{platform}' en el dataset."

        if genre not in genre_map:
            return f"No se encontró el género '{genre}' en el dataset."

        if publisher not in publisher_map:
            return f"No se encontró la editora '{publisher}' en el dataset."

        input_data = pd.DataFrame([{
            "Year_of_Release": float(datos["Year_of_Release"]),
            "Platform_encoded": float(platform_map[platform]),
            "Genre_encoded": float(genre_map[genre]),
            "Publisher_encoded": float(publisher_map[publisher]),
            "Critic_Score": float(datos["Critic_Score"]),
            "Critic_Count": float(datos["Critic_Count"]),
            "User_Score": float(datos["User_Score"]),
            "User_Count": float(datos["User_Count"]),
            "has_critic_score": int(datos["has_critic_score"]),
            "has_user_score": int(datos["has_user_score"]),
        }])

        input_data = input_data[FEATURES]

        pred_log = model.predict(input_data)[0]
        pred_global_sales = np.expm1(pred_log)

        if pred_global_sales < 0:
            pred_global_sales = 0

        return f"Predicción estimada: {pred_global_sales:.2f} millones de unidades vendidas."

    except FileNotFoundError as e:
        return f"Error: {str(e)}"

    except ValueError as e:
        return f"Error en los datos del proyecto: {str(e)}"

    except Exception as e:
        return f"Error al realizar la predicción: {str(e)}"

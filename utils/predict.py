import os
import pickle
import numpy as np
import pandas as pd


BASE_DIR = os.path.dirname(os.path.dirname(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "models", "modelo_ventas.pkl")


with open(MODEL_PATH, "rb") as f:
    model = pickle.load(f)


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


def make_prediction(datos):
    """
    Recibe los datos del formulario, los transforma al formato requerido
    por el modelo y retorna la predicción de ventas globales.
    """

    try:
        input_data = pd.DataFrame([{
            "Year_of_Release": float(datos["Year_of_Release"]),
            "Platform_encoded": float(datos["Platform_encoded"]),
            "Genre_encoded": float(datos["Genre_encoded"]),
            "Publisher_encoded": float(datos["Publisher_encoded"]),
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

    except FileNotFoundError:
        return "Error: no se encontró el archivo del modelo en la carpeta models."

    except Exception as e:
        return f"Error al realizar la predicción: {str(e)}"

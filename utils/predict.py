import os

# Cuando el modelo esté listo, descomentar estas líneas:
# import pickle
# MODEL_PATH = os.path.join(os.path.dirname(__file__), '..', 'models', 'model.pkl')
# with open(MODEL_PATH, 'rb') as f:
#     model = pickle.load(f)

def make_prediction(datos):
    """
    Recibe un diccionario con los datos del formulario y retorna una predicción.
    Por ahora retorna un valor de prueba hasta que el modelo .pkl esté disponible.
    """

    # --- REEMPLAZAR ESTO cuando llegue el modelo ---
    # features = [float(datos['na_sales']), float(datos['eu_sales']), ...]
    # prediction = model.predict([features])[0]
    # return round(float(prediction), 2)
    # -----------------------------------------------

    # Valor de prueba temporal
    return "🔧 Modelo aún no conectado. Aquí aparecerá la predicción de ventas globales."

from flask import Flask, render_template, request
from utils.predict import make_prediction, get_form_options
import os

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/modelos')
def modelos():
    return render_template('modelos.html')


@app.route('/prediccion', methods=['GET', 'POST'])
def prediccion():
    resultado = None
    error = None

    # Opciones para los select del formulario
    opciones = get_form_options()

    if request.method == 'POST':
        try:
            datos = {
                'Year_of_Release': request.form.get('year_of_release'),
                'Platform': request.form.get('platform'),
                'Genre': request.form.get('genre'),
                'Publisher': request.form.get('publisher'),
                'Critic_Score': request.form.get('critic_score'),
                'Critic_Count': request.form.get('critic_count'),
                'User_Score': request.form.get('user_score'),
                'User_Count': request.form.get('user_count'),
                'has_critic_score': request.form.get('has_critic_score'),
                'has_user_score': request.form.get('has_user_score'),
            }

            resultado = make_prediction(datos)

        except Exception as e:
            error = f"Ocurrió un error al realizar la predicción: {str(e)}"

    return render_template(
        'prediccion.html',
        resultado=resultado,
        error=error,
        opciones=opciones
    )


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)

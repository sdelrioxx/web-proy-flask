from flask import Flask, render_template, request
from utils.predict import make_prediction
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

    if request.method == 'POST':
        try:
            datos = {
                'platform': request.form.get('platform'),
                'genre': request.form.get('genre'),
                'year': request.form.get('year'),
                'na_sales': request.form.get('na_sales'),
                'eu_sales': request.form.get('eu_sales'),
            }

            resultado = make_prediction(datos)

        except Exception as e:
            error = f"Ocurrió un error al realizar la predicción: {str(e)}"

    return render_template(
        'prediccion.html',
        resultado=resultado,
        error=error
    )


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
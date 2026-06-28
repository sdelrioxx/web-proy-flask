# GameSales ML 🎮

Aplicación web para predicción de ventas globales de videojuegos usando Machine Learning.

## Objetivo
Predecir las ventas globales (en millones de unidades) de un videojuego dado su plataforma, género, año de lanzamiento y ventas regionales.

## Modelo utilizado
[ Completar cuando esté definido — Modelo A o B según métricas ]

## Cómo ejecutar la aplicación

1. Instalar dependencias:
```
pip install -r requirements.txt
```

2. Ejecutar el servidor:
```
python app.py
```

3. Abrir en el navegador: `http://localhost:5000`

## Navegación
- `/` → Página principal con descripción del proyecto
- `/modelos` → Comparación de modelos y métricas
- `/prediccion` → Formulario para ingresar datos y obtener predicción

## Estructura del proyecto
```
proyecto_web/
├── app.py              # Servidor Flask principal
├── requirements.txt    # Dependencias
├── README.md
├── static/
│   └── css/style.css   # Estilos
├── templates/
│   ├── base.html       # Plantilla base (navbar + footer)
│   ├── index.html      # Página principal
│   ├── modelos.html    # Página de modelos
│   └── prediccion.html # Formulario de predicción
├── models/
│   └── model.pkl       # Modelo entrenado (agregar cuando esté listo)
├── utils/
│   └── predict.py      # Función de predicción
└── data/               # Dataset opcional en .csv
```

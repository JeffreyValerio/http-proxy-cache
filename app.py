#!/usr/bin/env python3
"""
Backend simple para probar el proxy
Devuelve páginas HTML con timestamp
"""

from flask import Flask
import time

app = Flask(__name__)


@app.route("/")
def home():
    return f"""
    <html>
        <body style="font-family: Arial; padding: 20px;">
            <h1>Servidor Backend - Página de Inicio</h1>
            <p>Esta respuesta fue generada en: <b>{time.time()}</b></p>
            <p>Si el timestamp es el MISMO en dos peticiones consecutivas al proxy,
            significa que la segunda vino del CACHÉ.</p>
            <a href="/about">Ir a About</a>
        </body>
    </html>
    """


@app.route("/about")
def about():
    return f"""
    <html>
        <body style="font-family: Arial; padding: 20px;">
            <h1>Acerca de este proyecto</h1>
            <p>Este es un servidor backend simple para probar un Proxy HTTP con Caché.</p>
            <p>Timestamp: <b>{time.time()}</b></p>
            <a href="/">Volver al inicio</a>
        </body>
    </html>
    """


if __name__ == "__main__":
    print("✓ Backend corriendo en http://localhost:5000")
    app.run(host="0.0.0.0", port=5000, debug=False)

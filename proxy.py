#!/usr/bin/env python3
"""
HTTP Proxy con Caché en Memoria

QUÉ HACE:
---------
Este proxy es como un "intermediario" entre el cliente y un servidor web.

Cuando un cliente solicita una página:
1. Si LA TENEMOS EN CACHÉ → la devolvemos rápido (CACHE HIT)
2. Si NO LA TENEMOS → la pedimos al servidor, la guardamos y la devolvemos (CACHE MISS)

Así evitamos contactar al servidor web repetidas veces por las mismas páginas.

CÓMO FUNCIONA:
---------------
Cliente → Proxy → Caché ← Backend
                 (en memoria)

VENTAJAS:
---------
✓ Más rápido: respuestas desde memoria vs desde el servidor
✓ Menos carga: el servidor recibe menos peticiones
✓ Menos ancho de banda: no se repite tráfico de red
"""

import http.server
import socketserver
import requests
import json
from urllib.parse import urlparse
import threading
import time

# CACHÉ EN MEMORIA
# Estructura: {"url": {"contenido": "...", "tiempo": timestamp}}
CACHE = {}
CACHE_TTL = 60  # Segundos antes de que expire el caché
BACKEND_URL = "http://backend:5000"  # Servidor backend (en docker-compose)

PORT = 8888


class CacheHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    """
    Handler que intercepta peticiones HTTP y utiliza caché.
    """

    def do_GET(self):
        """Procesa peticiones GET con caché."""

        # Construir URL completa del recurso solicitado
        resource = self.path
        cache_key = f"{BACKEND_URL}{resource}"

        print(f"[PROXY] GET {resource}")

        # PASO 1: Verificar si está en caché
        if cache_key in CACHE:
            cached = CACHE[cache_key]
            # Verificar si ha expirado
            if time.time() - cached["tiempo"] < CACHE_TTL:
                print(f"  ✓ CACHE HIT - Devolviendo desde caché")

                # Enviar respuesta cacheada al cliente
                self.send_response(200)
                self.send_header("Content-Type", "text/html")
                self.send_header("X-Cache", "HIT")
                self.end_headers()
                self.wfile.write(cached["contenido"].encode())
                return
            else:
                print(f"  ✗ Caché expirado, solicitando al backend")
                del CACHE[cache_key]

        # PASO 2: Caché MISS - Solicitar al backend
        print(f"  ✗ CACHE MISS - Pidiendo al backend")
        try:
            response = requests.get(
                f"{BACKEND_URL}{resource}",
                timeout=5
            )
            contenido = response.text

            # PASO 3: Guardar en caché
            CACHE[cache_key] = {
                "contenido": contenido,
                "tiempo": time.time()
            }
            print(f"  → Guardado en caché")

            # PASO 4: Enviar al cliente
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.send_header("X-Cache", "MISS")
            self.end_headers()
            self.wfile.write(contenido.encode())

        except requests.exceptions.RequestException as e:
            print(f"  ✗ Error conectando al backend: {e}")
            self.send_response(502)
            self.send_header("Content-Type", "text/plain")
            self.end_headers()
            self.wfile.write(b"Error: No se puede contactar al backend")

    def do_HEAD(self):
        """Procesa peticiones HEAD."""
        self.do_GET()

    def log_message(self, format, *args):
        """Personalizar logs."""
        pass  # No mostrar logs por defecto


def print_stats():
    """Mostrar estadísticas del caché cada 10 segundos."""
    while True:
        time.sleep(10)
        hits = sum(1 for _ in CACHE)
        print(f"[STATS] Elementos en caché: {hits}")


if __name__ == "__main__":
    print("=" * 60)
    print("HTTP PROXY CON CACHÉ - En Puerto 8888")
    print("=" * 60)
    print()
    print("QUÉ HACE:")
    print("  • Intercepta peticiones HTTP del cliente")
    print("  • Verifica si la respuesta está en caché")
    print("  • Si SÍ (CACHE HIT): devuelve desde memoria (rápido)")
    print("  • Si NO (CACHE MISS): pide al backend y cachea respuesta")
    print()
    print("CÓMO PROBAR:")
    print("  curl http://localhost:8888/       # Primera vez: MISS")
    print("  curl http://localhost:8888/       # Segunda vez: HIT (desde caché)")
    print()
    print("=" * 60)
    print()

    # Thread para mostrar estadísticas
    stats_thread = threading.Thread(target=print_stats, daemon=True)
    stats_thread.start()

    # Crear servidor HTTP
    with socketserver.TCPServer(("", PORT), CacheHTTPRequestHandler) as httpd:
        print(f"✓ Proxy escuchando en http://localhost:{PORT}")
        print(f"✓ Reenviando solicitudes a {BACKEND_URL}")
        print()

        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n\n✗ Proxy detenido")

#!/usr/bin/env python3
"""
Servidor simple para servir el dashboard y los datos JSON
Ejecutar: python server.py
Luego abrir: http://localhost:8000
"""

import json
import os
import sys
from http.server import HTTPServer, SimpleHTTPRequestHandler

# Añadir directorio padre al path para importar configuraciones
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class DashboardHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=os.path.dirname(os.path.abspath(__file__)), **kwargs)
    
    def do_GET(self):
        # Ruta para obtener los datos del JSON
        if self.path == '/api/data':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            # Buscar el archivo JSON más reciente
            json_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 
                                    'data', 'resultados', 'perfil_extraido.json')
            
            if os.path.exists(json_path):
                with open(json_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                self.wfile.write(json.dumps(data, indent=2, ensure_ascii=False).encode('utf-8'))
            else:
                self.wfile.write(json.dumps({"error": "No se encontraron datos"}).encode('utf-8'))
        else:
            # Servir archivos estáticos normalmente
            super().do_GET()

def main():
    port = 8000
    server = HTTPServer(('localhost', port), DashboardHandler)
    print(f"🚀 Servidor iniciado en http://localhost:{port}")
    print(f"📊 Dashboard disponible en http://localhost:{port}")
    print("Presiona Ctrl+C para detener el servidor")
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n👋 Servidor detenido")
        server.server_close()

if __name__ == '__main__':
    main()
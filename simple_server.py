import http.server
import socketserver
import json
import os
import sys

PORT = 8000
DATA_DIR = 'SAVE'
DATA_FILE = os.path.join(DATA_DIR, 'data.json')

class AssetManagerHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/api/data':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            if os.path.exists(DATA_FILE):
                try:
                    with open(DATA_FILE, 'rb') as f:
                        self.wfile.write(f.read())
                except Exception as e:
                    self.wfile.write(json.dumps({'error': str(e)}).encode())
            else:
                self.wfile.write(json.dumps({}).encode())
        else:
            # Serve static files
            super().do_GET()

    def do_POST(self):
        if self.path == '/api/data':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            try:
                # Ensure directory exists
                if not os.path.exists(DATA_DIR):
                    os.makedirs(DATA_DIR)
                    
                # Parse to validate JSON
                data = json.loads(post_data.decode('utf-8'))
                
                # Save to file
                with open(DATA_FILE, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
                    
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({'success': True}).encode())
                print(f"Dados salvos com sucesso em {DATA_FILE}")
                
            except Exception as e:
                print(f"Erro ao salvar: {e}")
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({'error': str(e)}).encode())
        else:
            self.send_response(404)
            self.end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

print(f"Iniciando servidor em http://localhost:{PORT}")
print(f"Os dados serão salvos na pasta '{DATA_DIR}'")

with socketserver.TCPServer(("", PORT), AssetManagerHandler) as httpd:
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServidor parado.")

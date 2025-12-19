import http.server
import json
import os
from urllib.parse import urlparse

PORT = 8000
DATA_FILE = 'data.json'

class RequestHandler(http.server.BaseHTTPRequestHandler):
    def _set_headers(self, content_type='application/json'):
        self.send_response(200)
        self.send_header('Content-Type', content_type)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_OPTIONS(self):
        self._set_headers()

    def do_GET(self):
        query = urlparse(self.path).path
        if query == '/api/data':
            if os.path.exists(DATA_FILE):
                with open(DATA_FILE, 'r', encoding='utf-8') as f:
                    data = f.read()
                self._set_headers()
                self.wfile.write(data.encode('utf-8'))
            else:
                self._set_headers()
                self.wfile.write(json.dumps({}).encode('utf-8'))
        else:
            self.send_error(404)

    def do_POST(self):
        query = urlparse(self.path).path
        if query == '/api/data':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            try:
                # Validate JSON
                data = json.loads(post_data.decode('utf-8'))
                
                with open(DATA_FILE, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=4, ensure_ascii=False)
                
                self._set_headers()
                self.wfile.write(json.dumps({"status": "success"}).encode('utf-8'))
            except Exception as e:
                self.send_response(500)
                self.end_headers()
                self.wfile.write(json.dumps({"status": "error", "message": str(e)}).encode('utf-8'))
        else:
            self.send_error(404)

if __name__ == '__main__':
    print(f"Starting server on port {PORT}...")
    print(f"Saving data to {DATA_FILE}")
    http.server.HTTPServer(('', PORT), RequestHandler).serve_forever()

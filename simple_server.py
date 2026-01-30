import http.server
import json
import os
import posixpath
from urllib.parse import urlparse, unquote

PORT = 8000
DATA_FILE = 'data.json'

class RequestHandler(http.server.SimpleHTTPRequestHandler):
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
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        
        if path == '/api/data':
            if os.path.exists(DATA_FILE):
                with open(DATA_FILE, 'r', encoding='utf-8') as f:
                    data = f.read()
                self._set_headers()
                self.wfile.write(data.encode('utf-8'))
            else:
                self._set_headers()
                self.wfile.write(json.dumps({}).encode('utf-8'))
        else:
            # Serve static files
            return super().do_GET()

    def do_POST(self):
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        
        if path == '/api/data':
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
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"status": "error", "message": str(e)}).encode('utf-8'))
        else:
            self.send_error(404)

if __name__ == '__main__':
    print(f"======================================")
    print(f"Asset Manager Server")
    print(f"URL: http://localhost:{PORT}")
    print(f"Data File: {DATA_FILE}")
    print(f"======================================")
    http.server.HTTPServer(('', PORT), RequestHandler).serve_forever()

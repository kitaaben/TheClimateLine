"""Climate Cache Server — serves static files + POST /save for JSON caching."""
import http.server
import json
import os
import hashlib

PORT = 8080
DIRECTORY = os.path.dirname(os.path.abspath(__file__))
CACHE_DIR = os.path.join(DIRECTORY, 'cache')
os.makedirs(CACHE_DIR, exist_ok=True)


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def _ok(self, data):
        body = json.dumps(data).encode()
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_POST(self):
        if self.path != '/save':
            return self.send_error(404)
        try:
            length = int(self.headers.get('Content-Length', 0))
            payload = json.loads(self.rfile.read(length))
            key = payload.get('key', '')
            if not key:
                return self._ok({'error': 'Missing key'})
            path = os.path.join(CACHE_DIR, hashlib.md5(key.encode()).hexdigest() + '.json')
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(payload.get('data'), f, ensure_ascii=False)
            self._ok({'ok': True})
        except Exception as e:
            self._ok({'error': str(e)})

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()


if __name__ == '__main__':
    s = http.server.HTTPServer(('0.0.0.0', PORT), Handler)
    print(f'Serving on http://localhost:{PORT}')
    try:
        s.serve_forever()
    except KeyboardInterrupt:
        s.server_close()

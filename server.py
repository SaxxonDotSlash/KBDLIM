import json
import os
import re
from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

PORT = 8000
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
MAPS_DIR = os.path.join(ROOT_DIR, 'maps')

class SaveMapRequestHandler(SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

    def do_POST(self):
        parsed = urlparse(self.path)
        if parsed.path != '/save-map':
            return super().do_POST()

        query = parse_qs(parsed.query)
        map_key = query.get('map', [''])[0]
        if not map_key or not re.fullmatch(r'[A-Za-z0-9_-]+', map_key):
            self.send_error(400, 'Invalid map key')
            return

        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length).decode('utf-8')
        try:
            map_info = json.loads(body)
        except json.JSONDecodeError:
            self.send_error(400, 'Invalid JSON payload')
            return

        target_path = os.path.join(MAPS_DIR, f'{map_key}.json')
        if not os.path.commonpath([ROOT_DIR, os.path.abspath(target_path)]) == ROOT_DIR:
            self.send_error(400, 'Invalid save path')
            return

        try:
            with open(target_path, 'w', encoding='utf-8') as f:
                json.dump(map_info, f, indent=2)
                f.write('\n')
        except Exception as exc:
            self.send_error(500, f'Failed to save map: {exc}')
            return

        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({'status': 'ok', 'saved': True}).encode('utf-8'))

if __name__ == '__main__':
    os.chdir(ROOT_DIR)
    server = HTTPServer(('0.0.0.0', PORT), SaveMapRequestHandler)
    print(f'Serving HTTP at http://localhost:{PORT}/')
    print('Use Ctrl+C to stop.')
    server.serve_forever()

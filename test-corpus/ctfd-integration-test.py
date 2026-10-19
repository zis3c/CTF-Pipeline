#!/usr/bin/env python3
"""Small local CTFd API compatibility test for the pipeline helper."""
import json, subprocess, sys, tempfile
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from threading import Thread

DETAIL = {
    'id': 1, 'name': 'Fixture', 'category': 'Crypto', 'type': 'standard', 'value': 100,
    'description': 'fixture', 'connection_info': None, 'files': [], 'hints': [],
}


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        path = self.path.split('?', 1)[0]
        if path == '/api/v1/challenges':
            body = json.dumps({'success': True, 'data': [DETAIL]}).encode()
        elif path == '/api/v1/challenges/1':
            body = json.dumps({'success': True, 'data': DETAIL}).encode()
        elif path == '/api/v1/users/me':
            body = json.dumps({'success': True, 'data': {'name': 'fixture'}}).encode()
        else:
            self.send_error(404); return
        self.send_response(200); self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', str(len(body))); self.end_headers(); self.wfile.write(body)

    def log_message(self, *args): pass


server = HTTPServer(('127.0.0.1', 0), Handler); Thread(target=server.serve_forever, daemon=True).start()
try:
    with tempfile.TemporaryDirectory() as td:
        root = Path(td); (root / '.ctfd').mkdir()
        (root / '.ctfd/config.json').write_text(json.dumps({'CTFD': {'URL': f'http://127.0.0.1:{server.server_port}', 'TOKEN': 'fixture'}}))
        (root / 'challenges-detailed.json').write_text(json.dumps([{'id': 1, 'name': 'Fixture', 'category': 'Crypto', 'type': 'standard', 'value': 50, 'description': 'old', 'files': [], 'hints': []}]))
        tool = Path(__file__).resolve().parents[1] / 'scripts' / 'ctf-pipeline.py'
        out = subprocess.run([sys.executable, str(tool), 'dry-run', str(root)], capture_output=True, text=True, check=True).stdout
        assert '~ modified: Fixture' in out
    print('ctfd integration fixture: OK')
finally:
    server.shutdown()

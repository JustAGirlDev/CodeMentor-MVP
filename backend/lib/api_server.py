#!/usr/bin/env python3
"""
CodeMentor REST API — Bridges frontend to backend
Run: python3 api_server.py 8080
"""

import sys, os, json, urllib.request, sqlite3, hashlib
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse

BASE = os.path.expanduser("~/CodeMentor-MVP/backend")
sys.path.insert(0, BASE)
from ai_explain import analyze_code, call_gemini, call_openrouter, call_ollama, load_config

DB_PATH = f"{BASE}/database/codementor.db"

class APIHandler(BaseHTTPRequestHandler):
    def _json_response(self, data, status=200):
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())
    
    def _read_body(self):
        length = int(self.headers.get('Content-Length', 0))
        return self.rfile.read(length).decode()
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        q = urllib.parse.parse_qs(parsed.query)
        
        if path == '/api/health':
            self._json_response({
                "status": "ok",
                "version": "3.0.0-adversarial",
                "timestamp": datetime.now().isoformat(),
                "features": ["explain", "analytics", "battle", "challenges", "leaderboard"]
            })
        
        elif path == '/api/challenges':
            conn = sqlite3.connect(DB_PATH)
            c = conn.cursor()
            diff = q.get('difficulty', [None])[0]
            if diff:
                c.execute('SELECT * FROM challenges WHERE difficulty=?', (diff,))
            else:
                c.execute('SELECT * FROM challenges ORDER BY bounty DESC')
            rows = c.fetchall()
            cols = [d[0] for d in c.description]
            conn.close()
            self._json_response([dict(zip(cols, row)) for row in rows])
        
        elif path == '/api/leaderboard':
            conn = sqlite3.connect(DB_PATH)
            c = conn.cursor()
            c.execute('SELECT user_hash, xp, level, streak_days FROM user_progress ORDER BY xp DESC LIMIT 20')
            self._json_response([
                {"user_hash": r[0][:8]+"...", "xp": r[1], "level": r[2], "streak": r[3]}
                for r in c.fetchall()
            ])
            conn.close()
        
        elif path == '/api/intel':
            conn = sqlite3.connect(DB_PATH)
            c = conn.cursor()
            c.execute('SELECT competitor, feature, our_score, their_score, timestamp FROM competitive_intel ORDER BY timestamp DESC LIMIT 50')
            self._json_response([
                {"competitor": r[0], "feature": r[1], "our_score": r[2], "their_score": r[3], "date": r[4]}
                for r in c.fetchall()
            ])
            conn.close()
        
        else:
            self._json_response({"error": "Not found"}, 404)
    
    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        body = self._read_body()
        
        try:
            data = json.loads(body) if body else {}
        except:
            self._json_response({"error": "Invalid JSON"}, 400)
            return
        
        if path == '/api/explain':
            code = data.get('code', '')
            mode = data.get('mode', 'explain')
            cfg = load_config()
            
            metrics = analyze_code(code, data.get('filepath', 'unknown'))
            
            if mode == 'analytics':
                self._json_response({
                    "html": "",  # Frontend renders metrics
                    "metrics": metrics,
                    "cached": False,
                    "timestamp": datetime.now().isoformat()
                })
                return
            
            # AI explanation (simplified — full implementation in ai_explain.py)
            if cfg.get('provider') == 'openrouter':
                html = call_openrouter(code, cfg['api_key'], cfg.get('model'))
            elif cfg.get('provider') == 'ollama':
                html = call_ollama(code, cfg.get('endpoint'), cfg.get('model'))
            else:
                html = call_gemini(code, cfg['api_key'], cfg.get('model'))
            
            self._json_response({
                "html": html,
                "metrics": metrics,
                "cached": False,
                "timestamp": datetime.now().isoformat()
            })
        
        elif path == '/api/battle':
            # Store battle request, return async ID
            battle_id = hashlib.sha256(f"{data['code']}{datetime.now()}".encode()).hexdigest()[:16]
            self._json_response({
                "battle_id": battle_id,
                "status": "queued",
                "check_url": f"/api/battle/{battle_id}"
            })
        
        else:
            self._json_response({"error": "Not found"}, 404)
    
    def log_message(self, format, *args):
        pass  # Quiet mode

if __name__ == '__main__':
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8080
    server = HTTPServer(('', port), APIHandler)
    print(f"CodeMentor API v3.0 on port {port}")
    print(f"Dashboard: http://localhost:{port}/api/health")
    server.serve_forever()

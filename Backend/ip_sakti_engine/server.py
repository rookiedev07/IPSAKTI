"""
IP-SAKTI Unified Pipeline HTTP Server
Exposes POST /api/pipeline/evaluate on port 8000
"""

import os
import sys
import json
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse

from unified_pipeline import evaluate_full_pipeline

PORT = 8000


class PipelineRequestHandler(BaseHTTPRequestHandler):
    def _set_headers(self, status=200):
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")
        self.end_headers()

    def do_OPTIONS(self):
        self._set_headers(200)

    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path == "/api/health" or parsed.path == "/":
            self._set_headers(200)
            resp = {
                "status": "ok",
                "service": "IP-SAKTI Unified Pipeline Engine (Layers 5-9)",
                "framework": "House of Cards"
            }
            self.wfile.write(json.dumps(resp).encode("utf-8"))
        else:
            self._set_headers(404)
            self.wfile.write(json.dumps({"error": "Not Found"}).encode("utf-8"))

    def do_POST(self):
        parsed = urlparse(self.path)
        if parsed.path == "/api/pipeline/evaluate":
            try:
                content_len = int(self.headers.get("Content-Length", 0))
                body_bytes = self.rfile.read(content_len)
                data = json.loads(body_bytes.decode("utf-8")) if body_bytes else {}
                
                prompt = data.get("prompt", "")
                deliverable = data.get("deliverable", "")
                language = data.get("language", "en")
                
                result = evaluate_full_pipeline(prompt, deliverable, language)
                self._set_headers(200)
                self.wfile.write(json.dumps(result, ensure_ascii=False).encode("utf-8"))
            except Exception as e:
                self._set_headers(500)
                self.wfile.write(json.dumps({"error": str(e)}).encode("utf-8"))
        else:
            self._set_headers(404)
            self.wfile.write(json.dumps({"error": "Not Found"}).encode("utf-8"))


def run_server():
    server_address = ("127.0.0.1", PORT)
    httpd = HTTPServer(server_address, PipelineRequestHandler)
    print(f"♠ IP-SAKTI Unified Engine running on http://127.0.0.1:{PORT}")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n♠ Server shutting down...")
        httpd.server_close()


if __name__ == "__main__":
    run_server()

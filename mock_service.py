"""Lightweight mock HTTP service for local testing and demonstration.

Serves:
  - GET http://localhost:5000/       -> 200 OK (Homepage)
  - GET http://localhost:5000/health -> 200 OK (Health Check)
"""

import json
from http.server import BaseHTTPRequestHandler, HTTPServer
import os

PORT = int(os.getenv("APP_PORT", 5000))
HOST = os.getenv("APP_HOST", "127.0.0.1")


class MockDevOpsHandler(BaseHTTPRequestHandler):
    def _send_json_response(self, status: int, data: dict):
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode("utf-8"))

    def do_GET(self):
        if self.path == "/" or self.path == "":
            self._send_json_response(200, {
                "message": "Welcome to inventory-service",
                "status": "online",
                "version": "1.0.0"
            })
        elif self.path == "/health":
            self._send_json_response(200, {
                "status": "healthy",
                "uptime_seconds": 3600,
                "database": "connected"
            })
        else:
            self._send_json_response(404, {"error": "Not Found"})

    def log_message(self, format, *args):
        # Quiet standard HTTP server logs to keep console clean
        return


def run_mock_server():
    server_address = (HOST, PORT)
    httpd = HTTPServer(server_address, MockDevOpsHandler)
    print(f"[*] Mock DevOps service running on http://{HOST}:{PORT}")
    print("    - Root:   http://{HOST}:{PORT}/")
    print("    - Health: http://{HOST}:{PORT}/health")
    print("    Press Ctrl+C to stop.")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n[*] Shutting down mock service...")
        httpd.server_close()


if __name__ == "__main__":
    run_mock_server()

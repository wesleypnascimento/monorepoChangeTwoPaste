import json
import os
from http.server import BaseHTTPRequestHandler, HTTPServer


class NameHandler(BaseHTTPRequestHandler):
    def _send_json(self, status, data):
        body = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        self._send_json(404, {"error": "Rota não encontrada."})

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_POST(self):
        if self.path != "/api/name":
            self._send_json(404, {"error": "Rota não encontrada."})
            return

        try:
            content_length = int(self.headers.get("Content-Length", "0"))
            data = json.loads(self.rfile.read(content_length))
        except (ValueError, json.JSONDecodeError, UnicodeDecodeError):
            self._send_json(400, {"error": "Envie um JSON válido."})
            return
        # Validate that the data is a dictionary 1 2 3 4 5 6 7 8 9
        if not isinstance(data, dict):
            self._send_json(400, {"error": "Envie um objeto com nome e sobrenome."})
            return
        # Validate that the required fields are present and are strings
        first_name = data.get("firstName")
        last_name = data.get("lastName")
        if not isinstance(first_name, str) or not isinstance(last_name, str):
            self._send_json(400, {"error": "Preencha o nome e o sobrenome."})
            return
        # Strip leading and trailing whitespace from the names
        first_name = first_name.strip()
        last_name = last_name.strip()
        if not first_name or not last_name:
            self._send_json(400, {"error": "Preencha o nome e o sobrenome."})
            return

        self._send_json(200, {"fullName": f"{first_name} {last_name}"})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "3000"))
    server = HTTPServer(("127.0.0.1", port), NameHandler)
    print(f"Servidor disponível em http://localhost:{port}")
    server.serve_forever()

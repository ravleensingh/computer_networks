from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import sys

BACKEND = sys.argv[1].upper() if len(sys.argv) > 1 else "A"
if len(sys.argv) > 2:
    PORT = int(sys.argv[2])
else:
    PORT = 3001 if BACKEND == "A" else 3002

ETAG = '"cache-v1"'

class Handler(BaseHTTPRequestHandler):
    def send_json(self, status, payload, cache=False):
        if status == 304:
            body = b""
        else:
            body = json.dumps(payload).encode("utf-8")

        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("X-Backend", BACKEND)

        if cache:
            self.send_header("Cache-Control", "max-age=60")
            self.send_header("ETag", ETAG)

        self.end_headers()

        if status != 304 and self.command != "HEAD":
            self.wfile.write(body)

    def do_HEAD(self):
        self.do_GET()

    def do_GET(self):
        if self.path == "/":
            self.send_json(200, {
                "backend": BACKEND,
                "message": "CN project backend is running"
            })
            return

        if self.path == "/api/status":
            self.send_json(200, {
                "backend": BACKEND,
                "status": "ok"
            })
            return

        if self.path == "/api/cache":
            if self.headers.get("If-None-Match") == ETAG:
                self.send_json(304, {}, cache=True)
                return
            self.send_json(200, {
                "backend": BACKEND,
                "cached": True
            }, cache=True)
            return

        self.send_json(404, {
            "backend": BACKEND,
            "error": "not found"
        })

    def log_message(self, format, *args):
        print(f"[{BACKEND}] {self.address_string()} - {format % args}")

server = ThreadingHTTPServer(("0.0.0.0", PORT), Handler)
print(f"Backend {BACKEND} listening on 0.0.0.0:{PORT}")
server.serve_forever()

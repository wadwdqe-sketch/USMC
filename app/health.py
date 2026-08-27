"""Tiny HTTP health server for Railway health checks."""

from __future__ import annotations

from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from threading import Thread

from .config import Settings


class HealthHandler(BaseHTTPRequestHandler):
    """Return a simple successful response for Railway."""

    def do_GET(self) -> None:  # noqa: N802 - required by BaseHTTPRequestHandler
        if self.path != "/health":
            self.send_error(404, "Not found")
            return

        body = b'{"status":"ok"}'
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format: str, *args: object) -> None:
        print(f"health - {format % args}")


def start_health_server(settings: Settings) -> Thread:
    """Start the health endpoint in a daemon thread."""
    server = ThreadingHTTPServer((settings.host, settings.port), HealthHandler)
    thread = Thread(target=server.serve_forever, name="health-server", daemon=True)
    thread.start()
    return thread
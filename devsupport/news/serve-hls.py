#! /usr/bin/env python3

from http.server import HTTPServer, SimpleHTTPRequestHandler

class CORSRequestHandler(SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")  # Allow all origins
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")  # Allowed methods
        self.send_header("Access-Control-Allow-Headers", "*")  # Allow all headers
        super().end_headers()

if __name__ == "__main__":
    port = 5005
    server_address = ("", port)
    httpd = HTTPServer(server_address, CORSRequestHandler)
    print(f"Serving on port {port} with CORS enabled...")
    httpd.serve_forever()

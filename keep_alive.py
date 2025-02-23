from http.server import BaseHTTPRequestHandler, HTTPServer
import asyncio

class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b"I'm alive")

async def run_server():
    loop = asyncio.get_running_loop()
    server_address = ('', 8080)
    httpd = HTTPServer(server_address, SimpleHandler)
    
    print("Server running on port 8080...")
    await loop.run_in_executor(None, httpd.serve_forever)

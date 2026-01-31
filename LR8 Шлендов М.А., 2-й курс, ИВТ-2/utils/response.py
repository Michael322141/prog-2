from http import HTTPStatus
from http.server import BaseHTTPRequestHandler

def respond_bytes(handler: BaseHTTPRequestHandler, b: bytes, mime_type: str, status: HTTPStatus = HTTPStatus.OK):
    handler.send_response(status)
    handler.send_header('Content-Type', mime_type)
    handler.send_header('Content-Length', len(b))
    handler.end_headers()
    handler.wfile.write(b)

def respond_html(handler: BaseHTTPRequestHandler, html: str, status: HTTPStatus = HTTPStatus.OK):
    respond_bytes(handler, html.encode('utf-8'), 'text/html', status=status)
    
def redirect(handler: BaseHTTPRequestHandler, url: str):
    handler.send_response(301)
    handler.send_header('Location', url)
    handler.end_headers()
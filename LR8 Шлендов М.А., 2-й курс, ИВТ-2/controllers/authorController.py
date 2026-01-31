from http.server import BaseHTTPRequestHandler

from utils.response import *

from jinja2.environment import Environment

from common import APP, PAGES

class AuthorController:
    def __init__(self, handler: BaseHTTPRequestHandler, env: Environment):
        self.handler = handler
        self.template_index = env.get_template("index.html")
        self.template_author = env.get_template("author.html")
    
    def handle_get(self, path: str, params: dict) -> bool:
        if path == '':
            self._handle_index(params)
            return True
        if path == '/author':
            self._handle_author(params)
            return True
        
        return False
    
    def _handle_index(self, params: dict):
        data = params | {
            'app': APP,
            'pages': PAGES
        }
        respond_html(self.handler, self.template_index.render(data))
    
    def _handle_author(self, params: dict):
        data = params | {
            'app': APP,
            'pages': PAGES
        }
        respond_html(self.handler, self.template_author.render(data))
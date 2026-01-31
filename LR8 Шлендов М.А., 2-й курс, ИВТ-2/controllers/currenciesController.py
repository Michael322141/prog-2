from http.server import BaseHTTPRequestHandler
from jinja2.environment import Environment

from utils.response import *

from controllers.databaseController import CurrencyDatabase

from common import APP, PAGES

class CurrenciesController:
    def __init__(self, handler: BaseHTTPRequestHandler, db: CurrencyDatabase, env: Environment):
        self.handler = handler
        self.db = db
        self.template_currencies = env.get_template('currencies.html')
    
    def handle_get(self, path: str, params: dict) -> bool:
        if path == '/currencies':
            self._handle_currencies(params)
            return True
        if path == '/currency/delete':
            self._handle_delete(params)
            return True
        if path == '/currency/update':
            self._handle_update(params)
            return True
        if path == '/currency/show':
            self._handle_show()
            return True
        
        return False
    
    def _handle_currencies(self, params: dict):
        currencies = self.db.get_all()
        data = params | {
            'app': APP,
            'pages': PAGES,
            'currencies': currencies,
        }
        respond_html(self.handler, self.template_currencies.render(data))
        
    def _handle_delete(self, params: dict):
        id = params.get('id')
        if id is None:
            self.handler.send_response(HTTPStatus.BAD_REQUEST)
            return
            
        try:
            id = int(id)
        except ValueError:
            self.handler.send_response(HTTPStatus.BAD_REQUEST)
            return
    
        self.db.delete(id=id)
        self.handler.send_response(HTTPStatus.OK)
    
    def _handle_update(self, params: dict):
        for char_code, value in params.items():
            try:
                value = float(value)
            except ValueError:
                continue
            self.db.update_by_char_code(char_code, value)
        self.handler.send_response(HTTPStatus.OK)
    
    def _handle_show(self):
        currencies = self.db.get_all()
        for currency in currencies:
            print(currency)
        self.handler.send_response(HTTPStatus.OK)
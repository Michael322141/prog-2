from http.server import BaseHTTPRequestHandler

from jinja2.environment import Environment

from utils.response import *
from common import APP, PAGES

from controllers.databaseController import UserDatabase, UserCurrencyDatabase, CurrencyDatabase

class UserController:
    def __init__(self, handler: BaseHTTPRequestHandler, users_db: UserDatabase, user_currencies_db: UserCurrencyDatabase, currencies_db: CurrencyDatabase, env: Environment):
        self.handler = handler
        self.users_db = users_db
        self.user_currencies_db = user_currencies_db
        self.currencies_db = currencies_db
        self.template_users = env.get_template('users.html')
        self.template_user = env.get_template('user.html')
    
    def handle_get(self, path: str, params: dict) -> bool:
        if path == '/users':
            self._handle_users(params)
            return True
        if path == '/user':
            self._handle_user(params)
            return True
        
        return False
    
    def _handle_users(self, params: dict):
        users = self.users_db.get_all()
        data = params | {
            'app': APP,
            'pages': PAGES,
            'users': users,
        }
        respond_html(self.handler, self.template_users.render(data))
    
    def _handle_user(self, params: dict):
        id = params.get('id')
        if id is None:
            redirect(self.handler, '/users')
            return
        
        try:
            id = int(id)
        except ValueError:
            self.handler.send_response(HTTPStatus.BAD_REQUEST)
            return
        
        user = self.users_db.get_by_id(int(id))
        if user is None:
            self.handler.send_response(HTTPStatus.NOT_FOUND)
            return
        
        user_currencies = self.user_currencies_db.get_by_user_id(user.id)
        currencies = map(lambda uc: self.currencies_db.get_by_id(uc.currency_id), user_currencies)
        
        data = params | {
            'app': APP,
            'pages': PAGES,
            'user': user,
            'currencies': currencies
        }
        respond_html(self.handler, self.template_user.render(data))
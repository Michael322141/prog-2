from http.server import HTTPServer, BaseHTTPRequestHandler
from jinja2 import Environment, FileSystemLoader, select_autoescape
from urllib.parse import parse_qsl
from pathlib import Path
from utils.currencies_api import get_currencies

from models.app import App
from models.author import Author
from models.user import User
from models.user_currency import UserCurrency

PAGES = (
    {
        'caption': 'Главная',
        'href': '/'
    },
    {
        'caption': 'Курсы',
        'href': '/currencies'
    },
    {
        'caption': 'Пользователи',
        'href': '/users'
    },
    {
        'caption': 'Автор',
        'href': '/author'
    },
)

APP = App('Актуальные курсы валют', '0.0.1', Author('Шлендов Михаил', 'ИВТ-2'))

USERS = (
    User(1, 'Илон Маск'),
    User(2, 'Дональд Трамп'),
    User(3, 'Барак Обама'),
)

USER_CURRENCIES = (
    UserCurrency(1, 1, 'R01235'),
    UserCurrency(2, 1, 'R01375'),
    UserCurrency(3, 1, 'R01035'),
    
    UserCurrency(4, 2, 'R01235'),
    UserCurrency(5, 2, 'R01375'),
    UserCurrency(6, 2, 'R01035'),
    
    UserCurrency(7, 3, 'R01235'),
)

MIME_TYPES: dict = {
    '.css': 'text/css',
    '.html': 'text/html',
    '.js': 'text/javascript'
}

env = Environment(
    loader=FileSystemLoader('./templates/'),
    autoescape=select_autoescape()
)

template_index = env.get_template("index.html")
template_users = env.get_template("users.html")
template_user = env.get_template("user.html")
template_author = env.get_template("author.html")
template_currencies = env.get_template("currencies.html")

def respond_bytes(handler: BaseHTTPRequestHandler, b: bytes, mime_type: str, status: int = 200):
    handler.send_response(status)
    handler.send_header('Content-Type', mime_type)
    handler.send_header('Content-Length', len(b))
    handler.end_headers()
    handler.wfile.write(b)

def respond_html(handler: BaseHTTPRequestHandler, html: str, status: int = 200):
    respond_bytes(handler, html.encode('utf-8'), 'text/html', status=status)

class HttpHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        path = self.path
        if len(path) > 1:
            path = path.removesuffix('/')

        params = {}

        i = self.path.find('?')
        if i >= 0:
            path = self.path[:i]
            params = dict(parse_qsl(self.path[(i + 1):]))

        if path == '/':
            self.index(params)
        elif path == '/users':
            self.users(params)
        elif path == '/user':
            self.user(params)
        elif path == '/currencies':
            self.currencies(params)
        elif path == '/author':
            self.author(params)
        elif path.startswith('/static'):
            self.serve_static(path.removeprefix('/static'))
        else:
            self.send_response(404)

    def do_POST(self):
        pass

    def index(self, params: dict):
        data = params | {
            'app': APP,
            'pages': PAGES
        }
        respond_html(self, template_index.render(data))

    def users(self, params: dict):
        data = params | {
            'app': APP,
            'pages': PAGES,
            'users': USERS,
        }
        respond_html(self, template_users.render(data))
        
    def user(self, params: dict):
        id = params.get('id')
        if id is None:
            self.redirect('/users')
            return
        
        user = next((u for u in USERS if str(u.id) == id), None)
        if user is None:
            self.send_response(404)
            return
        
        user_currencies = filter(lambda uc: str(uc.user_id) == id, USER_CURRENCIES)
        currencies = get_currencies(list(map(lambda uc: uc.currency_id, user_currencies)))
        
        print(currencies)
        
        data = params | {
            'app': APP,
            'pages': PAGES,
            'user': user,
            'currencies': currencies
        }
        respond_html(self, template_user.render(data))

    def currencies(self, params: dict):
        currencies = get_currencies()
        data = params | {
            'app': APP,
            'pages': PAGES,
            'currencies': currencies,
        }
        respond_html(self, template_currencies.render(data))

    def author(self, params: dict):
        data = params | {
            'app': APP,
            'pages': PAGES
        }
        respond_html(self, template_author.render(data))

    def serve_static(self, path: str):
        p = Path(path)
        mime_type = MIME_TYPES.get(p.suffix, "application/octet-stream")
        try:
            with open('./static' + path, 'rb') as f:
                respond_bytes(self, f.read(), mime_type)
        except IsADirectoryError:
            self.send_response(403)
        except FileNotFoundError:
            self.send_response(404)
            
    def redirect(self, url: str):
        self.send_response(301)
        self.send_header('Location', url)
        self.end_headers()

def run_server(address: str, port: int):
    HTTPServer((address, port), HttpHandler).serve_forever()

def main():
    run_server('', 1234)

if __name__ == "__main__":
    main()

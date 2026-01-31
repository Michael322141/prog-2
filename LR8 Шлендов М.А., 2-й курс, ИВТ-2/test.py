import unittest
from unittest.mock import MagicMock, PropertyMock, call

from io import BytesIO
from jinja2 import Environment, FileSystemLoader, select_autoescape

from http import HTTPStatus

from utils.currencies_api import get_currencies
from models.currency import Currency
from models.user import User
from models.user_currency import UserCurrency
from main import HttpHandler

from common import APP, PAGES

from controllers.currenciesController import CurrenciesController
from controllers.authorController import AuthorController
from controllers.userController import UserController

class MockRequest:
    def __init__(self, request: str):
        self.request = request.encode('utf-8')
    
    def makefile(self, *args, **kwargs):
        return BytesIO(self.request)
    
    def sendall(self, *args, **kwargs):
        pass

class TestHttpHandler(HttpHandler):
    wbufsize = 1
    
    def finish(self):
        self.wfile.flush()
        self.rfile.close()
        
    def version_string(self):
        return "TestServer"
    
    def date_time_string(self, timestamp = None):
        return "123"

class Test(unittest.TestCase):
    def setUp(self):
        self.maxDiff = 9999
        
        self.env = Environment(
            loader=FileSystemLoader('./templates/'),
            autoescape=select_autoescape()
        )

        self.template_index = self.env.get_template("index.html")
        self.template_users = self.env.get_template("users.html")
        self.template_user = self.env.get_template("user.html")
        self.template_author = self.env.get_template("author.html")
        self.template_currencies = self.env.get_template("currencies.html")
        
        self.mock_currencies_db = MagicMock()
        self.mock_currencies_db.get_all.return_value = [Currency('1', 'USD', 'Доллар', 75, 1), Currency('2', 'EUR', 'Евро', 90, 1)]
        self.mock_currencies_db.get_by_id.return_value = Currency('1', 'USD', 'Доллар', 75, 1)
        self.mock_currencies_db.update_by_char_code.return_value = None
        self.mock_currencies_db.delete.return_value = None
        
        self.mock_users_db = MagicMock()
        self.mock_users_db.get_all.return_value = [User(1, "Вася"), User(2, "Петя"), User(3, 'Дима')]
        self.mock_users_db.get_by_id.return_value = User(1, "Вася")
        self.mock_users_db.delete.return_value = None
        
        self.mock_user_currencies_db = MagicMock()
        self.mock_user_currencies_db.get_all.return_value = [UserCurrency(1, "1", 1), UserCurrency(2, "1", 2), UserCurrency(3, "2", 3)]
        self.mock_user_currencies_db.get_by_user_id.return_value = [UserCurrency(1, "1", 1)]
        self.mock_user_currencies_db.delete.return_value = None
    
    def test_get_currencies(self):
        currencies = get_currencies(['R01235', 'R01375'])
        self.assertEqual(len(currencies), 2)
        
        for currency in currencies:
            self.assertIsInstance(currency, Currency)

    def test_get_currencies_wrong_id(self):
        result = get_currencies(['KEK'])
        self.assertEqual(len(result), 0)
        
    def test_author_controller(self):
        buffer = BytesIO()
        
        handler = MagicMock()
        handler.send_response.return_value = None
        handler.send_header.return_value = None
        handler.end_headers.return_value = None
        type(handler).wfile = PropertyMock(return_value=buffer)
        
        author_controller = AuthorController(handler=handler, env=self.env)
        
        response = author_controller.handle_get('', params={})
        self.assertTrue(response)
        
        template = self.template_index.render({'app': APP, 'pages': PAGES}).encode()
        handler.send_response.assert_called_with(200)
        handler.send_header.assert_has_calls(calls=[call('Content-Type', 'text/html'), call('Content-Length', len(template))])
        self.assertEqual(buffer.getvalue(), template)
        buffer.seek(0)
        
        response = author_controller.handle_get('/author', params={})
        self.assertTrue(response)
        
        template = self.template_author.render({'app': APP, 'pages': PAGES}).encode()
        handler.send_response.assert_called_with(200)
        handler.send_header.assert_has_calls(calls=[call('Content-Type', 'text/html'), call('Content-Length', len(template))])
        self.assertEqual(buffer.getvalue(), template)
        
    def test_currencies_controller(self):
        buffer = BytesIO()
        
        handler = MagicMock()
        handler.send_response.return_value = None
        handler.send_header.return_value = None
        handler.end_headers.return_value = None
        type(handler).wfile = PropertyMock(return_value=buffer)
        
        currencies_controller = CurrenciesController(handler=handler, db=self.mock_currencies_db, env=self.env)
        
        response = currencies_controller.handle_get('/currencies', params={})
        self.assertIsNotNone(response)
        
        template = self.template_currencies.render({
            'app': APP,
            'pages': PAGES,
            'currencies': [Currency('1', 'USD', 'Доллар', 75, 1), Currency('2', 'EUR', 'Евро', 90, 1)]
        }).encode()
        
        handler.send_response.assert_called_with(200)
        handler.send_header.assert_has_calls(calls=[call('Content-Type', 'text/html'), call('Content-Length', len(template))])
        self.assertEqual(buffer.getvalue(), template)
        buffer.seek(0)
        
        
        response = currencies_controller.handle_get('/currency/delete', params={'id': 1})
        self.assertIsNotNone(response)
        handler.send_response.assert_called_with(200)
        
        
        response = currencies_controller.handle_get('/currency/update', params={'USD': 250})
        self.assertIsNotNone(response)        
        handler.send_response.assert_called_with(200)
        
        
        self.mock_currencies_db.get_all.assert_called_once()
        self.mock_currencies_db.delete.assert_called_once_with(id=1)
        self.mock_currencies_db.update_by_char_code.assert_called_once_with('USD', 250.0)
        
    def test_users_controller(self):
        buffer = BytesIO()
        
        handler = MagicMock()
        handler.send_response.return_value = None
        handler.send_header.return_value = None
        handler.end_headers.return_value = None
        type(handler).wfile = PropertyMock(return_value=buffer)
        
        user_controller = UserController(handler=handler, users_db=self.mock_users_db, currencies_db=self.mock_currencies_db, user_currencies_db=self.mock_user_currencies_db, env=self.env)
        
        response = user_controller.handle_get('/users', params={})
        self.assertIsNotNone(response)
        
        template = self.template_users.render({
            'app': APP,
            'pages': PAGES,
            'users': [User(1, "Вася"), User(2, "Петя"), User(3, 'Дима')]
        }).encode()
        
        handler.send_response.assert_called_with(200)
        handler.send_header.assert_has_calls(calls=[call('Content-Type', 'text/html'), call('Content-Length', len(template))])
        self.assertEqual(buffer.getvalue(), template)
        buffer.seek(0)
        
        
        response = user_controller.handle_get('/user', params={'id': 1})
        self.assertIsNotNone(response)
        
        template = self.template_user.render({
            'app': APP,
            'pages': PAGES,
            'user': User(1, "Вася"),
            'currencies': [Currency('1', 'USD', 'Доллар', 75, 1)]
        }).encode()
        
        handler.send_response.assert_called_with(200)
        handler.send_header.assert_has_calls(calls=[call('Content-Type', 'text/html'), call('Content-Length', len(template))])
        self.assertEqual(buffer.getvalue(), template)
        buffer.seek(0)
        
        
        self.mock_users_db.get_all.assert_called_once()
        self.mock_users_db.get_by_id.assert_called_once_with(1)

if __name__ == '__main__':
    unittest.main()

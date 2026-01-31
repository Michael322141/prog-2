import unittest
from io import BytesIO
from jinja2 import Environment, FileSystemLoader, select_autoescape

from utils.currencies_api import get_currencies
from models.currency import Currency
from main import HttpHandler, APP, PAGES, USERS, USER_CURRENCIES

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
        
        env = Environment(
            loader=FileSystemLoader('./templates/'),
            autoescape=select_autoescape()
        )

        self.template_index = env.get_template("index.html")
        self.template_users = env.get_template("users.html")
        self.template_user = env.get_template("user.html")
        self.template_author = env.get_template("author.html")
        self.template_currencies = env.get_template("currencies.html")
    
    def test1(self):
        currencies = get_currencies(['R01235', 'R01375'])
        self.assertEqual(len(currencies), 2)
        
        for currency in currencies:
            self.assertIsInstance(currency, Currency)

    def test2(self):
        result = get_currencies(['KEK'])
        self.assertEqual(len(result), 0)
        
    def test3(self):
        handler = TestHttpHandler(MockRequest("GET / HTTP/1.1"), client_address=("127.0.0.1", 1234), server=self)
        result: bytes = handler.wfile.getvalue()
        template = self.template_index.render({'app': APP, 'pages': PAGES}).encode('utf-8')
        header = f"HTTP/1.0 200 OK\r\nServer: TestServer\r\nDate: 123\r\nContent-Type: text/html\r\nContent-Length: {len(template)}\r\n\r\n".encode('utf-8')
        self.assertEqual(result, header + template)
        
    def test4(self):
        handler = TestHttpHandler(MockRequest("GET /users HTTP/1.1"), client_address=("127.0.0.1", 1234), server=self)
        result: bytes = handler.wfile.getvalue()
        template = self.template_users.render({'app': APP, 'pages': PAGES, 'users': USERS}).encode('utf-8')
        header = f"HTTP/1.0 200 OK\r\nServer: TestServer\r\nDate: 123\r\nContent-Type: text/html\r\nContent-Length: {len(template)}\r\n\r\n".encode('utf-8')
        self.assertEqual(result, header + template)
        
    def test5(self):
        USER_ID = USERS[0].id
        handler = TestHttpHandler(MockRequest(f"GET /user?id={USER_ID} HTTP/1.1"), client_address=("127.0.0.1", 1234), server=self)
        result: bytes = handler.wfile.getvalue()
        
        user = USERS[0]
        
        user_currencies = filter(lambda uc: uc.user_id == USER_ID, USER_CURRENCIES)
        currencies = get_currencies(list(map(lambda uc: uc.currency_id, user_currencies)))
        
        template = self.template_user.render({'app': APP, 'pages': PAGES, 'user': user, 'currencies': currencies}).encode('utf-8')
        header = f"HTTP/1.0 200 OK\r\nServer: TestServer\r\nDate: 123\r\nContent-Type: text/html\r\nContent-Length: {len(template)}\r\n\r\n".encode('utf-8')
        self.assertEqual(result, header + template)
        
    def test6(self):
        handler = TestHttpHandler(MockRequest("GET /user?id=42343 HTTP/1.1"), client_address=("127.0.0.1", 1234), server=self)
        result: bytes = handler.wfile.getvalue()
        header = "HTTP/1.0 404 Not Found\r\nServer: TestServer\r\nDate: 123\r\n\r\n".encode('utf-8')
        self.assertEqual(result, header)
        
    def test7(self):
        handler = TestHttpHandler(MockRequest("GET /currencies HTTP/1.1"), client_address=("127.0.0.1", 1234), server=self)
        result: bytes = handler.wfile.getvalue()
        currencies = get_currencies()
        template = self.template_currencies.render({'app': APP, 'pages': PAGES, 'currencies': currencies}).encode('utf-8')
        header = f"HTTP/1.0 200 OK\r\nServer: TestServer\r\nDate: 123\r\nContent-Type: text/html\r\nContent-Length: {len(template)}\r\n\r\n".encode('utf-8')
        self.assertEqual(result, header + template)
        
    def test8(self):
        handler = TestHttpHandler(MockRequest("GET /author HTTP/1.1"), client_address=("127.0.0.1", 1234), server=self)
        result: bytes = handler.wfile.getvalue()
        template = self.template_author.render({'app': APP, 'pages': PAGES}).encode('utf-8')
        header = f"HTTP/1.0 200 OK\r\nServer: TestServer\r\nDate: 123\r\nContent-Type: text/html\r\nContent-Length: {len(template)}\r\n\r\n".encode('utf-8')
        self.assertEqual(result, header + template)

if __name__ == '__main__':
    unittest.main()

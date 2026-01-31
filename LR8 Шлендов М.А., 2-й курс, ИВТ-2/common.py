from models.app import App
from models.author import Author

APP = App('Актуальные курсы валют', '0.0.1', Author('Шлендов Михаил', 'ИВТ-2'))
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
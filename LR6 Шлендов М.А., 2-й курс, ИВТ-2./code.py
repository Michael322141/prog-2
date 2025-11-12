import requests
import sys
import logging
from functools import wraps
from typing import List, Dict, Optional
from unittest.mock import patch, MagicMock
import io
import contextlib

# Настройка логирования для итерации 3
logging.basicConfig(
    level=logging.ERROR,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

def log_errors(func):
    """Декоратор для логирования ошибок (Итерация 2 и 3)"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except requests.RequestException as e:
            # Логирование в sys.stdout (Итерация 1)
            print(f"Ошибка запроса к API: {e}", file=sys.stdout)
            # Логирование через logging (Итерация 3)
            logging.error(f"Ошибка запроса к API: {e}")
            return None
        except KeyError as e:
            print(f"В ответе API отсутствуют ожидаемые данные: {e}", file=sys.stdout)
            logging.error(f"В ответе API отсутствуют ожидаемые данные: {e}")
            return None
        except ValueError as e:
            print(f"Ошибка данных: {e}", file=sys.stdout)
            logging.error(f"Ошибка данных: {e}")
            return None
        except Exception as e:
            print(f"Неожиданная ошибка: {e}", file=sys.stdout)
            logging.error(f"Неожиданная ошибка: {e}")
            return None
    return wrapper

@log_errors
def get_currencies(currency_codes: List[str], url: str = "https://www.cbr-xml-daily.ru/daily_json.js") -> Optional[Dict[str, float]]:
    """
    Получает курсы валют из API Центробанка РФ.
    
    Args:
        currency_codes: Список символьных кодов валют (например, ['USD', 'EUR'])
        url: URL API (по умолчанию API ЦБ РФ)
    
    Returns:
        Словарь с курсами валют или None в случае ошибки
    """
    if not currency_codes:
        raise ValueError("Список кодов валют не может быть пустым")
    
    # Выполнение запроса к API
    response = requests.get(url)
    response.raise_for_status()  # Вызовет requests.RequestException при ошибке HTTP
    
    data = response.json()
    
    # Проверка наличия курсов валют в ответе
    if 'Valute' not in data:
        raise KeyError("В ответе API отсутствуют курсы валют (ключ 'Valute')")
    
    valutes = data['Valute']
    result = {}
    
    # Получение курсов для запрошенных валют
    for code in currency_codes:
        if code not in valutes:
            raise ValueError(f"Валюта с кодом '{code}' не найдена в ответе API")
        
        currency_data = valutes[code]
        if 'Value' not in currency_data:
            raise KeyError(f"В данных для валюты '{code}' отсутствует курс (ключ 'Value')")
        
        result[code] = currency_data['Value']
    
    return result

# ТЕСТИРОВАНИЕ
import unittest

class TestGetCurrencies(unittest.TestCase):
    
    def setUp(self):
        """Подготовка тестовых данных"""
        self.valid_currency_codes = ['USD', 'EUR', 'GBP']
        self.test_url = "https://www.cbr-xml-daily.ru/daily_json.js"
        
        # Пример корректного ответа API
        self.valid_api_response = {
            'Valute': {
                'USD': {'Value': 75.50, 'Name': 'Доллар США'},
                'EUR': {'Value': 82.30, 'Name': 'Евро'},
                'GBP': {'Value': 95.20, 'Name': 'Фунт стерлингов'},
                'JPY': {'Value': 0.65, 'Name': 'Японская иена'}
            }
        }
    
    def test_successful_response_keys_and_values(self):
        """Проверка ключей и значений возвращаемого словаря при успешном запросе"""
        with patch('requests.get') as mock_get:
            # Мокаем успешный ответ API
            mock_response = MagicMock()
            mock_response.json.return_value = self.valid_api_response
            mock_response.raise_for_status.return_value = None
            mock_get.return_value = mock_response
            
            # Вызываем функцию
            result = get_currencies(self.valid_currency_codes)
            
            # Проверяем, что результат не None
            self.assertIsNotNone(result)
            
            # Проверяем ключи
            expected_keys = set(self.valid_currency_codes)
            actual_keys = set(result.keys())
            self.assertEqual(expected_keys, actual_keys)
            
            # Проверяем значения
            self.assertIsInstance(result['USD'], float)
            self.assertIsInstance(result['EUR'], float)
            self.assertIsInstance(result['GBP'], float)
            
            # Проверяем конкретные значения
            self.assertEqual(result['USD'], 75.50)
            self.assertEqual(result['EUR'], 82.30)
            self.assertEqual(result['GBP'], 95.20)
    
    def test_partial_currency_codes(self):
        """Проверка работы с подмножеством доступных валют"""
        with patch('requests.get') as mock_get:
            mock_response = MagicMock()
            mock_response.json.return_value = self.valid_api_response
            mock_response.raise_for_status.return_value = None
            mock_get.return_value = mock_response
            
            # Запрашиваем только одну валюту
            result = get_currencies(['USD'])
            
            self.assertIsNotNone(result)
            self.assertEqual(len(result), 1)
            self.assertIn('USD', result)
            self.assertEqual(result['USD'], 75.50)
    
    def test_empty_currency_codes_exception(self):
        """Проверка обработки исключения при пустом списке валют"""
        with patch('requests.get') as mock_get:
            # Захватываем вывод для проверки логов
            with self.assertLogs(level='ERROR') as log_context:
                with io.StringIO() as buffer:
                    with contextlib.redirect_stdout(buffer):
                        result = get_currencies([])
            
            # Проверяем, что функция вернула None
            self.assertIsNone(result)
            
            # Проверяем, что в логах есть сообщение об ошибке
            self.assertTrue(any('Ошибка данных' in record.message 
                              for record in log_context.records))
    
    def test_nonexistent_currency_exception(self):
        """Проверка обработки исключения при запросе несуществующей валюты"""
        with patch('requests.get') as mock_get:
            mock_response = MagicMock()
            mock_response.json.return_value = self.valid_api_response
            mock_response.raise_for_status.return_value = None
            mock_get.return_value = mock_response
            
            # Захватываем вывод для проверки логов
            with self.assertLogs(level='ERROR') as log_context:
                with io.StringIO() as buffer:
                    with contextlib.redirect_stdout(buffer):
                        result = get_currencies(['XYZ'])
            
            # Проверяем, что функция вернула None
            self.assertIsNone(result)
            
            # Проверяем запись в логах
            self.assertTrue(any("Валюта с кодом 'XYZ' не найдена" in record.message 
                              for record in log_context.records))
    
    def test_api_response_missing_valute_key(self):
        """Проверка обработки исключения при отсутствии ключа Valute в ответе API"""
        with patch('requests.get') as mock_get:
            # Мокаем ответ без ключа Valute
            mock_response = MagicMock()
            mock_response.json.return_value = {}  # Пустой ответ
            mock_response.raise_for_status.return_value = None
            mock_get.return_value = mock_response
            
            with self.assertLogs(level='ERROR') as log_context:
                with io.StringIO() as buffer:
                    with contextlib.redirect_stdout(buffer):
                        result = get_currencies(self.valid_currency_codes)
            
            self.assertIsNone(result)
            self.assertTrue(any("отсутствуют курсы валют" in record.message 
                              for record in log_context.records))
    
    def test_api_connection_error(self):
        """Проверка обработки ошибки соединения с API"""
        with patch('requests.get') as mock_get:
            # Мокаем ошибку соединения
            mock_get.side_effect = requests.RequestException("Connection error")
            
            with self.assertLogs(level='ERROR') as log_context:
                with io.StringIO() as buffer:
                    with contextlib.redirect_stdout(buffer):
                        result = get_currencies(self.valid_currency_codes)
            
            self.assertIsNone(result)
            self.assertTrue(any("Ошибка запроса к API" in record.message 
                              for record in log_context.records))
    
    def test_http_error(self):
        """Проверка обработки HTTP ошибки"""
        with patch('requests.get') as mock_get:
            mock_response = MagicMock()
            mock_response.raise_for_status.side_effect = requests.HTTPError("404 Not Found")
            mock_get.return_value = mock_response
            
            with self.assertLogs(level='ERROR') as log_context:
                with io.StringIO() as buffer:
                    with contextlib.redirect_stdout(buffer):
                        result = get_currencies(self.valid_currency_codes)
            
            self.assertIsNone(result)
            self.assertTrue(any("Ошибка запроса к API" in record.message 
                              for record in log_context.records))
    
    def test_currency_missing_value_key(self):
        """Проверка обработки отсутствия ключа Value у валюты"""
        with patch('requests.get') as mock_get:
            # Мокаем ответ, где у одной валюты нет ключа Value
            invalid_response = {
                'Valute': {
                    'USD': {'Name': 'Доллар США'},  # Нет ключа Value!
                    'EUR': {'Value': 82.30, 'Name': 'Евро'}
                }
            }
            mock_response = MagicMock()
            mock_response.json.return_value = invalid_response
            mock_response.raise_for_status.return_value = None
            mock_get.return_value = mock_response
            
            with self.assertLogs(level='ERROR') as log_context:
                with io.StringIO() as buffer:
                    with contextlib.redirect_stdout(buffer):
                        result = get_currencies(['USD', 'EUR'])
            
            self.assertIsNone(result)
            self.assertTrue(any("отсутствует курс" in record.message 
                              for record in log_context.records))

    def test_log_output_to_stdout(self):
        """Проверка записи логов в поток вывода"""
        with patch('requests.get') as mock_get:
            mock_get.side_effect = requests.RequestException("Test error")
            
            # Захватываем stdout
            with io.StringIO() as buffer:
                with contextlib.redirect_stdout(buffer):
                    result = get_currencies(self.valid_currency_codes)
                
                stdout_output = buffer.getvalue()
            
            self.assertIsNone(result)
            # Проверяем, что сообщение об ошибке было выведено в stdout
            self.assertIn("Ошибка запроса к API", stdout_output)

# Демонстрация работы функции
def demonstrate_function():
    """Демонстрация работы функции с реальным API"""
    print("=== Демонстрация работы функции get_currencies ===")
    
    # Тест с реальными данными
    currencies = ['USD', 'EUR', 'GBP']
    
    print("1. Успешный запрос:")
    result = get_currencies(currencies)
    if result:
        print("   Курсы валют:")
        for currency, rate in result.items():
            print(f"   {currency}: {rate:.2f} руб.")
    else:
        print("   Не удалось получить курсы валют")
    
    print("\n2. Тест с несуществующей валютой:")
    result = get_currencies(['XYZ'])
    if result is None:
        print("   Обработка ошибки выполнена корректно")
    
    print("\n3. Тест с пустым списком:")
    result = get_currencies([])
    if result is None:
        print("   Обработка ошибки выполнена корректно")

if __name__ == "__main__":
    # Запуск демонстрации
    demonstrate_function()
    
    print("\n" + "="*50)
    print("Запуск unit-тестов...")
    
    # Запуск тестов
    unittest.main(argv=[''], verbosity=2, exit=False)

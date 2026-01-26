from typing import Optional
import requests

from models.currency import Currency

def dict_to_currency(v: dict) -> Currency:
    return Currency(v['ID'], v['NumCode'], v['CharCode'], v['Name'], v['Value'], v['Nominal'])

def get_currencies(currency_ids: Optional[list[str]] = None) -> list[Currency]:
    response = requests.get("https://www.cbr-xml-daily.ru/daily_json.js")
    
    if response.status_code != 200:
        raise Exception("Ошибка выполнения запроса к API")

    try:
        data = response.json()
    except ValueError:
        raise Exception("Ошибка выполнения запроса к API")

    if 'Valute' not in data:
        raise Exception("В ответе не содержатся курсы валют")
    
    valutes = data['Valute'].values()
    
    if currency_ids is None:
        return list(map(dict_to_currency, valutes))

    result: list[Currency] = []
    
    for valute in valutes:
        for id in currency_ids:
            if valute['ID'] != id:
                continue
            
            result.append(dict_to_currency(valute))
    return result

import json
import requests
from config import *


class APIException(Exception):
    pass


class Convertor:
    @staticmethod
    def get_price(base_key, sym_key, amount):
        try:
            base_key = exchanges[base_key.lower()]
        except KeyError:
            raise APIException(f"Валюта {base_key} не найдена!")

        try:
            sym_key = exchanges[sym_key.lower()]
        except KeyError:
            raise APIException(f"Валюта {sym_key} не найдена!")

        if base_key == sym_key:
            raise APIException(f'Невозможно перевести одинаковые валюты {base_key}!')

        try:
            amount = float(amount.replace(",", "."))
        except ValueError:
            raise APIException(f'Не удалось обработать количество {amount}!')

        url = f"https://api.apilayer.com/exchangerates_data/convert?to={sym_key}&from={base_key}&amount={int(amount)}"
        print(headers)
        querystring = {"format": "json", "from": "AUD", "to": "CAD", "amount": "1"}
        response = requests.get(url, headers=headers)
        print(url,response.text)
        resp = json.loads(response.text)
        new_price = resp['result']
        new_price = round(new_price, 3)
        message = f"Цена {amount} {base_key} в {sym_key} : {new_price}"
        return message
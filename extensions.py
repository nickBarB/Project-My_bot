import json
import requests
from config import exchanges
import time

class APIException(Exception):
    pass

class Currency_convertor:
    @staticmethod
    def get_price(base, sym, amount):
        try:
            base_key = exchanges[base.lower()]
        except KeyError:
            raise APIException(f'Currency {base} not found!'
                               f'\nВалюта {base} не найдена!')

        try:
            sym_key = exchanges[sym.lower()]
        except KeyError:
            raise APIException(f'Currency {sym} not found!'
                               f'\nВалюта {sym} не найдена!')

        if base_key == sym_key:
            raise APIException(f'Convertible currencies {base} are equal!'
                               f'\nКонвертируемые валюты {base} равны!')

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Failed to process value {amount}!'
                               f'\nНе удалось обработать значение {amount}!')

        r = requests.get(f'https://api.exchangeratesapi.io/latest?base={base_key}&symbols={sym_key}')
        resp = json.loads(r.content)
        new_price = resp['rates'][sym_key] * amount
        new_price = round(new_price, 3)
        message = f'Price {amount} {base} in {sym} : {new_price}.{time.ctime()}' \
                  f'\n' \
                  f'\nСтоимость {amount} {base} в {sym} : {new_price}.{time.ctime()}'
        return message

def quick_info():
    usd = (json.loads((requests.get(f'https://api.exchangeratesapi.io/latest?base=USD&symbols=RUB')).content))['rates'][
        'RUB']
    eur = (json.loads((requests.get(f'https://api.exchangeratesapi.io/latest?base=EUR&symbols=RUB')).content))['rates'][
        'RUB']
    return f'USD = {usd} RUB, EUR = {eur} RUB. {time.ctime()}'

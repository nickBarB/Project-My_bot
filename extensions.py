import json
import requests
from config import exchanges

class APIException(Exception):
    pass

class Currency_convertor:
    @staticmethod
    def get_price(base, sym, amount):
        try:
            base_key = exchanges[base.lower()]
        except KeyError:
            raise APIException(f'Currency {base} not found!')

        try:
            sym_key = exchanges[sym.lower()]
        except KeyError:
            raise APIException(f'Currency {sym} not found!')

        if base_key == sym_key:
            raise APIException(f'You are transferring one currency {base}!')

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Failed to process value {amount}!')

        r = requests.get(f'https://api.exchangeratesapi.io/latest?base={base_key}&symbols={sym_key}')
        resp = json.loads(r.content)
        new_price = resp['rates'][sym_key] * amount
        new_price = round(new_price, 3)
        message = f'Price {amount} {base} in {sym} : {new_price}'
        return message



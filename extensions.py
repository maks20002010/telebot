import json
import requests
from config import keys


class ConvExceptions(Exception):
    pass


class CurrencyConv:
    @staticmethod
    def convert(quote: str, base: str, amount: str):
        if quote == base:
            raise ConvExceptions(f'Невозможно конвертировать одинаковую валюту "{base}"')
        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise ConvExceptions(f'Не удалось обработать валюту "{quote}"')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise ConvExceptions(f'Не удалось обработать валюту "{base}"')

        try:
            amount = float(amount)
        except ValueError:
            raise ConvExceptions(f'Не удалось обработать количество "{amount}"')

        r = requests.get(
            f'https://v6.exchangerate-api.com/v6/ba9af052c560f9da06c7c27a/pair/{quote_ticker}/{base_ticker}/{amount}')
        total_base = json.loads(r.content)['conversion_result']

        return total_base
import json
import requests
from config import keys


class ConvertionException(Exception):
    pass

class EexchangeConverter:
    @staticmethod
    def convert(quote: str, base: str, amount: str):
               
        if quote == base:
            raise ConvertionException(f'Невозможно перевести одинаковые валлюты {base}')
        
        try:
            quote_ticher = keys[quote]
        except KeyError:
            raise ConvertionException(f'Не удалось обработать валюту {quote}')
        
        try:
            base_ticher = keys[base]
        except KeyError:
            raise ConvertionException(f'Не удалось обработать валюту {base}')
        
        try:
            amount = float(amount)
        except ValueError:
            raise ConvertionException(f'Не удалось обработать количество {amount}')
        
                
        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticher}&tsyms={base_ticher}')
        total_base = json.loads(r.content)[keys[base]]
        
        return total_base
        
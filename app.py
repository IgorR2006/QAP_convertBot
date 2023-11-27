import json
import requests
import telebot


TOKEN = '6421247490:AAGKMQNK7BzNDcBM0CFJNsAmDfDi3JzKaco'


bot = telebot.TeleBot(TOKEN)


keys = {
    'евро': 'EUR',
    'доллар': 'USD',
    'рубль': 'RUB'
}

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
        

@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = 'Чтобы начать работу введите команду боту в следующем формате: \n <имя валюты> <в какуювалюту перевести>\
    <количество переводимой валюты> \n Увидеть список всех доступных валют: /values'
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def help(message: telebot.types.Message):
    text = 'Доступные валюты: '
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
        
    low_text = message.text.lower()
    values = low_text.split(' ')
    
    if len(values) != 3:
        raise ConvertionException('Слишком много параметров')
            
    quote, base, amount = values
    total_base = EexchangeConverter.convert(quote, base, amount)
    
    convert_amout = float(total_base) * float(amount)
    text = f'Цена {amount} {quote} в {base} - {round(convert_amout, 2)}'
    bot.send_message(message.chat.id, text)


bot.polling()

import json
import requests
import telebot


TOKEN = ' '


bot = telebot.TeleBot(TOKEN)


keys = {
    'евро': 'EUR',
    'доллар': 'USD',
    'рубль': 'RUB'
}


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
    quote, base, amount = message.text.split(' ')
    r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={keys[quote]}&tsyms={keys[base]}')
    total_base = json.loads(r.content)[keys[base]]
    convert_amout = float(total_base) * float(amount)
    text = f'Цена {amount} {quote} в {base} - {round(convert_amout, 2)}'
    bot.send_message(message.chat.id, text)





# @bot.message_handler()
# def echo_test(message: telebot.types.Message):
#     bot.send_message(message.chat.id, 'HELLOOO')


bot.polling()

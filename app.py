import telebot
from config import keys, TOKEN
from extensions import ConvertionException, EexchangeConverter


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = 'Чтобы начать работу введите команду боту в следующем формате: \n <имя валюты> <в какую валюту перевести> \
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
    try:
        low_text = message.text.lower()
        values = low_text.split(' ')
        
        if len(values) != 3:
            raise ConvertionException('Слишком много параметров')
                
        quote, base, amount = values
        total_base = EexchangeConverter.convert(quote, base, amount)
        convert_amout = float(total_base) * float(amount)
        
    except ConvertionException as e:
        bot.reply_to(message, f'Ошибка пользователя. Смотри инструкцию /help \n{e}')
        
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
        
    else:
        text = f'Цена {amount} {quote} в {base} - {round(convert_amout, 2)}'
        bot.send_message(message.chat.id, text)


bot.polling()

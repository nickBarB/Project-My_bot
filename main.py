import telebot
from config import exchanges, TOKEN
from extensions import APIException, Currency_convertor
import traceback


bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message: telebot.types.Message):
    text = 'Hello! команда /help - вызов инструкции'
    bot.send_message(message.chat.id, text)

@bot.message_handler(commands=['help'])
def start(message: telebot.types.Message):
    text = '/currencies - список доступных валют' \
           ' что бы конвертировать валюты используйте следующую форму записи' \
           ' <имя валюты>  <в какую валюту перевести>  <количество>'
    bot.send_message(message.chat.id, text)

@bot.message_handler(commands=['currencies'])
def values(message: telebot.types.Message):
    text = 'Currencies available for conversion: '
    for i in exchanges.keys():
        text = '\n'.join((text, i))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text'])
def converter(message: telebot.types.Message):
    values = message.text.split(' ')
    try:
        if len(values) != 3:
            raise APIException('Error')

        answer = Currency_convertor.get_price(*values)
    except APIException as e:
        bot.reply_to(message, f'Error in comand:\n{e}')
    except Exception as e:
        traceback.print_tb(e.__traceback__)
        bot.reply_to(message, f'Unknown error:\n{e}')
    else:
        bot.reply_to(message, answer)

bot.polling(none_stop=True)
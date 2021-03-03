import telebot
from config import exchanges, TOKEN
from extensions import APIException, Currency_convertor, quick_info
import traceback

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def start(message: telebot.types.Message):
    text = 'Hello! command /help - call instruction' \
           '\ncommand /currencies - list of available currencies.' \
           '\nTo convert currencies, use the following entry form:' \
           '\n<currency name> <to which currency to convert> <amount>' \
           '\n' \
           '\nПриветствую! команда /help - вызов инструкции.' \
           '\nкоманда /currencies - список доступных валют.' \
           '\n Для конвертации валют используйте следующую форму записи:' \
           '\n <имя валюты>  <в какую валюту перевести>  <количество>.' \
           '\nкоманда /quick_info - быстрый вывод стоимости евро и доллара в рублях.'
    bot.send_message(message.chat.id, text)

@bot.message_handler(commands=['currencies'])
def values(message: telebot.types.Message):
    text = 'Currencies available for conversion: ' \
           '\nВалюты, доступные для конвертации:'
    for i in exchanges.keys():
        text = '\n'.join((text, i))
    bot.reply_to(message, text)

@bot.message_handler(commands=['quick_info'])
def quick_commands(message: telebot.types.Message):
    text = quick_info()
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
import telebot
from telebot import types
from config import keys, TOKEN
from extensions import CurrencyConv, ConvExceptions


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def start_command(message):
    text = 'Привет! Я бот, который поможет тебе узнать цену на определённое количество валюты. Чтобы узнать цену, напиши сообщение в следующем формате: \n' \
           '<имя валюты> <в какую валюту перевести> <количество>. \n' \
           '\n' \
           'Например: Доллар Рубль 10 \n' \
           '\n' \
           'Для просмотра списка доступных валют введите команду /values'
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')
        if len(values) != 3:
            raise ConvExceptions('Неверный формат. Слишком много параметров. Попробуйте ещё раз.')
        quote, base, amount = values
        total_base = CurrencyConv.convert(quote, base, amount)
    except ConvExceptions as e:
        bot.reply_to(message, f'Ошибка ввода: \n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду \n{e}.')
    else:
        text = f'Цена {amount} {quote} в {base} - {total_base} {base}'
        bot.send_message(message.chat.id, text)


if __name__ == '__main__':
    bot.polling(none_stop=True)

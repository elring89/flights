import os
from time import sleep
import telebot
from airports import get_city_info, get_cities


token = os.environ.get('TOKEN', '')
bot = telebot.TeleBot(token, threaded=False)
keyboard = None


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(
        message.chat.id,
        'Трям! Узнать что летает из Уфы...',
        reply_markup=keyboard
    )


@bot.message_handler(content_types=['text'])
def send_text(message):
    if message.text.lower() == 'Города':
        msgs = ', '.join(get_cities())
        bot.send_message(message.chat.id, msgs)
    elif message.text.lower() == 'Описание':
        msgs = ', '.join(get_city_info())
        bot.send_message(message.chat.id, msgs)
    print('Обработка сообщения')


def init_keyboard():
    telebot.types.ReplyKeyboardMarkup()
    keyboard.row('Города', 'Описание')


def main():
    init_keyboard()
    while True:
        try:
            bot.polling(none_stop=True)
        except Exception as e:
            print(e)
            sleep(15)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit()
    except Exception as exc:
        print(exc)

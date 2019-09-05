import os
import asyncio
from time import sleep
import telebot
from airports import get_city_info, get_cities


token = os.environ.get('TOKEN', '')
bot = telebot.TeleBot(token, threaded=False)
buttons = None


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(
        message.chat.id,
        'Трям! Узнать что летает из Уфы...',
        reply_markup=buttons
    )


@bot.message_handler(content_types=['text'])
async def send_text(message):
    print('Обработка сообщения..')
    if message.text.lower() == 'Города':
        cities = await get_cities()
        msgs = ', '.join(cities)
        bot.send_message(message.chat.id, msgs)
    elif message.text.lower() == 'Описание':
        info = await get_city_info()
        msgs = ', '.join(info)
        bot.send_message(message.chat.id, msgs)
    print('Обработка сообщения закончена')


def init_buttons():
    buttons = telebot.types.ReplyKeyboardMarkup()
    buttons.row('Города', 'Описание')


def main():
    init_buttons()
    print('Запуск..')
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

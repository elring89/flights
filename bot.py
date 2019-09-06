import os
from time import sleep
import telebot
from airports import get_tomorrow_schedule


token = os.environ.get('TOKEN', '')
bot = telebot.TeleBot(token, threaded=False)


@bot.message_handler(commands=['start'])
def start_message(message):
    buttons = telebot.types.ReplyKeyboardMarkup()
    buttons.row('Аэропорт Уфы на завтра')
    bot.send_message(
        message.chat.id,
        'Трям! Узнать что летает из Уфы...',
        reply_markup=buttons
    )


@bot.message_handler(content_types=['text'])
def send_text(message):
    print('Обработка сообщения..')
    if message.text.lower() == 'аэропорт уфы на завтра':
        schedule = get_tomorrow_schedule()
        bot.send_message(message.chat.id, schedule)
    print('Обработка сообщения закончена')


def main():
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

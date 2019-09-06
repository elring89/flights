import os
from time import sleep
import telebot
import airports
from flask import Flask, request

TOKEN = os.environ.get('TOKEN', '')
bot = telebot.TeleBot(TOKEN, threaded=False)
airport = airports.UfaAirport()
server = Flask(__name__)

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
        schedule = airport.get_schedule_msg()
        msg = schedule or 'Не удалось получить информацию.'
        bot.send_message(message.chat.id, msg)
    print('Обработка сообщения закончена')


@server.route('/' + TOKEN, methods=['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200


@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url='https://ufaflightbot.herokuapp.com/' + TOKEN)
    return "!", 200


def main():
    print('Запуск..')
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit()
    except Exception as exc:
        print(exc)

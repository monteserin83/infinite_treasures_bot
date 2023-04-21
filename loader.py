'''Module that load the Telegram bot'''


import telebot
from telebot import apihelper
from flask import Flask, request  # para crear el servidor web local

from constants import API_TOKEN


apihelper.SESSION_TIME_TO_LIVE = 5 * 60

# instanciar la API de telegram
bot = telebot.TeleBot(API_TOKEN, parse_mode="html")

# instanciar el servidor web
web_server = Flask(__name__)

# gestionar las peticiones POST enviadas al servidor web


@web_server.route('/', methods=['POST'])
def webhook():
    if request.headers.get("content-type") == "application/json":
        update = telebot.types.Update.de_json(
            request.stream.read().decode('utf-8'))
        bot.process_new_updates([update])
        return "OK", 200

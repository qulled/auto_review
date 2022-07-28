import telebot
import datetime as dt
from telebot import types
import os
from dotenv import load_dotenv
import time
import requests
import json

chat_id = []

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)
load_dotenv('.env ')
token = os.getenv('TOKEN_BOT')
url = os.getenv('URL')

bot = telebot.TeleBot(token)

@bot.message_handler(commands=['start'])
def start(message):
    markup_start = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_start = types.KeyboardButton('/start')
    markup_start.add(button_start)
    user_id = message.from_user.id

    if user_id not in chat_id:
        chat_id.append(user_id)
    bot.send_message(message.chat.id,
                    'Бот активирован', reply_markup=markup_start)
    bot.send_message(message.chat.id,
                    f'{chat_id}', reply_markup=markup_start)
    with open('chat_id.json', 'w') as outfile:
        json.dump(chat_id, outfile)



# launch bot
bot.polling(none_stop=True, interval=0)

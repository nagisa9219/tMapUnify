import telebot
import api.bus_api as d
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, InlineQueryResultPhoto
import api.weather_api  #use weather.weather(address) to get the weather

API_KEY = '6057511045:AAGut6QZzRU64WDYZmT4bvBk47Mb9srVJD8'
bot = telebot.TeleBot(API_KEY)

start_coord = []
dest_coord = []

API_KEY = '6057511045:AAGut6QZzRU64WDYZmT4bvBk47Mb9srVJD8'
bot = telebot.TeleBot(API_KEY)


@bot.message_handler(commands=['start'])
def start(message):
  start_coord = d.address_to_coord(message.text[7:],
                                         "f0305e991db040688c28b59ac6d9fbd5")
  if start_coord[0] == 400:
    bot.reply_to(message, "Invalied request: Address not found.")
  else:
    bot.reply_to(message, "OK")
    bot.reply_to(message, start_coord)

@bot.message_handler(commands=['dest'])
def dest(message):
  dest_coord = d.address_to_coord(message.text[6:],"f0305e991db040688c28b59ac6d9fbd5")
  if dest_coord[0] == 400:
    bot.reply_to(message, "Invalied request: Address nxqot found.")
  else:
    bot.reply_to(message, "OK")
    bot.reply_to(message, dest_coord)

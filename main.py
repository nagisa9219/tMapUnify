import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, InlineQueryResultPhoto

API_KEY = '6057511045:AAGut6QZzRU64WDYZmT4bvBk47Mb9srVJD8'
bot = telebot.TeleBot(API_KEY)


@bot.message_handler(commands=['start', 'back'])
def start(message):

  reply_markup = InlineKeyboardMarkup([[
    InlineKeyboardButton("walk", callback_data="walking"),
    InlineKeyboardButton("bike", callback_data="biking"),
    InlineKeyboardButton("drive", callback_data="driving"),
    InlineKeyboardButton("scooter", callback_data="scooter"),
    InlineKeyboardButton("mass", callback_data="mass"),
    InlineKeyboardButton("taxi", callback_data="taxi"),
  ]])
  bot.reply_to(message, 'Enter an option.', reply_markup=reply_markup)


@bot.callback_query_handler(func=lambda cb: cb.data == "walking")
def walking(call):
  bot.answer_callback_query(call.id, "Okay")


@bot.callback_query_handler(func=lambda cb: cb.data == 'biking')
def biking(call):
  
  reply_markup = InlineKeyboardMarkup([[
    InlineKeyboardButton("walk", callback_data="walking"),
    InlineKeyboardButton("bike", callback_data="biking"),
    InlineKeyboardButton("drive", callback_data="driving"),
    InlineKeyboardButton("scooter", callback_data="scooter"),
    InlineKeyboardButton("mass", callback_data="mass"),
    InlineKeyboardButton("taxi", callback_data="taxi"),
  ]])
  
  bot.answer_callback_query(call.id, "Okay")

  @bot.callback_query_handler(func=lambda cb: cb.data == 'North')
  def North(call):
    bot.answer_callback_query(call.id, "Okay")

  @bot.callback_query_handler(func=lambda cb: cb.data == 'South')
  def South(call):
   bot.answer_callback_query(call.id, "Okay")

  @bot.callback_query_handler(func=lambda cb: cb.data == 'East')
  def East(call):
   bot.answer_callback_query(call.id, "Okay")

  @bot.callback_query_handler(func=lambda cb: cb.data == 'West')
  def West(call):
   bot.answer_callback_query(call.id, "Okay")


@bot.callback_query_handler(func=lambda cb: cb.data == 'driving')
def driving(call):
  bot.answer_callback_query(call.id, "Okay")


@bot.message_handler(func=lambda cb: cb.data == 'scooter')
def scooter(call):
  bot.answer_callback_query(call.id, "Okay")


@bot.message_handler(func=lambda cb: cb.data == 'mass')
def mass(call):
  bot.answer_callback_query(call.id, "Okay")


@bot.message_handler(func=lambda cb: cb.data == 'taxi')
def taxi(call):
  bot.answer_callback_query(call.id, "Okay")


bot.polling()

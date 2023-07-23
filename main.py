import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, InlineQueryResultPhoto
import api.weather_api #use weather.weather(address) to get the weather
from telegram import Update
from telegram.ext import CallbackContext, MessageHandler, Filters 

API_KEY = '6057511045:AAGut6QZzRU64WDYZmT4bvBk47Mb9srVJD8'
bot = telebot.TeleBot(API_KEY)

#retart
backQuery = InlineKeyboardButton("New Option", callback_data="New Option")
deleteQuery = InlineKeyboardButton("Delete Message", callback_data="Delete")
renderingMenu = InlineKeyboardMarkup([[
  InlineKeyboardButton("walk", callback_data="walking"),
  InlineKeyboardButton("UBike", callback_data="biking"),
  InlineKeyboardButton("drive", callback_data="driving"),
  InlineKeyboardButton("scooter", callback_data="scooter"),
  InlineKeyboardButton("mass", callback_data="mass"),
  InlineKeyboardButton("taxi", callback_data="taxi"),
], [backQuery, deleteQuery]])

def location(update: Update, context: CallbackContext): 
    current_pos = (update.message.location.latitude, update.message.location.longitude) 
    print(current_pos) 
@bot.add_handler(MessageHandler(Filters.location, location))

@bot.message_handler(commands=['start'])
def start(message):

  reply_markup = renderingMenu
  bot.reply_to(message, 'Enter an option.', reply_markup=reply_markup)


@bot.callback_query_handler(func=lambda cb: cb.data == "New Option")
def Back(call):

  reply_markup = renderingMenu
  bot.reply_to(call.message, 'Enter an option.', reply_markup=reply_markup)


@bot.callback_query_handler(func=lambda cb: cb.data == "Delete")
def Delete(call):
  bot.delete_message(call.message.chat.id, call.message.message_id)


@bot.callback_query_handler(func=lambda cb: cb.data == "walking")
def walking(call):
  reply_markup = InlineKeyboardMarkup([[backQuery,deleteQuery,]])
  bot.reply_to(call.message, 'ok', reply_markup=reply_markup)
  bot.answer_callback_query(call.id, " ")


@bot.callback_query_handler(func=lambda cb: cb.data == 'biking')
def biking(call):

  reply_markup = InlineKeyboardMarkup([[backQuery,deleteQuery,]])
  bot.reply_to(call.message, 'Enter an option.', reply_markup=reply_markup)
  bot.answer_callback_query(call.id, " ")

@bot.callback_query_handler(func=lambda cb: cb.data == "driving")
def driving(call):
  reply_markup = InlineKeyboardMarkup([[backQuery,deleteQuery,]])
  bot.reply_to(call.message, 'ok', reply_markup=reply_markup)
  bot.answer_callback_query(call.id, " ")


@bot.callback_query_handler(func=lambda cb: cb.data == "scooter")
def scooter(call):
  reply_markup = InlineKeyboardMarkup([[backQuery,deleteQuery,]])
  bot.reply_to(call.message, 'ok', reply_markup=reply_markup)
  bot.answer_callback_query(call.id, "")


@bot.callback_query_handler(func=lambda cb: cb.data == "mass")
def mass(call):
  reply_markup = InlineKeyboardMarkup([[backQuery,deleteQuery,]])
  bot.reply_to(call.message, 'ok', reply_markup=reply_markup)
  bot.answer_callback_query(call.id, " ")


@bot.callback_query_handler(func=lambda cb: cb.data == "taxi")
def taxi(call):
  reply_markup = InlineKeyboardMarkup([[backQuery,deleteQuery,]])
  bot.reply_to(call.message, 'ok', reply_markup=reply_markup)
  bot.answer_callback_query(call.id, " ")

bot.polling()
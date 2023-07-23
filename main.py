import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, InlineQueryResultPhoto
import weather #


API_KEY = '6057511045:AAGut6QZzRU64WDYZmT4bvBk47Mb9srVJD8'
bot = telebot.TeleBot(API_KEY)

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
  reply_markup = InlineKeyboardMarkup([[
    backQuery,
    deleteQuery,
  ]])
  bot.reply_to(call.message, 'ok', reply_markup=reply_markup)
  bot.answer_callback_query(call.id, " ")


@bot.callback_query_handler(func=lambda cb: cb.data == 'biking')
def biking(call):

  reply_markup = InlineKeyboardMarkup([[
    InlineKeyboardButton("North", callback_data="North"),
    InlineKeyboardButton("South", callback_data="South"),
    InlineKeyboardButton("East", callback_data="East"),
    InlineKeyboardButton("Mid", callback_data="Mid"),
    ],[backQuery,deleteQuery]])
  bot.reply_to(call.message, 'Enter an option.', reply_markup=reply_markup)
  bot.answer_callback_query(call.id, " ")

  @bot.callback_query_handler(func=lambda cb: cb.data == "North")
  def North(call):
    reply_markup = InlineKeyboardMarkup([[
      InlineKeyboardButton("台北", callback_data="1"),
      InlineKeyboardButton("基隆", callback_data="2"),
      InlineKeyboardButton("新北", callback_data="3"),
      InlineKeyboardButton("桃園", callback_data="4"),
      InlineKeyboardButton("新竹", callback_data="5"),
      InlineKeyboardButton("宜蘭", callback_data="6"),
      ],[backQuery,deleteQuery]])
    bot.reply_to(call.message, 'ok', reply_markup=reply_markup)
    bot.answer_callback_query(call.id, " ")

  @bot.callback_query_handler(func=lambda cb: cb.data == "South")
  def South(call):
    reply_markup = InlineKeyboardMarkup([[
      InlineKeyboardButton("嘉義", callback_data="7"),
      InlineKeyboardButton("台南", callback_data="8"),
      InlineKeyboardButton("高雄", callback_data="9"),
      InlineKeyboardButton("屏東", callback_data="10"),
      ],[backQuery,deleteQuery]])
    bot.reply_to(call.message, 'ok', reply_markup=reply_markup)
    bot.answer_callback_query(call.id, " ")

  @bot.callback_query_handler(func=lambda cb: cb.data == "East")
  def East(call):
    reply_markup = InlineKeyboardMarkup([[
      InlineKeyboardButton("花蓮", callback_data="11"),
      InlineKeyboardButton("台東", callback_data='12'),
      ],[backQuery,deleteQuery]])
    bot.reply_to(call.message, 'ok', reply_markup=reply_markup)
    bot.answer_callback_query(call.id, " ")

  @bot.callback_query_handler(func=lambda cb: cb.data == "Mid")
  def Mid(call):
    reply_markup = InlineKeyboardMarkup([[
      InlineKeyboardButton("苗栗", callback_data="13"),
      InlineKeyboardButton("台中", callback_data="14"),
      InlineKeyboardButton("彰化", callback_data="15"),
      InlineKeyboardButton("雲林", callback_data="16"),
      InlineKeyboardButton("南投", callback_data="17"),],[backQuery,deleteQuery]])
    bot.reply_to(call.message, 'ok', reply_markup=reply_markup)
    bot.answer_callback_query(call.id, " ")


@bot.callback_query_handler(func=lambda cb: cb.data == "driving")
def driving(call):
  reply_markup = InlineKeyboardMarkup([[
    backQuery,
    deleteQuery,
  ]])
  bot.reply_to(call.message, 'ok', reply_markup=reply_markup)
  bot.answer_callback_query(call.id, " ")


@bot.callback_query_handler(func=lambda cb: cb.data == "scooter")
def scooter(call):
  reply_markup = InlineKeyboardMarkup([[
    backQuery,
    deleteQuery,
  ]])
  bot.reply_to(call.message, 'ok', reply_markup=reply_markup)
  bot.answer_callback_query(call.id, " ")


@bot.callback_query_handler(func=lambda cb: cb.data == "mass")
def mass(call):
  reply_markup = InlineKeyboardMarkup([[
    backQuery,
    deleteQuery,
  ]])
  bot.reply_to(call.message, 'ok', reply_markup=reply_markup)
  bot.answer_callback_query(call.id, " ")

 
@bot.callback_query_handler(func=lambda cb: cb.data == "taxi")
def taxi(call):
  reply_markup = InlineKeyboardMarkup([[
    backQuery,
    deleteQuery,
  ]])
  bot.reply_to(call.message, 'ok', reply_markup=reply_markup)
  bot.answer_callback_query(call.id, " ")


bot.polling()

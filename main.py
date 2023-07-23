import telebot
from datetime import datetime
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, InlineQueryResultPhoto


import api.maps_api 
import api.Ubike_api
import api.weather_api


API_TOKEN = '6352815505:AAE2C8RWX12R1io18BBcJYFqJlP817Ub3kg'

bot = telebot.TeleBot(API_TOKEN)
start = []
dest = []

# Handle '/start' and '/help'
@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    bot.reply_to(message, """\
哈囉，你也在煩惱晚餐吃什麼嗎

用 /add 告訴我你喜歡哪些美食
輸入 /list 查看完整美食列表
晚餐時間只要用 /eat 就能幫你決定囉 (⁎⁍̴̛ᴗ⁍̴̛⁎)
""")


@bot.message_handler(commands=['setstart'])
def set_start(message):
    start = api.maps_api.address_to_coord(message.text[10:],"f0305e991db040688c28b59ac6d9fbd5",False)
    if start[0]==400:
        bot.reply_to(message, 'Wrong. Please try again.')
    else:
        bor.reply_to
        


@bot.message_handler(commands=['setdest'])
def set_start(message):
    dest = api.maps_api.address_to_coord(message.text[9:],"f0305e991db040688c28b59ac6d9fbd5")
    bot.reply_to(message, 'OK')

@bot.callback_quary_handler(func=lambda cb: cb.data == "press_the button")
def press_the_buttom(call):
    InlineKeyboardMarkup([[InlineKeyboardButton("a", callback_data="b"), InlineKeyboardButton("a", callback_data="b"),]])
    InlineKeyboardMarkup([[InlineKeyboardButton("a", callback_data="b"), InlineKeyboardButton("a", callback_data="b"),]])
    InlineKeyboardMarkup([[InlineKeyboardButton("a", callback_data="b"), InlineKeyboardButton("a", callback_data="b"),]])





@bot.message_handler(commands=[""])
def eat_food(message):
    bot.reply_to(message, 'TODO')


@bot.message_handler(commands=['time'])
def time_cmd(message):
    t = datetime.now().strftime('%m 月 %d 日 %H:%M:%S')

    reply_markup = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("更新時間", callback_data="time_update"),
        ]
    ])
    bot.reply_to(message, f'現在時間：{t}', reply_markup=reply_markup)


@bot.callback_query_handler(func=lambda cb: cb.data.startswith('time_'))
def time_cb(call):
    if call.data == "time_update":
        reply_markup = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("更新時間", callback_data="time_update"),
            ]
        ])

        t = datetime.now().strftime('%m 月 %d 日 %H:%M:%S')
        bot.edit_message_text(text=f'現在時間：{t}',
                              chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              reply_markup=reply_markup)

        bot.answer_callback_query(call.id, "時間已更新")


print('Bot is online!')
bot.infinity_polling()
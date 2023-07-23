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
is_valid=False

# Handle '/start' and '/help'
@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    bot.reply_to(message, """\
/setstart <地址> --> 輸入起始點
/setdest <地址> --> 輸入終點
""")


@bot.message_handler(commands=['setstart'])
def set_start(message):
    start.append(api.maps_api.address_to_coord(message.text[10:],False))

    if start[0] == "F":
        bot.reply_to(message, 'Wrong. Please try again.')
        print(start)
        start.clear()
    else:
        bot.reply_to(message, 'OK')
        print(start)

@bot.message_handler(commands=['setdest'])
def set_dest(message):
    dest.append(api.maps_api.address_to_coord(message.text[9:]))
    if start[0] == "F":
        bot.reply_to(message, 'Wrong. Please try again.')
        print(start)
        start.clear()
        
    else:
        bot.reply_to(message, 'OK')
        #bot.callback_query_handler("press_the button")
        is_valid=True
        print(start)

@bot.callback_query_handler(is_valid)#)(func=lambda cb: cb.data == "press_the button")
def press_the_buttom(call):
    reply_markup = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("trans1",callback_data="use1")
        ]
    ])

@bot.callback_query_handler(func=lambda cb: cb.data == "use1")
def transport1(call):
    bot.reply_to(call.message,"the weather is"+str(api.weather_api.weather(dest[0],dest[1])))

@bot.message_handler(commands=["eat_food"])
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
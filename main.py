import telebot #telebot imported
#import api.Ubike_api
from datetime import datetime
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, InlineQueryResultPhoto
import api.maps_api 
import api.weather_api


API_TOKEN = '6352815505:AAE2C8RWX12R1io18BBcJYFqJlP817Ub3kg'

bot = telebot.TeleBot(API_TOKEN)
start = []
dest = []
is_valid=False
stations=""

#delete&new
backQuery = InlineKeyboardButton("New Option", callback_data="New Option")
deleteQuery = InlineKeyboardButton("Delete Message", callback_data="Delete")
# Handle '/start' and '/help'
@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    bot.reply_to(message, """\
Hi! 請輸入下列的指令來開始規劃出門方式
                 
/setstart <地址> -> 輸入起始點
/setdest <地址> -> 輸入終點
""")

@bot.callback_query_handler(func=lambda cb: cb.data == "New Option")
def Back(call):
  bot.reply_to(call.message, """\
Hi! 請輸入下列的指令來開始規劃出門方式

/setstart <地址> -> 輸入起始點
/setdest <地址> -> 輸入終點
""")
               
@bot.callback_query_handler(func=lambda cb: cb.data == "Delete")
def Delete(call):
  bot.delete_message(call.message.chat.id, call.message.message_id)





@bot.message_handler(commands=['setstart'])
def set_start(message):
    start.append(api.maps_api.address_to_coord(message.text[10:],False))

    if start[0] == "F":
        bot.reply_to(message, 'Wrong. Please try again.')
        #print(start)
        start.clear()
    else:
        bot.reply_to(message, 'OK')
        print(start)

@bot.message_handler(commands=['setdest'])
def set_dest(message):
    dest.append(api.maps_api.address_to_coord(message.text[9:]))
    if start[0] == "F":
        bot.reply_to(message, 'Wrong. Please try again.')
        #print(start)
        start.clear()
        
    else:
        reply_markup=InlineKeyboardMarkup([[
        InlineKeyboardButton('Walk',callback_data='walking'),
        InlineKeyboardButton('Drive',callback_data='driving'),
        InlineKeyboardButton('UBike',callback_data='biking')],
        [InlineKeyboardButton('Mass',callback_data='masstrans'),
        InlineKeyboardButton('Taxi',callback_data='taxi'),
        ],[backQuery, deleteQuery]])
        bot.reply_to(message = message, text = 'OK',reply_markup = reply_markup)
        #bot.callback_query_handler("press_the button")
        is_valid=True
        print(dest)

# @bot.callback_query_handler(is_valid)#)(func=lambda cb: cb.data == "press_the button")
# def press_the_buttom(call):
#     reply_markup = InlineKeyboardMarkup([
#         [
#             InlineKeyboardButton("trans1",callback_data="use1")
#         ]
#r    ])

@bot.callback_query_handler(func=lambda cb: cb.data =="walking")
def walking(call):
    print("walking")
    #bot.reply_to(call.message,f")\
    con=api.weather_api.weather(str(dest[0][1][0]),str(dest[0][1][1]))
    cost=api.maps_api.distance_calc(start,dest,"walking")
    bot.reply_to(call.message,f"the weather there is {con}")
    bot.reply_to(call.message,f"The estimated distance is {cost[1]:.2f}km,\nand it will take about {int(cost[2]/60)}mins to get there.")
    #print(con,cost)
    print(con)

@bot.callback_query_handler(func=lambda cb: cb.data =="biking")
def biking(call):
    print("walking")
    #bot.reply_to(call.message,f")\
    con=api.weather_api.weather(str(dest[0][1][0]),str(dest[0][1][1]))
    cost=api.maps_api.distance_calc(start,dest,"bicycling")
    bot.reply_to(call.message,f"the weather is {con}")
    bot.reply_to(call.message,f"The estimated distance is {cost[1]:.2f}km,\nand it will take about {int(cost[2]/60)}mins to get there.")






    #reply_markup=InlineKeyboardMarkup([[backQuery,deleteQuery]])
    
@bot.callback_query_handler(func=lambda cb: cb.data =="driving")
def driving(call):
    print("driving")
    #bot.reply_to(call.message,f")\
    con=api.weather_api.weather(str(dest[0][1][0]),str(dest[0][1][1]))
    cost=api.maps_api.distance_calc(start,dest,"driving")
    bot.reply_to(call.message,f"The weather there is {con}")
    bot.reply_to(call.message,f"The estimated distance is {cost[1]:.2f}km,\nand it will take about {int(cost[2]/60)}mins to get there.")
    #print(con,cost)
    print(con)
@bot.callback_query_handler(func=lambda cb: cb.data =="masstrans")
def mass(call):
    #bot.reply_to(call.message,f")\
    con=api.weather_api.weather(str(dest[0][1][0]),str(dest[0][1][1]))
    cost=api.maps_api.distance_calc(start,dest,"transit")
    bot.reply_to(call.message,f"The weather there is {con}")
    bot.reply_to(call.message,f"The estimated distance is {cost[1]:.2f}km,\nand it will take about {int(cost[2]/60)}mins to get there.")
    #print(con,cost)
    print(con)

@bot.callback_query_handler(func=lambda cb: cb.data =="taxi")
def taxi(call):
    #bot.reply_to(call.message,f")\
    con=api.weather_api.weather(str(dest[0][1][0]),str(dest[0][1][1]))
    cost=api.maps_api.distance_calc(start,dest,"driving")
    bot.reply_to(call.message,f"The weather there is {con}")
    bot.reply_to(call.message,f"The estimated distance is {cost[1]:.2f}km,\nand it will take about {int(cost[2]/60)}mins to get there.")
    #print(con,cost)
    print(con)


# @bot.callback_query_handler(func=lambda cb: cb=="ubike")
# def time_cb(call):
#     if call.data == "time_update":
#         reply_markup = InlineKeyboardMarkup([
#             [
#                 InlineKeyboardButton("更新時間", callback_data="time_update"),
#             ]
#         ])

#         t = datetime.now().strftime('%m 月 %d 日 %H:%M:%S')
#         bot.edit_message_text(text=f'現在時間：{t}',
#                               chat_id=call.message.chat.id,
#                               message_id=call.message.message_id,
#                               reply_markup=reply_markup)

#         bot.answer_callback_query(call.id, "時間已更新")

# @bot.callback_query_handler(func=lambda cb: cb == "taxi")
# def transit(call):
#      bot.reply_to(call.message,"the weather is"+str(api.weather_api.weather(dest[0],dest[1])))
#      #bot.reply_to(call.message,api.maps_api.taxi_calc())


print('Bot is online!')
bot.infinity_polling()
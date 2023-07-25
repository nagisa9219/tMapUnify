import telebot #telebot imported
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, InlineQueryResultPhoto
import api.maps_api 
import api.weather_api
from api.api_token import apitoken
# import api.Ubike_api

apitokens = apitoken()
bot = telebot.TeleBot(apitokens.telebot)
start = []
dest = []
is_valid = False
stations = ""
place_list = []

#delete&new
backQuery = InlineKeyboardButton("New Option", callback_data="New Option")
deleteQuery = InlineKeyboardButton("Delete Message", callback_data="Delete")

# Handle '/start' and '/help'
@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    bot.reply_to(message, "Hi！tMap Unify機器人可以幫你規劃出門方式\n\n請輸入下列的指令來開始:\n/setstart <地址> -> 輸入起始點\n/setdest <地址> -> 輸入終點\n\nP.S. <地址>支援模糊地點搜尋，你也可以輸入「台灣大學」等地點名稱喔!")

@bot.callback_query_handler(func=lambda cb: cb.data == "New Option")
def Back(call):
    bot.reply_to(call.message, "Hi！tMap Unify機器人可以幫你規劃出門方式\n\n請輸入下列的指令來開始:\n/setstart <地址> -> 輸入起始點\n/setdest <地址> -> 輸入終點\n\nP.S. <地址>支援模糊地點搜尋，你也可以輸入「台灣大學」等地點名稱喔!")
               
@bot.callback_query_handler(func=lambda cb: cb.data == "Delete")
def Delete(call):
    bot.delete_message(call.message.chat.id, call.message.message_id)

@bot.message_handler(commands=['setstart'])
def set_start(message):
    if len(message.text) <= 9:
        bot.reply_to(message, "輸入的資訊有誤，請再試一遍!\n\n指令用法:\n/setstart <地址>")
    else:
        place_list.append(message.text[10:])
        start.append(api.maps_api.address_to_coord(message.text[10:],False))
        if start[0] == "F":
            bot.reply_to(message, '輸入的資訊有誤，請再試一遍!')
            #print(start)
            start.clear()
        else:
            bot.reply_to(message, 'OK')
            # print(start)

@bot.message_handler(commands=['setdest'])
def set_dest(message):
    dest.append(api.maps_api.address_to_coord(message.text[9:]))
    # print(start,dest)
    if message.text[9:] in place_list:
        bot.reply_to(message, "目的地不可以和起始點相同，請再試一遍!")
        dest.clear()
    elif dest[0] == "F":
        bot.reply_to(message, '輸入的資訊有誤，請再試一遍!')
        #print(dest)
        dest.clear()  
    else:
        reply_markup=InlineKeyboardMarkup([[
        InlineKeyboardButton('Walk',callback_data='walking'),
        InlineKeyboardButton('Drive',callback_data='driving'),
        InlineKeyboardButton('UBike',callback_data='biking')],
        [InlineKeyboardButton('Mass',callback_data='masstrans'),
        InlineKeyboardButton('Taxi',callback_data='taxi')],
        [backQuery, deleteQuery]])
        bot.reply_to(message = message, text = 'OK',reply_markup = reply_markup)
        #bot.callback_query_handler("press_the button")
        is_valid=True
        # print(dest)

@bot.callback_query_handler(func=lambda cb: cb.data =="walking")
def walking(call):
    # print("walking")
    #bot.reply_to(call.message,f")\
    con=api.weather_api.weather(str(dest[0][1][0]),str(dest[0][1][1]))
    cost=api.maps_api.distance_calc(start,dest,"walking")
    bot.reply_to(call.message,f"the weather there is {con}")
    bot.reply_to(call.message,f"The estimated distance is {cost[1]:.2f}km,\nand it will take about {int(cost[2]/60)}mins to get there.")
    # print(con,cost)
    # print(con)

@bot.callback_query_handler(func=lambda cb: cb.data =="biking")
def biking(call):
    # print("walking")
    #bot.reply_to(call.message,f")\
    weather_result=api.weather_api.weather(str(dest[0][1][0]),str(dest[0][1][1]))
    distance_result=api.maps_api.distance_calc(start,dest,"bicycling")
    bot.reply_to(call.message,f"the weather is {weather_result}")
    bot.reply_to(call.message,f"The estimated distance is {distance_result[1]:.2f}km,\nand it will take about {int(distance_result[2]/60)}mins to get there.")
    
@bot.callback_query_handler(func=lambda cb: cb.data =="driving")
def driving(call):
    # print("driving")
    #bot.reply_to(call.message,f")\
    con=api.weather_api.weather(str(dest[0][1][0]),str(dest[0][1][1]))
    cost=api.maps_api.distance_calc(start,dest,"driving")
    bot.reply_to(call.message,f"The weather there is {con}")
    bot.reply_to(call.message,f"The estimated distance is {cost[1]:.2f}km,\nand it will take about {int(cost[2]/60)}mins to get there.")
    #print(con,cost)
    # print(con)

@bot.callback_query_handler(func=lambda cb: cb.data =="masstrans")
def mass(call):
    #bot.reply_to(call.message,f")\
    con=api.weather_api.weather(str(dest[0][1][0]),str(dest[0][1][1]))
    cost=api.maps_api.distance_calc(start,dest,"transit")
    bot.reply_to(call.message,f"The weather there is {con}")
    bot.reply_to(call.message,f"The estimated distance is {cost[1]:.2f}km,\nand it will take about {int(cost[2]/60)}mins to get there.")
    #print(con,cost)
    # print(con)

@bot.callback_query_handler(func=lambda cb: cb.data =="taxi")
def taxi(call):
    #bot.reply_to(call.message,f")\
    con=api.weather_api.weather(str(dest[0][1][0]),str(dest[0][1][1]))
    cost=api.maps_api.distance_calc(start,dest,"driving")
    bot.reply_to(call.message,f"The weather there is {con}")
    bot.reply_to(call.message,f"The estimated distance is {cost[1]:.2f}km,\nand it will take about {int(cost[2]/60)}mins to get there.")
    #print(con,cost)
    # print(con)

print('Bot is online!')
bot.infinity_polling()
import requests
import json
from requests.structures import CaseInsensitiveDict
enter_user='user-agent'
enter_web='Mozilla/5.0'
ID_Data_clean=[]
#Location_Data_clean=[]
city=input()
geo_api_key='f0305e991db040688c28b59ac6d9fbd5'
google_api_key='AIzaSyB8jGb3zHAnT_47p-c-5avxJ4KieHEs7-c'

"""
    此function透過Geogapify Geocode API將地址轉換為經緯度座標
    
    Args:
        address (str): 欲轉換的地址
        api_key (str): API的key
        cityinfo (bool): 顯示該地址位於的縣市英文名稱(概略)，可略

    Returns:
        lat, lot (float, float): 地址轉換過後的經緯度座標(cityinfo == False時)
        [cityname (str)]"
        [status_code (str): 若查無地址或其他錯誤，則僅回傳此項]
"""
def address_to_coord(address,api_key,cityinfo):
  url = "https://api.geoapify.com/v1/geocode/search?text=" + address + "&apiKey=" + api_key
  headers = CaseInsensitiveDict()
  headers["Accept"] = "application/json"
  resp = requests.get(url, headers=headers).json()
  if resp["features"] == []:
      return "400"
  elif cityinfo == False:
      coord = resp["features"][0]["geometry"]["coordinates"]
      return coord
  elif cityinfo == True:
      city = resp["features"][0]["properties"]["city"]
      return city

"""
    計算起始點與目的地的路線距離並依交通方式計算通行時間

    Args:
        coord1, coord2 (list[float]): 起始,目的地的經緯度座標
        mode (str) ={driving|bicycling|walking|transit}: 交通方式
        api_key (str): API的key
    
    Returns:
        distance, duration (int, float): 計算過後的交通距離及花費時間(單位：公里,秒)
"""
def distance_calc(coord1, coord2, mode, api_key) :
    url = "https://maps.googleapis.com/maps/api/distancematrix/json?origins=" + str(coord1[1]) + "%2C" + str(coord1[0]) + "&destinations=" + str(coord2[1]) + "%2C" + str(coord2[0]) + "&mode=" + mode +"&key=" + api_key
    payload = {}
    headers = {}
    resp = requests.get(url, headers=headers, data=payload).json()
    distance = float(resp["rows"][0]["elements"][0]["distance"]["value"])*0.001 #m->km
    duration = float(resp["rows"][0]["elements"][0]["duration"]["value"])
    return distance, duration

'''
Ubike 即時性站點更新
資料來源:PTX
API使用:注意沒有會員用官方文件方法可能會被擋下來
資料內容:
[{"StationUID"  str:站點ID(格式:縣市代碼+流水號),
  "AvailableRentBikes"  str: 目前閒置腳踏車數量,  
  "UpdateTime"  str: 更新時間
'''
def ID_Rest_call(user,web):
  headers={user:web}
  Ubike_ID_url = 'https://tdx.transportdata.tw/api/basic/v2/Bike/Availability/City/'+city+'?%24top=30&%24format=JSON'
  #print(Ubike_url)
  ID_res =requests.get(Ubike_ID_url,headers=headers)
  j = ID_res.json()
  with open ("Ubike.json","w",encoding='utf-8') as f:
    ID_Data=json.dump(j,f)
    f.close
  with open ("Ubike.json","r",encoding='utf-8') as f:
    ID_Data=json.load(f)
    print(ID_Data)
    for i in range(len(ID_Data)):
      ID_Rest={}
      ID_Rest["StationUID"]=ID_Data[i]["StationUID"]
      print(ID_Rest)  
      ID_Rest["AvailableRentBikes"]=ID_Data[i]["AvailableRentBikes"]  
      print(ID_Rest)
      ID_Rest["UpdateTime"]=ID_Data[i]["UpdateTime"]  
      print(ID_Rest)
      ID_Rest["StationAddress"]=ID_Data[i]["StationAddress"]  
      #ID_Rest["Time"]=distance_calc(start,ID_Rest["StationAddress"],mode='bicycling',api_key=google_api_key)[0]
      ID_Data_clean.append(ID_Rest)
      
  return ID_Data_clean

#print(distance_calc(start,end,mode='bicycling',api_key=google_api_key)[0])
def Ubike_output(time):
    if time<=600:
      print("好啦")
    elif time==400:
      print ("查無資料")
    else:
      print("三小有夠遠")
#print(ID_Data_clean)

'''
使用者輸入起點終點
透過起點地址點位得到起始位置經緯度座標
透過起始位置的經緯度座標和Ubike地指點位座標得到行程時間
行程時間小於600為適合的站位
return 所有需要輸出的資料 資料內容包含 位置,ID,距離,剩餘Ubike 數量
''' 

ID_Rest_call(enter_user,enter_web)
start=address_to_coord('嘉南藥理大學',geo_api_key, cityinfo=False)
end=address_to_coord('二仁溪流域教育中心',geo_api_key, cityinfo=False)
Ubike=address_to_coord(ID_Data_clean[0]["StationAddress"],geo_api_key, cityinfo=False)
Ubike_time= distance_calc(start, Ubike, mode='bicycling', api_key=google_api_key)[1]
Ubike_output(Ubike_time)


#Ubike_output(ID_Data_clean[0]["Time"])

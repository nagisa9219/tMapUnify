import requests
import json
from requests.structures import CaseInsensitiveDict
from  maps_api import address_to_coord, distance_calc
enter_user='user-agent'
enter_web='Mozilla/5.0'
ID_Data_clean=[]
Location_Data_clean=[]
output_data=[]
city=input()

geo_api_key='f0305e991db040688c28b59ac6d9fbd5'
google_api_key='AIzaSyB8jGb3zHAnT_47p-c-5avxJ4KieHEs7-c'

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
    headers = {user:web}
    Ubike_ID_url = 'https://tdx.transportdata.tw/api/basic/v2/Bike/Availability/City/'+city+'?%24top=30&%24format=JSON'
    #print(Ubike_url)
    ID_res =requests.get(Ubike_ID_url,headers=headers)
    j = ID_res.json()
    with open ("Ubike.json","w",encoding='utf-8') as f:
        ID_Data=json.dump(j,f)
        f.close
    with open ("Ubike.json","r",encoding='utf-8') as f:
        ID_Data=json.load(f)
        for i in range(len(ID_Data)):
            ID_Rest={}
            ID_Rest["StationUID"]=ID_Data[i]["StationUID"]  
            ID_Rest["AvailableRentBikes"]=ID_Data[i]["AvailableRentBikes"]  
            ID_Rest["UpdateTime"]=ID_Data[i]["UpdateTime"]  
            #ID_Rest["Time"]=distance_calc(start,ID_Rest["StationAddress"],mode='bicycling',api_key=google_api_key)[0]
            ID_Data_clean.append(ID_Rest)
            #print(ID_Data_clean)
    return ID_Data_clean
#print(ID_Rest_call(enter_user,enter_web))
'''
Ubike 經緯度與ID 結合
資料來源:PTX
API使用:注意沒有會員用官方文件方法可能會被擋下來
資料內容:
[{"StationUID"  str: 站點ID(格式:縣市代碼+流水號),
    "'PositionLon'"  int: 站點經度,
    "PositionLat"  int: 站點緯度,
    "UpdateTime": "2023-07-23T13:34:41.914Z"
'''
def ID_Location_call(user,web):
    headers={user:web}
    Ubike_Location_url = 'https://tdx.transportdata.tw/api/basic/v2/Bike/Station/City/'+city+'?%24top=30&%24format=JSON'
    #print(Ubike_url)
    Location_res =requests.get(Ubike_Location_url,headers=headers)
    h = Location_res.json()
    with open ("UbikeLocation.json","w",encoding='utf-8') as f:
        Location_Data=json.dump(h,f)
        f.close
    with open ("UbikeLocation.json","r",encoding='utf-8') as f:
        Location_Data=json.load(f)
        #print(Location_Data)
    for i in range(len(Location_Data)):
        ID_Location={}
        ID_Location["StationUID"]=Location_Data[i]["StationUID"]  
        ID_Location["StationName"]=Location_Data[i]['StationName']['Zh_tw']
        ID_Location["StationAddress"]=Location_Data[i]['StationAddress']['Zh_tw']
        ID_Location["PositionLon"]=Location_Data[i]["StationPosition"]['PositionLon']
        ID_Location["PositionLat"]=Location_Data[i]["StationPosition"]['PositionLat']
        ID_Location["Position"]=[Location_Data[i]["StationPosition"]['PositionLon'],Location_Data[i]["StationPosition"]['PositionLat']]
        Location_Data_clean.append(ID_Location)
    return Location_Data_clean

'''
將站點資訊和location整合

輸出內容(all_Data)
ex:
'StationUID': 'TNN501301001', 
'StationName': 'YouBike2.0_七股遊客中心', 
'StationAddress': '七股區鹽埕里鹽埕69號', 
'PositionLon': 120.10398, 
'PositionLat': 23.15375, 
"Position":120.10398, 23.15375,
'AvailableRentBikes': 5

'''
def Mix_Data():
    ID_Rest=ID_Rest_call(enter_user,enter_web)
    #print(ID_Rest)
    ID_Location=ID_Location_call(enter_user,enter_web)
    #print(ID_Location)
    # 資料總共有幾筆
    for i in range(len(ID_Location)):
    #一筆一筆找一不一樣
        for j in range(len(ID_Rest)):
            #print(ID_Location[j]['StationUID'])
            if ID_Rest[i]['StationUID']==ID_Location[j]['StationUID']:
                ID_Location[j]['AvailableRentBikes']= ID_Rest[i]['AvailableRentBikes']
    return ID_Location

all_Data=Mix_Data()

'''
起點到站點時間輸入all_Data
'''
def Ubike_judge(start_coord, Data):
   for i in range(len(Data)):
        Data[i]["duration"]=distance_calc(start_coord, Data[i]["Position"], mode='bicycling')[2]
'''
判斷是否在十分鐘裡面/輸出內容
'''

def Ubike_nearMain(location: str, coord: list[float]) ->tuple:
  """
    輸入起點後，透過其經緯度座標和Ubike地指點位座標得到行程時間小於600為適合的站位
  
    Args:
      location (str): 使用者所在的地點(英文)
      coord (list[float, float]): 使用者所在的經緯度座標

    Returns:
      statuscode, sta_inrange_dict (tuple[str, dict]): 狀態碼及站點資訊(站點位置、ID、距離、剩餘YouBike數量)
  
  """
  all_Data = Mix_Data()
  Ubike_judge(all_Data)
  for i in range(len(all_Data)):
    sta_inrange_dict = {}
    if all_Data[i]["duration"] <= 600:
        print("在範圍內")
        print(all_Data[i]['StationUID'])
        print(all_Data[i]['StationName'])
        print(all_Data[i]['AvailableRentBikes'])
        print(all_Data[i]['StationAddress'])

        sta_inrange_dict[i] = {
            "StationUID" : all_Data[i]["StationUID"],
            "StationName" : all_Data[i]["StationName"],
            "AvailableRentBikes" : all_Data[i]["AvailableRentBikes"],
            "StationAddress" : all_Data[i]["StationAddress"]
            }
      
        print(sta_inrange_dict)
        
        return "T", sta_inrange_dict
    elif all_Data[i]["duration"] == 400:
        print("查無資料")
        return "F","400: No Result"
    else:
        continue

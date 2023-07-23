'''
Ubike 即時性站點更新
資料來源:PTX(注意用官方文件方法可能會被擋下來)
資料內容:
[{"StationUID": ,
 "StationID": "501301001", 
 "ServiceStatus": 1,
   "ServiceType": 2, 
   "AvailableRentBikes": 5, 
   "AvailableReturnBikes": 20, 
   "SrcUpdateTime": "2023-07-21T11:45:03+08:00", 
   "UpdateTime": "2023-07-22T22:44:54+08:00",
     "AvailableRentBikesDetail": {"GeneralBikes": 5, "ElectricBikes": 0}}, 
'''
import requests
import json
headers={'user-agent':'Chrome/114.0.0.0'}
city=input()
train_url = 'https://tdx.transportdata.tw/api/basic/v2/Bike/Availability/City/'+city+'?%24top=30&%24format=JSON'
print(train_url)
train_res = requests.get(train_url,headers=headers)
j = train_res.json()
#print(j)
with open ("Ubike.json","w") as f:
    json.dump(j,f)
'''
print(j[0]['RouteID']['Zh_tw'])
print(j[0]['EndingStationName']['Zh_tw'])

'''
import requests
import json
headers={'user-agent':'Chrome/114.0.0.0'}
city=input()
train_url = 'https://tdx.transportdata.tw/api/basic/v2/Bus/RouteFare/City/'+city+'?%24top=30&%24format=JSON'
print(train_url)
train_res = requests.get(train_url,headers=headers)
j = train_res.json()
#print(j)
with open ("bus.json","w") as f:
    json.dump(j,f)
'''
print(j[0]['RouteID']['Zh_tw'])
print(j[0]['EndingStationName']['Zh_tw'])

'''
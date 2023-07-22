import requests
import re
import json
url = "https://www.cpc.com.tw/historyprice.aspx?n=2890"
resp = requests.get(url)
m = re.search("var pieSeries = (.*);", resp.text)
jsonstr = m.group(0).strip('var pieSeries = ').strip(";")
j = json.loads(jsonstr)
#print(j)
for item in reversed(j):
  print("date:" + item['name'])
  for data in item['data']:
    print(data['name'] + ":" + str(data['y']))
  print("======")

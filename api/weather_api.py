import requests
import json
from api_token import get_apitoken

apitoken = get_apitoken()

def weather(lad: str, lon: str):
    """
        輸入地點的經緯度已取得當地及時的氣象資訊

        Args:
            lad, lon (float): 地點的經緯度座標
    
    """
    url="https://api.openweathermap.org/data/2.5/weather?lat=" + lon + "&lon=" + lad + "&appid=" + apitoken["openweather"]
    date={}
    resp=requests.get(url).json()

    with open ("weather.json","w") as f:
        json.dump(resp,f)

    with open("weather.json") as read:
        data = json.load(read)
    main_data=data["weather"][0]["description"]
    
    return main_data
#print(type(weather("30","30")))
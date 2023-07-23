import requests
import json

def weather(lad: float, lon: float):
    """
        輸入地點的經緯度已取得當地及時的氣象資訊

        Args:
            lad, lon (float): 地點的經緯度座標
    
    """
    url="https://api.openweathermap.org/data/2.5/weather?lat="+lad+"&lon="+lon+"&appid=d11faca77d78a15c85b9a1f1ea09dcd2"
    date={}
    resp=requests.get(url).json()

    with open ("weather.json","w") as f:
        json.dump(resp,f)

    with open("weather.json") as read:
        data = json.load(read)
    main_data=data["weather"][0]["description"]
    
    return main_data
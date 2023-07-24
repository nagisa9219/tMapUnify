import json
import requests
from requests.structures import CaseInsensitiveDict

def address_to_coord(address: str, cityinfo: bool=False) -> tuple[str, float, float]:
    """
        此function透過Geogapify Geocode API將地址轉換為經緯度座標
        
        Args:
            address (str): 欲轉換的地址
            cityinfo (bool): 顯示該地址位於的縣市英文名稱(概略)，可略

        Returns:
            statuscode, lat, lot (str, float, float): 地址轉換過後的經緯度座標(cityinfo == False時)
            [cityname (str)]: 出發地點所屬的縣市名稱(概略, cityinfo == True時)
    """

    url = "https://api.geoapify.com/v1/geocode/search?text=" + address + "&apiKey=f0305e991db040688c28b59ac6d9fbd5"
    headers = CaseInsensitiveDict()
    headers["Accept"] = "application/json"


    resp = requests.get(url, headers=headers).json()
    if resp["features"] == []:
        return "F",[400,400]
    elif cityinfo == False:
        coord = resp["features"][0]["geometry"]["coordinates"]
        return "T",coord
    elif cityinfo == True:
        city = resp["features"][0]["properties"]["city"]
        return city

def distance_calc(coord1: list[float], coord2: list[float], mode: str) :
    """
        計算起始點與目的地的路線距離並依交通方式計算通行時間

        Args:
            coord1, coord2 (list[float]): 起始,目的地的經緯度座標
            mode (str) ={driving|bicycling|walking|transit}: 交通方式
        
        Returns:
            statuscode, distance, duration (str, int, float): 狀態碼及計算過後的交通距離和花費時間(單位：公里,秒)
                statuscode = {"T"|"F"}: T: 正常, F: 異常
    """

    url = "https://maps.googleapis.com/maps/api/distancematrix/json?origins=" + str(coord1[1]) + "%2C" + str(coord1[0]) + "&destinations=" + str(coord2[1]) + "%2C" + str(coord2[0]) + "&mode=" + mode +"&key=AIzaSyB8jGb3zHAnT_47p-c-5avxJ4KieHEs7-c"
    payload = {}
    headers = {}
    resp = requests.get(url, headers=headers, data=payload).json()
    print(resp["rows"][0]["elements"][0])
    if resp["rows"][0]["elements"][0]["status"] == "NOT_FOUND":
        return "F",0,0
    else:
        distance = float(resp["rows"][0]["elements"][0]["distance"]["value"])*0.001 #m->km
        duration = int(resp["rows"][0]["elements"][0]["duration"]["value"])
        return "T",distance, duration

def taxi_calc(distance: float, city: str) -> int:
    """
        利用行車距離及出發地所在縣市估算計程車車資
        *未於下方列出的縣市為查無資料，並以平均值估算之

        Args:
            distance (float): 行車距離(單位：公里)
            city (str): 出發地所在縣市(英文名稱)
        
        Returns:
            fare (int): 估算的車資
    
    """
    if city == "Keelong" or city == "New Taipei" or city == "Taipei":
        return (85 + ((distance*1000-1250)/200)*5)
    elif city == "Taoyuan City" or city == "Taoyuan":
        return (90 + ((distance*1000-1250)/200)*5)
    elif city == "Hsinchu":
        return (100 + ((distance*1000-1250)/200)*5)
    elif city == "Taichung":
        return (85 + ((distance*1000-1500)/200)*5)
    elif city == "Taibao City" or city == "CHiayi":
        return (100 + ((distance*1000-1250)/220)*5)
    elif city == "Tainan":
        return (85 + ((distance*1000-1250)/200)*5)
    elif city == "Kaoshiung":
        return (85 + ((distance*1000-1250)/200)*5)
    elif city == "Maioli City" or city == "Maioli":
        return (100 + ((distance*1000-1250)/200)*5)
    elif city == "Douliu City" or city == "Douliu" or city == "Yunlin":
        return (100 + ((distance*1000-1250)/220)*5)
    elif city == "Zhanghua City" or city == "Zhanghua":
        return (100 + ((distance*1000-1500)/250)*5)
    else:
        return (90 + ((distance*1000-1250)/200)*5)
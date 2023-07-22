import json
import requests
from requests.structures import CaseInsensitiveDict

def address_to_coord(address: str, api_key: str) -> list[float]:
    """
        此function透過Geogapify Geocode API將地址轉換為經緯度座標
        
        Args:
            address (str): 欲轉換的地址
            api_key (str): API的key

        Returns:
            list: 地址轉換過後的經緯度座標
    """

    url = "https://api.geoapify.com/v1/geocode/search?text=" + address + "&apiKey=" + api_key

    headers = CaseInsensitiveDict()
    headers["Accept"] = "application/json"

    resp = requests.get(url, headers=headers).json()

    coord = resp["features"][1]["geometry"]["coordinates"]

    return coord


def distance_cacl(coord1: list[float], coord2: list[float], mode: str, api_key: str) :
    """
        計算起始點與目的地的路線距離並依交通方式計算通行時間

        Args:
            coord1, coord2: list[float] 起始,目的地的經緯度座標
            mode: str {driving|bicycling|walking|transit} 交通方式
            api_key: str API的key
        
        Returns:
            distance, duration: str 計算過後的交通距離及花費時間

    """

    url = "https://maps.googleapis.com/maps/api/distancematrix/json?origins=" + str(coord1[0]) + "%2C" + str(coord1[1]) + "&destinations=" + str(coord2[0]) + "%2C" + str(coord2[1]) + "&mode=" + mode +"&key=" + api_key
    payload = {}
    headers = {}

    resp = requests.get(url, headers=headers, data=payload).json()
    distance = resp["rows"][0]["elements"][0]["distance"]["text"]
    duration = resp["rows"][0]["elements"][0]["duration"]["text"]
    
    return distance, duration
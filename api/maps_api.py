import json
import requests
from requests.structures import CaseInsensitiveDict

def address_to_coord(address: str) -> list:
    """
        此function透過Geogapify Geocode API將地址轉換為經緯度座標
        
        Args:
            address (str): 欲轉換的地址

        Returns:
            list: 地址轉換過後的經緯度座標
    """

    url = "https://api.geoapify.com/v1/geocode/search?text=" + address + "&apiKey=f0305e991db040688c28b59ac6d9fbd5"

    headers = CaseInsensitiveDict()
    headers["Accept"] = "application/json"

    resp = requests.get(url, headers=headers).json()

    coord = resp["features"][1]["geometry"]["coordinates"]

    return coord
print(address_to_coord("新北市蘆洲區中山二路265巷25號"))


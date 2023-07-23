# from api.maps_api import address_to_coord
import requests
from requests.structures import CaseInsensitiveDict


def address_to_coord(address: str,api_key: str, cityinfo: bool=False) -> list[float]:
    """
        此function透過Geogapify Geocode API將地址轉換為經緯度座標
        
        Args:
            address (str): 欲轉換的地址
            api_key (str): API的key
            cityinfo (bool): 顯示該地址位於的縣市英文名稱(概略)，可略

        Returns:
            lat, lot (float, float): 地址轉換過後的經緯度座標(cityinfo == False時)
            [cityname (str)]"
            [errorcode (str): 若查無地址或其他錯誤，則僅回傳此項]
    """

    url = "https://api.geoapify.com/v1/geocode/search?text=" + address + "&apiKey=" + api_key
    headers = CaseInsensitiveDict()
    headers["Accept"] = "application/json"


    resp = requests.get(url, headers=headers).json()
    # print(resp.status_code)
    if resp["features"] == []:
        return "400"
    elif cityinfo == False:
        coord = resp["features"][0]["geometry"]["coordinates"]
        return coord
    elif cityinfo == True:
        city = resp["features"][0]["properties"]["city"]
        return city
    
print(address_to_coord("陽明交通大學光復校區", "f0305e991db040688c28b59ac6d9fbd5"))
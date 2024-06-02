import configparser
import os

current_path = os.path.join(os.path.dirname(__file__))
config_path = os.path.abspath(current_path+os.path.sep+"../.."+os.path.sep+"config/config.ini")
config = configparser.ConfigParser()
config.read(config_path)
class token:
    def teleBotToken():
        return config["token"]["teleBotToken"]
    
    def googleMapsToken():
        return config["token"]["googleMapsToken"]
    
    def tdxToken():
        return config["token"]["tdxToken"]
    
    def geoToken():
        return config["token"]["geoToken"]

    def openWeatherToken():
        return config["token"]["openWeatherToken"]

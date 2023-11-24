import requests
from datetime import datetime
import time
from pymongo import MongoClient
from bson.objectid import ObjectId

const = ("<APIKEY>", "Pączkowo")
APIKey, city = const

def process(db):
    response = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={APIKey}")

    if response.ok:
        data = response.json()
        doc = data_to_dict(data)
        db.weather.insert_one(doc)
        # print(text)
        # with open("weather.txt", "w", encoding="UTF8") as file:
        #     file.writelines(text)
    else:
        print(response)


def data_to_dict(data):
    temp_k_to_c = lambda x: round(float(x) - 273.15, 2)
    return {
        "temp": temp_k_to_c(data['main']['temp']),
        "min_temp": temp_k_to_c(data['main']['temp_min']),
        "max_temp": temp_k_to_c(data['main']['temp_max']),
        "feels_like": temp_k_to_c(data['main']['feels_like']),
        "humidity": data['main']['humidity'],
        "pressure": data['main']['pressure'],
        "description": data['weather'][0]['description'],
        "time": datetime.now().strftime('%H-%M-%S'),
        "date": datetime.now().strftime('%y-%m-%d'),
        "city": city,
    }
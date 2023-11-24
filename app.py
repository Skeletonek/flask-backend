from flask import Flask, request
from database import db
from utils.show_json import show_json
from bson import ObjectId
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from utils.regex import password_regex, email_regex
import utils.weather
import re
import threading
import schedule
import time

app = Flask(__name__)

cors = CORS(app)
app.config['CORS_HEADERS'] = "Content-Type"

@app.route("/create-travel",methods=["GET","POST"])
def create_travel():
    title = request.json['title']
    price = request.json['price']
    country = request.json['country']
    desc = request.json['desc']
    image = request.json['image']

    travel_exists = db.travels.find_one({"title":title})

    if travel_exists:
        return show_json("Wycieczka o podanej nazwie już istnieje", 405, False)
    
    db.travels.insert_one({
        "title": title,
        "price": price,
        "country": country,
        "desc": desc,
        "image": image
    })

    return show_json("Udało się dodać nową wycieczkę", 200, True)


@app.route("/all-travels", methods=["GET", "POST"])
def all_travels():
    data = db.travels.find({})
    travels = []
    for item in data:
        item['_id'] = str(item['_id'])
        travels.append(item)
    return show_json("Pobrano listę wszystkich wycieczek", 200, True, travels)


@app.route("/travel-title/<title>", methods=["GET", "POST"])
def travel_title(title):
    data = db.travels.find_one({"title": {'$regex': "(?i)"+title}})

    if not data:
        return show_json("Nie znaleziono wycieczki o podanej nazwie", 404, False)
    
    data['_id'] = str(data['_id'])
    return show_json("Pobrano dane wycieczki po jej nazwie", 200, True, data)


@app.route("/edit-travel/<id>", methods=["PUT"])
def edit_travel(id):
    try:
        travel_json = request.json
        travel = db.travels.update_one({"_id":ObjectId(id)},{"$set":travel_json})
        if travel.modified_count == 1:
            return show_json("Pomyślnie zmodyfikowano dane", 200, True)
        return show_json("Nie odnaleziono wycieczki", 404, False)
    except Exception as e:
        print(str(e))
        return show_json("Nie udało się zmodyfikować wycieczki", 500, False)
    

@app.route("/delete-travel/<id>", methods=["DELETE"])
def delete_travel(id):
    try:
        result = db.travels.delete_one({"_id": ObjectId(id)})
        if result.deleted_count == 1:
            return show_json("Pomyślnie usunięto wycieczke", 200, True)
        return show_json("Nie odnaleziono wycieczki", 404, False)
    except Exception as e:
        print(str(e))
        return show_json("Nie udało się usunąć wycieczki", 500, False)
    

@app.route("/weather-newest")
def show__newest_weather():
    data = db.weather.find({}).sort({"_id":-1}).limit(1)
    if not data:
        return show_json("Nie znaleziono danych pogodowych", 404, False)
    weathers = []
    for item in data:
        item['_id'] = str(item['_id'])
        weathers.append(item)
    return show_json("Pobrane obecne dane pogodowe", 200, True, weathers)


@app.route("/weather")
def show_all_weather():
     data = db.weather.find({}).sort({"_id":-1})
     weather = []
     for item in data:
        item['_id'] = str(item['_id'])
        weather.append(item)
     return show_json("Udało się pobrać dane",200,True,weather) 


# -------------------------------------------------------------

@app.route("/register", methods=["POST"])
def register():
    username = request.json['username']
    email = request.json['email']
    password = request.json['password']
    hashed_password = generate_password_hash(password)
    
    if re.match(password_regex, password) is None:
        return show_json("Hasło musi zawierać małą, dużą literę, cyfrę i minimum 8 znaków", 400, False)
    
    if re.match(email_regex, email) is None:
        return show_json("Podano niepoprawny adres email", 400, False)

    user = {
        "username": username,
        "email": email,
        "password": hashed_password
    }

    db.users.insert_one(user)

    user['_id'] = str(user['_id'])

    return show_json("Użytkownik pomyślnie zarejestrowany", 201, True, user)


# -------------------------------------------------------------


# def download_weather_data():
#     weather.process(db)
#     threading.Timer(60.0, download_weather_data).start()

# download_weather_data()
from flask import Flask, request, jsonify
from database import db
from utils.show_json import show_json
from bson import json_util
from bson import ObjectId
import json
from flask_cors import CORS

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
    

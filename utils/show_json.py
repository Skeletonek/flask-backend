from flask import jsonify

def show_json(message, status, ok, data={}):
    return jsonify({
            "message": message,
            "status": status,
            "ok": ok,
            "data": data
        })
    
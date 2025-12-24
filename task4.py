
from flask import Flask
from flask import request
from flask import jsonify
from functools import wraps

app = Flask(__name__)
#Dictionary(Users)
users = {
    "user1": "pass1",
    "user2": "pass2"
}
#Dictionary(items)
items = [

    {"id": 1, "name": "CD", "price": 250 },
    {"id": 2, "name": "Vynil", "price": 1250 },
    {"id": 3, "name": "Tape", "price": 750 }
]

def check_auth(username, password):
    if username in users and users[username] == password:
        return True
    else:
        return False

def authenticate():
    return jsonify({"error":"Authorization required"}), 401

def auth_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()

        return f(*args, **kwargs)

    return decorator

@app.route("/items", methods=["POST","GET" ])
@auth_required
def item_list():
    if request.method == "GET":
        return jsonify(items)

    if request.method == "POST":
        data = request.get_json()
        if not data or "name" not in data or "price" not in data:
            return jsonify({"error": "Invalid data"}), 400

        new_id = max(item["id"] for item in items) + 1
        new_item = {"id": new_id, "name": data["name"], "price": data["price"]}

        items.append(new_item)
        return jsonify(new_item), 201

@app.route("/items/<int:item_id>", methods=["GET","PUT","DELETE"])
@auth_required
def item_red(item_id):
    item = None
    for i in items:
        if i["id"] == item_id:
            item = i
            break

    if not item:
        return jsonify({"error": "Item not found"}), 404

    if request.method == "GET":
        return jsonify(item)

    if request.method == "PUT":
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid data"}), 400

        if "name" in data:
             item["name"] = data["name"]

        if "price" in data:
            item["price"] = data["price"]

        return jsonify({"message": "Item updated"})

    if request.method == "DELETE":
        items.remove(item)
        return jsonify({"message": "Item deleted"})


if __name__ == '__main__':
    app.run(port=8000)
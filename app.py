import uuid
from flask import Flask, request
from db import stores, items

app = Flask(__name__)


@app.get("/store")      #http://127.0.0.1:5000/store
def get_stores() -> list: 
    return {"stores": list(stores.values())}

# retrieves the entire store's contents
@app.get("/store/<string:store_id>")    #http://127.0.0.1:5000/store/<name>
def get_store(store_id):
    try:
        return stores["store_id"]
    except KeyError:
        return {"message": "Store not found"}, 404

# retrieves items from a specific store
@app.get("/store/<string:name>/item")   #http://127.0.0.1:5000/store/<name>/item
def get_item_in_store(name):
    for store in stores:
        if store["name"] == name:
            return {"items": store["items"]}
    return {"message": "Store not found"}, 404

@app.post("/store")     #http://127.0.0.1:5000/store
def create_stores() -> dict:
    store_data = request.get_json()
    store_id = uuid.uuid4().hex
    
    store = {**store_data, "id": store_id}
    stores[store_id] = store
    
    return store, 201

@app.post("/store/<string:name>/item")
def create_item(name):
    request_data = request.get_json()
    for store in stores:
        if store["name"] == name:
            new_item = {"name": request_data["name"], "price": request_data["price"]}
            store["items"].append(new_item)
            return new_item, 201

    return {"message": "Store not found"}, 404


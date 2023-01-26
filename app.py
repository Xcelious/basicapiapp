import uuid
from flask import Flask, request
from db import stores, items


app = Flask(__name__)


@app.get("/store")      #http://127.0.0.1:5000/store
def get_stores() -> dict: 
    return {"stores": list(stores.values())}

# retrieves the entire store's contents
@app.get("/store/<string:store_id>")    #http://127.0.0.1:5000/store/<name>
def get_store(store_id):
    try:
        return stores[store_id]
    except KeyError:
        return {"message": "Store not found"}, 404

# retrieves items from a specific store
@app.get("item/<string:item_id>")   #http://127.0.0.1:5000/store/<name>/item
def get_item(item_id):
    try:
        return items[item_id]
    except KeyError:
        return {"message": "Item not found"}, 404

@app.post("/store")     #http://127.0.0.1:5000/store
def create_stores() -> dict:
    store_data = request.get_json()
    store_id = uuid.uuid4().hex     #generates unique id per resource

    # unpacks the values from the <store_data> dict and adds
    # to the <store> dict, along with the unique ID
    store = {**store_data, "id": store_id}
    stores[store_id] = store

    return store, 201

@app.post("/item")
def create_item(name):
    item_data = request.get_json()
    if item_data["store_id"] not in stores:
        return {"message": "Store not found"}, 404

    item_id = uuid.uuid4().hex
    item = {**item_data, "id": item_id}
    items[item_id] = item

    return item, 201

@app.get("/item")
def get_all_items():
    return {"items": list(items.values())}

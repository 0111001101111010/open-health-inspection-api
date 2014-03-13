from pymongo import MongoClient
from bson.objectid import ObjectId
import json
from bson import json_util
from flask import Flask, Response

app = Flask(__name__)

client = MongoClient('mongodb://cfa:cfa123@ds033639.mongolab.com:33639/healthdata')
db = client.healthdata

@app.route('/')
def api_root():
    return 'Welcome'

@app.route('/restaurants')
def api_restaurants():
    data = db.va.find({}, {'name': 1, 'address': 1})

    if data.count() > 0:
        restaurant_list = []
        for item in data:
            restaurant_list.append(item)

        resp = Response(json.dumps(restaurant_list, default=json_util.default), mimetype='application/json')
    else:
        resp = Response(status=204)

    return resp

@app.route('/restaurants/<restaurantid>')
def api_restaurant(restaurantid):
    data = db.va.find({'_id': ObjectId(restaurantid)}, {'name': 1, 'address': 1, 'inspections': { '$slice': 1}})

    if data.count() == 1:
        resp = Response(json.dumps(data[0], default=json_util.default), mimetype='application/json')
    elif data.count() > 1:
        resp = Response(status=300)
    else:
        resp = Response(status=204)

    return resp

if __name__ == '__main__':
    app.run()
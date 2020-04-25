from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from pymongo import MongoClient

app = Flask(__name__)
api = Api(app)

client = MongoClient("mongodb://db:27017")
db = client.aNewDB
user_num = db["UserNum"]

user_num.insert({
    'num_of_users':0
})

class Visit(Resource):
    def get(self):
        previous_number = user_num.find({})[0]['num_of_users']
        new_number = previous_number + 1
        user_num.update({}, {"$set" : {"num_of_users":new_number}})
        return "Hello user " + str(new_number)

def check_posted_data(posted_data, function_name):
    if function_name == "add":
        if "x" not in posted_data or "y" not in posted_data:
            return 301
        else:
            return 200

class Add(Resource):
    def post(self):
        posted_data = request.get_json()

        status_code = check_posted_data(posted_data, "add")
        
        if status_code != 200:
            ret_json = {"Message": "An error occured", "Status Code": status_code}
            return jsonify(ret_json)

        x = posted_data["x"]
        y = posted_data["y"]

        x = int(x)
        y = int(y)

        ret = x + y
        ret_map = {"Message":ret, "Status Code":200}

        return jsonify(ret_map)

class Subtract(Resource):
    pass

class Multiply(Resource):
    pass

class Divide(Resource):
    pass


api.add_resource(Add, "/add")
api.add_resource(Visit, "/hello")

@app.route('/')
def hello_world():
    return "Hello world!"


if __name__ == "__main__":
    app.run(host='0.0.0.0')


from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from pymongo import MongoClient
import bcrypt

app = Flask(__name__)
api = Api(app)

client = MongoClient("mongodb://db:27017")
db = client.SentencesDatabase
users = db["Users"]

class Register(Resource):
	def post(self):

		posted_data = request.get_json()

		username = posted_data["username"]
		password = posted_data["password"]

		hashed_pw = bcrypt.hashpw(password.encode("utf8"), bcrypt.gensalt())


		users.insert({
			"Username": username,
			"Password": hashed_pw,
			"Sentence": "",
			"Tokens": 6

		})


		ret_json = {
			"status": 200,
			"msg": "You successfully signed up for the API"
		}


		return jsonify(ret_json)


def verify_pw(username, password):
	hashed_pw = users.find({
		"Username": username
	})[0]["Password"]

	return bcrypt.hashpw(password.encode("utf8"), bcrypt.gensalt()) == hashed_pw

def count_tokens(username):
	tokens = users.find({
		"Username": username
	})[0]["Tokens"]

	return tokens


class Store(Resource):
	def post(self):

		posted_data = request.get_json()

		username = posted_data["username"]
		password = posted_data["password"]
		sentence = posted_data["sentence"]

		correct_pw = verify_pw(username, password)

		if not correct_pw:
			ret_json = {
				"status": 302
			}

			return jsonify(ret_json)


		num_tokens = count_tokens(username)

		if num_tokens <= 0:
			ret_json = {
				"status": 301
			}

			return jsonify(ret_json)


		users.update({"Username": username}, {"$set": {"Sentence": sentence, "Tokens": num_tokens-1}})

		ret_json = {
			"status": 200,
			"msg": "sentence saved successfully"
		}

		return jsonify(ret_json)


class Get(Resource):
	def post(self):
		posted_data = request.get_json()

		username = posted_data["username"]
		password = posted_data["password"]

		correct_pw = verify_pw(username, password)

		if not correct_pw:
			ret_json = {
				"status": 302
			}
			return jsonify(ret_json)

		num_tokens = count_tokens(username)

		if num_tokens <= 0:
			ret_json = {
				status: 301
			}
			return jsonify(ret_json)


		users.update({"Username", username}, {"$set": {"Tokens": num_tokens-1}})

		sentence = users.find({"Username": Username})[0]["Sentence"]

		ret_json = {
			"status": 200
			"sentence": str(sentence)
		}

		return jsonify(ret_json)


api.add_resource(Register, '/register')
api.add_resource(Store, '/store')
api.add_resource(Get, '/get')


if __name__ == "__main__":
	app.run(host='0.0.0.0')
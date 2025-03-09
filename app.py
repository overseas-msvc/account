import json
import base64
from flask import Flask, request, jsonify
from flask_cors import CORS

from db_manage.mysql_connector.database import Database


app = Flask(__name__)
CORS(app)

@app.route("/accounts", methods=["GET"])
def get_accounts():
	data = request.json
	db = Database("account")
	conditions = data["filter"] if "filter" in data else {}
	objects = db.get_list_of_objects("account", conditions, inJson=True)
	return json.dumps(objects), 200

@app.route("/account", methods=["GET"])
def get_account():
	data = request.json
	db = Database("account")
	objects = db.get_object_by_id("account", data["id"], inJson=True)
	return json.dumps(objects), 200
	

@app.route("/account", methods=["POST"])
def create_account():
	data = request.json
	db = Database("account")
	if db.get_list_of_objects("account", { "name": data["name"]}):
		return "account with this name already exists", 400
	else:
		id = db.add_object("account", data)
		return json.dumps({"id": id}), 201


@app.route("/account", methods=["PUT"])
def update_account():
	data = request.json
	db = Database("account")
	id = data["id"]
	del data["id"]
	db.update_object("account", id, data)
	return "", 204


@app.route("/account", methods=["DELETE"])
def delete_account():
	data = request.json
	db = Database("account")
	db.delete_object("account", data["id"])
	return "", 204


@app.route("/users", methods=["GET"])
def get_users():
	data = request.json
	db = Database("account")
	conditions = data["filter"] if "filter" in data else {}
	objects = db.get_list_of_objects("user", conditions, inJson=True)
	return json.dumps(objects), 200

@app.route("/user", methods=["GET"])
def get_user():
	data = request.json
	db = Database("account")
	objects = db.get_object_by_id("user", data["id"], inJson=True)
	return json.dumps(objects), 200
	

@app.route("/user", methods=["POST"])
def create_user():
	data = request.json
	db = Database("account")
	id = db.add_object("user", data)
	return json.dumps({"id": id}), 201


@app.route("/user", methods=["PUT"])
def update_user():
	data = request.json
	db = Database("account")
	id = data["id"]
	del data["id"]
	db.update_object("user", id, data)
	return "", 204


@app.route("/user", methods=["DELETE"])
def delete_user():
	data = request.json
	db = Database("account")
	db.delete_object("user", data["id"])
	return "", 204

@app.route("/login", methods=["POST"])
def login():
	data = request.json
	db = Database("account")
	user = db.get_list_of_objects("user", {"name": data["username"]})
	if user:
		user = user[0]
	else:
		user = db.get_list_of_objects("user", {"email": data["username"]})
		if user:
			user = user[0]
		else:
			return f"no such user {data["username"]}", 405
	if base64.b64decode(data["password"]) != base64.b64decode(user.encrypted_password):
		return jsonify({"message": "wrong password"}), 401

	return json.dumps({"userId": user.id, "accountId": user.account_id}), 200


@app.route("/signup", methods=["POST"])
def signup():
	data = request.json
	if data["accountName"] == '':
		return jsonify({"message": f"invalid account name"}), 401
	if data["username"] == '':
		return jsonify({"message": f"invalid username"}), 401
	if data["email"] == '':
		return jsonify({"message": f"invalid email"}), 401
	if data["password"] == '':
		return jsonify({"message": f"invalid password"}), 401
	db = Database("account")
	account = db.get_list_of_objects("account", {"name": data["accountName"]})
	if account:
		account_id = account[0].id
	else:
		account_id = db.add_object("account", {"name": data["accountName"]})
	user = db.get_list_of_objects("user", {"name": data["username"],
							 	"account_id": account_id})
	if user:
		return jsonify({"message": f"user '{user[0].name}' already exists in account {data["accountName"]}"}), 401
	user_id = db.add_object("user", data={"name": data["username"],
							 	"account_id": account_id,
								"email": data["email"],
								"encrypted_password": data["password"]})
	# verify email
	return {"userId": user_id, "accountId": account_id}


if __name__ == "__main__":
	app.run(host="0.0.0.0", debug=True)
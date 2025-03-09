import json
from flask import Flask, request

from db_manage.mysql_connector.database import Database


app = Flask(__name__)

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



if __name__ == "__main__":
	app.run(host="0.0.0.0", debug=True)
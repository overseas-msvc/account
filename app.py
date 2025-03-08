import json
from flask import Flask, request

from db_manage.mysql_connector.database import Database


app = Flask(__name__)

@app.route("/account", methods=["GET"])
def get_account():
	data = request.json
	db = Database("account")
	objects = db.get_list_of_objects("account", data, inJson=True)
	return json.dumps(objects)
	

@app.route("/account", methods=["POST"])
def create_account():
	data = request.json
	db = Database("account")
	id = db.add_object("account", data)
	return json.dumps({"id": id})


@app.route("/user", methods=["GET"])
def get_user():
	data = request.json
	db = Database("account")
	objects = db.get_list_of_objects("user", inJson=True)
	return json.dumps(objects)
	

@app.route("/user", methods=["POST"])
def create_user():
	data = request.json
	db = Database("account")
	id = db.add_object("user", data)
	return json.dumps({"id": id})

if __name__ == "__main__":
	app.run(host="0.0.0.0", debug=True)
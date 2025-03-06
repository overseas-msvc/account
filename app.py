from flask import Flask, request

app = Flask(__name__)

@app.route("/account", methods=["GET"])
def get_account():
	data = request.json
	return f"reply from endpoint get_account, data = {data}"

@app.route("/account", methods=["POST"])
def create_account():
	data = request.json
	return f"reply from endpoint create_account, data = {data}"

if __name__ == "__main__":
	app.run(host="0.0.0.0", debug=True)
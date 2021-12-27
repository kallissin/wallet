from flask import Flask, jsonify


app = Flask(__name__)

@app.get("/")
def get_all():
    return jsonify({"message": "initial aplication"}), 200

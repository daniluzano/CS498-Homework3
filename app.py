from flask import Flask, request, jsonify
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from pymongo.write_concern import WriteConcern
from pymongo.read_preferences import ReadPreference

app = Flask(__name__)

uri = "mongodb+srv://dluzano2:nDspug5Gr3FE04TW@hw3.iukqnly.mongodb.net/?retryWrites=true&w=majority&appName=hw3"

client = MongoClient(uri, server_api=ServerApi('1'))

db = client["ev_db"]
collection = db["vehicles"]


@app.route("/")
def home():
    return "API is running"


@app.route("/insert-fast", methods=["POST"])
def insert_fast():
    data = request.get_json()

    if data is None:
        return jsonify({"error": "No JSON payload provided"}), 400

    fast_collection = collection.with_options(write_concern=WriteConcern(w=1))
    result = fast_collection.insert_one(data)

    return jsonify({"inserted_id": str(result.inserted_id)})


@app.route("/insert-safe", methods=["POST"])
def insert_safe():
    data = request.get_json()

    if data is None:
        return jsonify({"error": "No JSON payload provided"}), 400

    safe_collection = collection.with_options(write_concern=WriteConcern("majority"))
    result = safe_collection.insert_one(data)

    return jsonify({"inserted_id": str(result.inserted_id)})


@app.route("/count-tesla-primary", methods=["GET"])
def count_tesla_primary():
    primary_collection = collection.with_options(read_preference=ReadPreference.PRIMARY)
    count = primary_collection.count_documents({"Make": "TESLA"})

    return jsonify({"count": count})


@app.route("/count-bmw-secondary", methods=["GET"])
def count_bmw_secondary():
    secondary_collection = collection.with_options(read_preference=ReadPreference.SECONDARY_PREFERRED)
    count = secondary_collection.count_documents({"Make": "BMW"})

    return jsonify({"count": count})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
from flask import Flask, request, jsonify
from controller import store_data, get_data_sensor, delete_all_data
from dotenv import load_dotenv
import os

load_dotenv(verbose=True)

LOCALHOST = os.getenv("IP4_ADDRESS")
PORT = os.getenv("PORT")

app = Flask(__name__)


@app.route("/api/sensor/store_data", methods=["POST"])
def store_data_from_sensor():
    data = request.json
    try:
        store_data(data)
        return jsonify({"status": True, "message": "Data stored successfully"}), 201
    except Exception as e:
        return jsonify({"status": False, "message": str(e)}), 500

@app.route("/api/sensor/get_data", methods=["GET"])
def get_data_from_db():
    try:
        data = get_data_sensor()
        return jsonify(
            {"status": True, "message": "Data retrieved successfully", "data": data}
        ), 200
    except Exception as e:
        return jsonify({"status": False, "message": str(e)}), 500

@app.route("/api/sensor/delete_all_data", methods=["DELETE"])
def delete_all_data_from_db():
    try:
        delete_all_data()
        return jsonify({"status": True, "message": "Data deleted successfully"}), 200
    except Exception as e:
        return jsonify({"status": False, "message": str(e)}), 500

@app.route("/api/", methods=["GET"])
def home():
    return jsonify({"message": "Welcome to the API"}), 200


if __name__ == "__main__":
    app.run(debug=True, port=int(PORT), host=LOCALHOST)

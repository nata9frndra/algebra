from flask import Flask, request, jsonify
from pymongo import MongoClient
import os

app = Flask(__name__)

# MongoDB Configuration (Replace with actual credentials)
MONGO_URI = "mongodb+srv://asantas152:4O3zn3XxJ6P6oXtS@cluster0.htmak.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
DB_NAME = "ALGEBRA"
COLLECTION_NAME = "algebra"

# Initialize MongoDB Client
client = MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

@app.route('/save', methods=['POST'])
def save_data():
    data = request.get_json()
    temperature = data.get("temperature")
    humidity = data.get("humidity")
    
    if temperature is None or humidity is None:
        return jsonify({"error": "Temperature and humidity are required."}), 400
    
    record = {"temperature": temperature, "humidity": humidity}
    collection.insert_one(record)
    
    return jsonify({"message": "Data saved successfully."}), 201

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')

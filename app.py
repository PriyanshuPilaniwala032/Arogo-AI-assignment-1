import numpy as np
from flask import Flask, request, jsonify, render_template
import pickle
import pandas as pd

app = Flask(__name__)
model = pickle.load(open("model.pkl", "rb"))

vehicle_type_encoding = {'Container': 0, 'Lorry': 1, 'Trailer': 2, 'Truck': 3}
weather_encoding = {'Clear': 0, 'Fog': 1, 'Rain': 2, 'Storm': 3}
traffic_encoding = {'Heavy': 0, 'Light': 1, 'Moderate': 2}

@app.route("/predict", methods = ["POST"])
def predict():
    try:
        data = request.get_json() 
        vehicle_type = data.get("Vehicle Type")
        weather = data.get("Weather Conditions")
        traffic = data.get("Traffic Conditions")
        print(vehicle_type, weather, traffic)

        vehicle_type_encoded = vehicle_type_encoding.get(vehicle_type, -1)
        weather_encoded = weather_encoding.get(weather, -1)
        traffic_encoded = traffic_encoding.get(traffic, -1)
        data = {
            "Vehicle Type": [vehicle_type_encoded],
            "Weather Conditions": [weather_encoded],
            "Traffic Conditions": [traffic_encoded]
        }

        df = pd.DataFrame(data)
        prediction = model.predict(df)

        result = int(prediction[0]) 

        return jsonify({"prediction": "Delayed" if result == 1 else "On Time"})

    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(debug=True)
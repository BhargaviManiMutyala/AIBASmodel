from flask import Flask, request, jsonify
import pickle
import numpy as np
import requests

# Load the saved model
with open("C:/Users/bharg/Downloads/rf_model.pkl", "rb") as f:
    model = pickle.load(f)

app = Flask(__name__)

# ThingSpeak API Keys
THINGSPEAK_WRITE_KEY = "6L8XNFIEHPBBHE6R"
THINGSPEAK_CHANNEL_ID = "2848943"

@app.route('/predict', methods=['GET'])
def predict():
    try:
        # Get input from URL parameters (e.g., ?x=5)
        value = float(request.args.get("x"))
        prediction = model.predict(np.array([[value]]))[0]

        # Send prediction to ThingSpeak
        ts_url = f"https://api.thingspeak.com/update?api_key={THINGSPEAK_WRITE_KEY}&field1={prediction}"
        response = requests.get(ts_url)

        return jsonify({"prediction": prediction, "ThingSpeak_response": response.text})
    
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

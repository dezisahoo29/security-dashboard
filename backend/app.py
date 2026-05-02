from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import numpy as np
import os
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import IsolationForest

app = Flask(__name__)
CORS(app)

# Load dataset (for training model)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(BASE_DIR, '..', 'data', 'data.csv')

df = pd.read_csv(data_path)

# Use numeric columns only
X = df.select_dtypes(include=[np.number])

# Scale data
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Train model
model = IsolationForest(contamination=0.1, random_state=42)
model.fit(X_scaled)

@app.route('/')
def home():
    return "Security Dashboard API is Running"

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()

        # Get input features
        features = np.array(data['features']).reshape(1, -1)

        # OPTIONAL ML prediction (still included for assignment)
        features_scaled = scaler.transform(features)
        prediction = model.predict(features_scaled)

        # 🔥 NEW LOGIC (CLEAR RISK CLASSIFICATION)
        avg_value = np.mean(features)

        if avg_value >= 1000:
            threat_score = 85
            risk_level = "High Risk"
        elif avg_value >= 100:
            threat_score = 55
            risk_level = "Medium Risk"
        else:
            threat_score = 25
            risk_level = "Low Risk"

        # Result label
        result = "Threat Detected" if prediction[0] == -1 else "Normal Activity"

        return jsonify({
            "result": result,
            "threat_score": threat_score,
            "risk_level": risk_level
        })

    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(debug=True)
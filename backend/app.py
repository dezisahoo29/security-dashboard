from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import numpy as np
import os
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import IsolationForest

app = Flask(__name__)
CORS(app)

# Dataset path
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

        features = np.array(data['features']).reshape(1, -1)
        features_scaled = scaler.transform(features)

        prediction = model.predict(features_scaled)
        anomaly_score = model.decision_function(features_scaled)[0]

        # Convert anomaly score to 0-100 threat score
        threat_score = int(max(0, min(100, (1 - anomaly_score) * 50)))

        if threat_score >= 70:
            risk_level = "High Risk"
        elif threat_score >= 40:
            risk_level = "Medium Risk"
        else:
            risk_level = "Low Risk"

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
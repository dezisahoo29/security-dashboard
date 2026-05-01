from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import IsolationForest

app = Flask(__name__)
CORS(app)  # ✅ Fix CORS issue

# Load dataset
df = pd.read_csv(r'D:\Security-dashboard\data\data.csv')

# Convert label
df['Label'] = df['Label'].apply(lambda x: 0 if x == 'BENIGN' else 1)

# Features
X = df.drop('Label', axis=1)

# Scale
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Train model
model = IsolationForest(contamination=0.3, random_state=42)
model.fit(X_scaled)

# Home route
@app.route('/')
def home():
    return "✅ Security Dashboard API is Running"

# Prediction route
@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.json

        input_data = np.array([[
            data['Feature1'],
            data['Feature2'],
            data['Feature3'],
            data['Feature4']
        ]])

        input_scaled = scaler.transform(input_data)

        pred = model.predict(input_scaled)
        pred = 1 if pred[0] == -1 else 0

        threat = "High Risk" if pred == 1 else "Low Risk"

        return jsonify({
            "prediction": pred,
            "threat_level": threat
        })

    except Exception as e:
        return jsonify({"error": str(e)})

# Run server
if __name__ == '__main__':
    app.run(debug=True)
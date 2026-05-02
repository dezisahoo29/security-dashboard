from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import IsolationForest

app = Flask(__name__)
CORS(app)

df = pd.read_csv('data/data.csv')

X = df.select_dtypes(include=[np.number])

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

model = IsolationForest(contamination=0.1, random_state=42)
model.fit(X_scaled)

@app.route('/')
def home():
    return "Security Dashboard API is Running"

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()

    features = np.array(data['features']).reshape(1, -1)
    features_scaled = scaler.transform(features)

    prediction = model.predict(features_scaled)

    result = "Threat Detected" if prediction[0] == -1 else "Normal Activity"

    return jsonify({"result": result})

if __name__ == '__main__':
    app.run(debug=True)
from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import IsolationForest

app = Flask(__name__)
CORS(app)

# ✅ LOAD DATA (FIXED FOR RENDER)
df = pd.read_csv('data/data.csv')

# Use only numeric columns
X = df.select_dtypes(include=[np.number])

# Scale data
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Train model
model = IsolationForest(contamination=0.1, random_state=42)
model.fit(X_scaled)

# Home route
@app.route('/')
def home():
    return "✅ Security Dashboard API is Running"

# Prediction route
@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()

        # Expect list like [100,200,300,400]
        features = np.array(data['features']).reshape(1, -1)

        # Scale input
        features_scaled = scaler.transform(features)

        # Predict
        prediction = model.predict(features_scaled)

        if prediction[0] == -1:
            result = "⚠️ Threat Detected"
        else:
            result = "✅ Normal Activity"

        return jsonify({'result': result})

    except Exception as e:
        return jsonify({'error': str(e)})

# Run app
if __name__ == '__main__':
    app.run(debug=True)
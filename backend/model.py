import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import IsolationForest
from sklearn.metrics import classification_report

# Load dataset
df = pd.read_csv(r'D:\Security-dashboard\data\data.csv')

# Convert label to numeric
df['Label'] = df['Label'].apply(lambda x: 0 if x == 'BENIGN' else 1)

# Separate features and label
X = df.drop('Label', axis=1)

# Normalize data
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Train model
model = IsolationForest(contamination=0.3, random_state=42)
model.fit(X_scaled)

# Predict anomalies
preds = model.predict(X_scaled)

# Convert predictions (-1 = attack → 1)
preds = np.where(preds == -1, 1, 0)

# Evaluation
print("\n📊 Model Evaluation:\n")
print(classification_report(df['Label'], preds))

# Threat scoring
def threat_score(pred):
    return "High Risk" if pred == 1 else "Low Risk"

df['Prediction'] = preds
df['Threat_Level'] = df['Prediction'].apply(threat_score)

print("\n🚨 Sample Results:\n")
print(df[['Label', 'Prediction', 'Threat_Level']])
import os
import sys
import joblib
import pandas as pd

# Base directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MODEL_PATH = os.path.join(BASE_DIR, "models", "risk_model.pkl")

# Load trained model
model = joblib.load(MODEL_PATH)

# Severity label mapping (must match training order)
severity_labels = ["Critical", "High", "Low", "Medium"]

# Validate input
if len(sys.argv) != 3:
    print("Usage: python3 scripts/predict_risk.py <port> <cvss_score>")
    sys.exit(1)

port = int(sys.argv[1])
cvss = float(sys.argv[2])

# Prepare input
input_data = pd.DataFrame([[port, cvss]], columns=["port", "cvss_score"])

# Predict
prediction = model.predict(input_data)[0]
predicted_severity = severity_labels[prediction]

print("\n==== RISK PREDICTION RESULT ====")
print(f"Port: {port}")
print(f"CVSS Score: {cvss}")
print(f"Predicted Severity: {predicted_severity}")
print("================================\n")

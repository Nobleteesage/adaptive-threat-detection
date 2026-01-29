import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score
import joblib

# Base directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATA_PATH = os.path.join(BASE_DIR, "data", "processed_vulnerabilities.csv")
MODEL_PATH = os.path.join(BASE_DIR, "models", "risk_model.pkl")

# Ensure model directory exists
os.makedirs(os.path.join(BASE_DIR, "models"), exist_ok=True)

# Load data
df = pd.read_csv(DATA_PATH)

# Encode severity labels
label_encoder = LabelEncoder()
df["severity_encoded"] = label_encoder.fit_transform(df["severity"])

# Features & target
X = df[["port", "cvss_score"]]
y = df["severity_encoded"]

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42
)

# Train model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

# Save model
joblib.dump(model, MODEL_PATH)

print("\n==== MODEL TRAINING COMPLETE ====")
print(f"Model Accuracy: {accuracy * 100:.2f}%")
print("Model saved to models/risk_model.pkl")
print("================================\n")


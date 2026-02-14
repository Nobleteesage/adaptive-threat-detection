import json
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

# Load scan results
with open('automated_scan_results.json', 'r') as f:
    data = json.load(f)

# Prepare training data (simulated historical scans)
# In real scenario, you'd have multiple scan results
risk_mapping = {'High': 3, 'Medium': 2, 'Low': 1, 'Informational': 0}

# Create features from alerts
features = []
labels = []

for alert in data['alerts']:
    feature = [
        risk_mapping.get(alert['risk'], 0),
        len(alert['url']),
        1 if 'sql' in alert['alert'].lower() else 0,
        1 if 'xss' in alert['alert'].lower() else 0,
        1 if 'csrf' in alert['alert'].lower() else 0,
    ]
    features.append(feature)
    labels.append(risk_mapping.get(alert['risk'], 0))

# Add some synthetic training data for demonstration
synthetic_features = np.random.randint(0, 4, size=(50, 5))
synthetic_labels = np.random.randint(0, 4, size=50)

all_features = np.vstack([features, synthetic_features])
all_labels = np.concatenate([labels, synthetic_labels])

# Train model
X_train, X_test, y_train, y_test = train_test_split(
    all_features, all_labels, test_size=0.2, random_state=42
)

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

accuracy = model.score(X_test, y_test)

print("=" * 60)
print("    🤖 MACHINE LEARNING THREAT PREDICTOR")
print("=" * 60)
print(f"\n✓ Model trained with {len(all_features)} samples")
print(f"✓ Model accuracy: {accuracy*100:.2f}%")
print(f"\n📊 Predicting threat levels for current scan...")

# Predict on current alerts
predictions = model.predict(features)
threat_levels = ['Informational', 'Low', 'Medium', 'High']

print("\n🔮 PREDICTIONS:")
print("-" * 60)
for i, (alert, pred) in enumerate(zip(data['alerts'][:5], predictions[:5]), 1):
    print(f"\n{i}. {alert['alert'][:50]}...")
    print(f"   Actual Risk: {alert['risk']}")
    print(f"   Predicted: {threat_levels[int(pred)]}")

print("\n" + "=" * 60)

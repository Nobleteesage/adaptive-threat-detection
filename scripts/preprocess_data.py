import os
import pandas as pd

# Project base directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

INPUT_PATH = os.path.join(BASE_DIR, "data", "vulnerabilities.csv")
OUTPUT_PATH = os.path.join(BASE_DIR, "data", "processed_vulnerabilities.csv")

# Load CSV
df = pd.read_csv(INPUT_PATH)

# Convert CVSS to float
df["cvss_score"] = df["cvss_score"].astype(float)

# Severity classification
def classify_severity(score):
    if score >= 9.0:
        return "Critical"
    elif score >= 7.0:
        return "High"
    elif score >= 4.0:
        return "Medium"
    else:
        return "Low"

df["severity"] = df["cvss_score"].apply(classify_severity)

# Save processed data
df.to_csv(OUTPUT_PATH, index=False)

print("[+] Preprocessing complete. Saved to data/processed_vulnerabilities.csv")

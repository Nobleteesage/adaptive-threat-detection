import os
import pandas as pd

# Base directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATA_PATH = os.path.join(BASE_DIR, "data", "processed_vulnerabilities.csv")

# Load data
df = pd.read_csv(DATA_PATH)

# Summary statistics
total_vulns = len(df)
avg_cvss = df["cvss_score"].mean()

severity_counts = df["severity"].value_counts()

# Risk scoring (simple weighted logic)
risk_weights = {
    "Critical": 4,
    "High": 3,
    "Medium": 2,
    "Low": 1
}

df["risk_weight"] = df["severity"].map(risk_weights)
overall_risk_score = df["risk_weight"].sum()

# Most risky service
top_service = df.groupby("service")["risk_weight"].sum().idxmax()

# Output
print("\n==== RISK ANALYSIS SUMMARY ====\n")
print(f"Total Vulnerabilities: {total_vulns}")
print(f"Average CVSS Score: {avg_cvss:.2f}")
print("\nSeverity Breakdown:")
print(severity_counts)

print(f"\nOverall Risk Score: {overall_risk_score}")
print(f"Most Risky Service: {top_service}")

print("\n===============================\n")

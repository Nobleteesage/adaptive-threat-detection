import json

# ---- 1. Load ZAP JSON report ----
with open('zap_report.json', 'r') as f:
    data = json.load(f)

# ---- 2. Prepare summary ----
vulns = data.get('site', [])
summary = []

for site in vulns:
    alerts = site.get('alerts', [])
    for alert in alerts:
        risk = alert.get('risk', 'Unknown')
        if risk in ['High', 'Medium', 'Critical']:  # focus on significant risks
            summary.append({
                'url': alert.get('url', 'N/A'),
                'alert': alert.get('alert', 'N/A'),
                'risk': risk,
                'description': alert.get('description', 'N/A')
            })

# ---- 3. Save summary to a file ----
with open('zap_summary.json', 'w') as f:
    json.dump(summary, f, indent=4)

print(f"Summary saved to zap_summary.json with {len(summary)} important vulnerabilities.")

from zapv2 import ZAPv2
import time
import json

# Configuration
ZAP_API_KEY = 'MySecretKey123'
ZAP_ADDRESS = '127.0.0.1'
ZAP_PORT = 8090
TARGET = 'http://example.com'

# Initialize ZAP
zap = ZAPv2(apikey=ZAP_API_KEY, proxies={
    'http': 'http://127.0.0.1:8090',
    'https': 'http://127.0.0.1:8090'
})
    'http': f'http://{ZAP_ADDRESS}:{ZAP_PORT}',
    'https': f'http://{ZAP_ADDRESS}:{ZAP_PORT}'
})

print("[*] Checking ZAP connection...")
try:
    print("ZAP Version:", zap.core.version)
except Exception as e:
    print(f"Error connecting to ZAP: {e}")
    print("Make sure ZAP is running!")
    exit(1)

print(f"\n[*] Starting Spider Scan on {TARGET}...")
scan_id = zap.spider.scan(TARGET)

while int(zap.spider.status(scan_id)) < 100:
    progress = zap.spider.status(scan_id)
    print(f"Spider progress: {progress}%")
    time.sleep(2)

print("[✓] Spider Scan Completed\n")

print("[*] Starting Active Scan...")
ascan_id = zap.ascan.scan(TARGET)

while int(zap.ascan.status(ascan_id)) < 100:
    progress = zap.ascan.status(ascan_id)
    print(f"Active Scan progress: {progress}%")
    time.sleep(5)

print("[✓] Active Scan Completed\n")

print("[*] Fetching Alerts...")
alerts = zap.core.alerts(baseurl=TARGET)

risk_score = 0
risk_levels = {
    'High': 5,
    'Medium': 3,
    'Low': 1,
    'Informational': 0
}

for alert in alerts:
    risk_score += risk_levels.get(alert['risk'], 0)

print(f"\n[!] Total Alerts Found: {len(alerts)}")
print(f"[!] Total Risk Score: {risk_score}\n")

# Save results as JSON
output = {
    "target": TARGET,
    "total_alerts": len(alerts),
    "risk_score": risk_score,
    "alerts": alerts
}

with open("automated_scan_results.json", "w") as f:
    json.dump(output, f, indent=4)

print("[✓] Results saved to automated_scan_results.json")

# Save results as XML (for DefectDojo)
print("[*] Generating XML report for DefectDojo...")
xml_report = zap.core.xmlreport()

with open("data/zap_scan_report.xml", "w") as f:
    f.write(xml_report)

print("[✓] XML report saved to data/zap_scan_report.xml")

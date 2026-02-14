from zapv2 import ZAPv2
import time

# ---- 1. Target URL ----
target = 'http://localhost:8081'  # Replace with your target URL

# ---- 2. Connect to ZAP daemon ----
zap = ZAPv2(apikey='', proxies={'http':'http://127.0.0.1:8080', 'https':'http://127.0.0.1:8080'})

# ---- 3. Spider (crawl the site) ----
print(f"Spidering target: {target}")
scanid = zap.spider.scan(target)

while int(zap.spider.status(scanid)) < 100:
    print(f"Spider progress: {zap.spider.status(scanid)}%")
    time.sleep(2)
print("Spider completed")

# ---- 4. Active Scan (vulnerability scan) ----
print("Starting Active Scan...")
scanid = zap.ascan.scan(target)

while int(zap.ascan.status(scanid)) < 100:
    print(f"Active scan progress: {zap.ascan.status(scanid)}%")
    time.sleep(5)
print("Active Scan completed")

# ---- 5. Export JSON report ----
report = zap.core.jsonreport()
with open('zap_report.json', 'w') as f:
    f.write(report)
print("Report saved as zap_report.json")

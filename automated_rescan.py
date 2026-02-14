import json
import time
import os
from datetime import datetime
from zapv2 import ZAPv2

# Configuration
ZAP_API_KEY = 'MySecretKey123'
TARGET = 'http://example.com'
SCAN_INTERVAL = 3600  # 1 hour (change to 86400 for daily, 604800 for weekly)

# Compare scan results
def compare_scans(old_file, new_file):
    """Compare two scan results and identify new/fixed vulnerabilities"""
    
    if not os.path.exists(old_file):
        print("[!] No previous scan found. This is the first scan.")
        return None
    
    with open(old_file, 'r') as f:
        old_data = json.load(f)
    
    with open(new_file, 'r') as f:
        new_data = json.load(f)
    
    old_alerts = {alert['alert']: alert for alert in old_data['alerts']}
    new_alerts = {alert['alert']: alert for alert in new_data['alerts']}
    
    # Find new vulnerabilities
    new_vulns = set(new_alerts.keys()) - set(old_alerts.keys())
    
    # Find fixed vulnerabilities
    fixed_vulns = set(old_alerts.keys()) - set(new_alerts.keys())
    
    # Find changed severity
    changed = []
    for alert_name in set(old_alerts.keys()) & set(new_alerts.keys()):
        if old_alerts[alert_name]['risk'] != new_alerts[alert_name]['risk']:
            changed.append({
                'name': alert_name,
                'old_risk': old_alerts[alert_name]['risk'],
                'new_risk': new_alerts[alert_name]['risk']
            })
    
    print("\n" + "=" * 60)
    print("    📊 SCAN COMPARISON REPORT")
    print("=" * 60)
    
    print(f"\n📅 Previous Scan: {old_data.get('scan_date', 'Unknown')}")
    print(f"📅 Current Scan: {new_data.get('scan_date', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))}")
    
    print(f"\n📈 Previous Risk Score: {old_data['risk_score']}")
    print(f"📈 Current Risk Score: {new_data['risk_score']}")
    
    if new_data['risk_score'] > old_data['risk_score']:
        print("   ⚠️  RISK INCREASED")
    elif new_data['risk_score'] < old_data['risk_score']:
        print("   ✅ RISK DECREASED")
    else:
        print("   ➡️  NO CHANGE")
    
    if new_vulns:
        print(f"\n🆕 NEW VULNERABILITIES ({len(new_vulns)}):")
        for vuln in new_vulns:
            print(f"   • {vuln} (Risk: {new_alerts[vuln]['risk']})")
    else:
        print("\n✅ No new vulnerabilities detected")
    
    if fixed_vulns:
        print(f"\n✅ FIXED VULNERABILITIES ({len(fixed_vulns)}):")
        for vuln in fixed_vulns:
            print(f"   • {vuln} (Was: {old_alerts[vuln]['risk']})")
    else:
        print("\n⚠️  No vulnerabilities fixed")
    
    if changed:
        print(f"\n🔄 CHANGED SEVERITY ({len(changed)}):")
        for item in changed:
            print(f"   • {item['name']}: {item['old_risk']} → {item['new_risk']}")
    
    print("\n" + "=" * 60)

def run_automated_scan():
    """Run a single scan and save results"""
    
    print(f"\n[*] Starting automated scan at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Check if ZAP is running
    try:
        zap = ZAPv2(apikey=ZAP_API_KEY)
        print(f"[*] Connected to ZAP version: {zap.core.version}")
    except Exception as e:
        print(f"[!] Error: Cannot connect to ZAP. Make sure it's running!")
        print(f"[!] Start ZAP with: zaproxy -daemon -host 127.0.0.1 -port 8080 -config api.key=MySecretKey123")
        return None
    
    # Spider scan
    print(f"[*] Starting Spider Scan on {TARGET}...")
    scan_id = zap.spider.scan(TARGET)
    while int(zap.spider.status(scan_id)) < 100:
        print(f"    Spider progress: {zap.spider.status(scan_id)}%")
        time.sleep(2)
    print("[✓] Spider Scan Completed")
    
    # Active scan
    print("[*] Starting Active Scan...")
    ascan_id = zap.ascan.scan(TARGET)
    while int(zap.ascan.status(ascan_id)) < 100:
        print(f"    Active Scan progress: {zap.ascan.status(ascan_id)}%")
        time.sleep(5)
    print("[✓] Active Scan Completed")
    
    # Fetch alerts
    alerts = zap.core.alerts(baseurl=TARGET)
    
    # Calculate risk
    risk_levels = {'High': 5, 'Medium': 3, 'Low': 1, 'Informational': 0}
    risk_score = sum(risk_levels.get(alert['risk'], 0) for alert in alerts)
    
    # Save results
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"data/scan_{timestamp}.json"
    
    output = {
        "target": TARGET,
        "scan_date": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        "total_alerts": len(alerts),
        "risk_score": risk_score,
        "alerts": alerts
    }
    
    with open(filename, 'w') as f:
        json.dump(output, f, indent=4)
    
    print(f"[✓] Results saved to {filename}")
    print(f"[!] Total Alerts: {len(alerts)}, Risk Score: {risk_score}")
    
    return filename

def continuous_scanning():
    """Run scans at regular intervals"""
    
    print("=" * 60)
    print("    🔄 AUTOMATED CONTINUOUS SCANNING")
    print("=" * 60)
    print(f"\nTarget: {TARGET}")
    print(f"Scan Interval: {SCAN_INTERVAL} seconds ({SCAN_INTERVAL//3600}h)")
    print("\nPress Ctrl+C to stop\n")
    
    previous_scan = None
    scan_count = 0
    
    try:
        while True:
            scan_count += 1
            print(f"\n{'='*60}")
            print(f"    SCAN #{scan_count}")
            print(f"{'='*60}")
            
            current_scan = run_automated_scan()
            
            if current_scan and previous_scan:
                compare_scans(previous_scan, current_scan)
            
            previous_scan = current_scan
            
            print(f"\n[*] Next scan in {SCAN_INTERVAL//60} minutes...")
            print(f"[*] Waiting until {datetime.fromtimestamp(time.time() + SCAN_INTERVAL).strftime('%Y-%m-%d %H:%M:%S')}")
            
            time.sleep(SCAN_INTERVAL)
            
    except KeyboardInterrupt:
        print("\n\n[!] Stopping automated scanning...")
        print(f"[✓] Completed {scan_count} scans")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == 'once':
        # Run single scan
        run_automated_scan()
    elif len(sys.argv) > 1 and sys.argv[1] == 'compare':
        # Compare two specific scans
        if len(sys.argv) == 4:
            compare_scans(sys.argv[2], sys.argv[3])
        else:
            print("Usage: python3 automated_rescan.py compare <old_file> <new_file>")
    else:
        # Run continuous scanning
        continuous_scanning()

#!/usr/bin/env python3
"""
Batch Vulnerability Scanner - Scans multiple legal test sites
"""

import time
from zapv2 import ZAPv2
import json
from datetime import datetime
import os

# Configuration
ZAP_API_KEY = 'MySecretKey123'
ZAP_ADDRESS = '127.0.0.1'
ZAP_PORT = 8090

# LEGAL TEST TARGETS - Safe to scan, no permission needed
TARGETS = [
    "http://testphp.vulnweb.com/",
    "http://testhtml5.vulnweb.com/",
    "http://testasp.vulnweb.com/",
    "http://testaspnet.vulnweb.com/",
    "http://testfire.net/",
    "http://zero.webappsecurity.com/",
    "http://demo.testfire.net/",
    "http://www.webscantest.com/",
    "http://crackme.cenzic.com/",
    "http://www.vulnweb.com/",
    "http://rest.vulnweb.com/",
    "http://php.testsparker.com/",
    "http://aspnet.testsparker.com/",
    "http://public-firing-range.appspot.com/",
    "http://www.hackthissite.org/",
    "http://testaspnet.vulnweb.com/",
    "http://testphp.acunetix.com/",
    "http://demo.xtreamlab.net/",
    "http://hack.me/",
    "http://www.dvwa.co.uk/",
    "http://scanme.nmap.org/",
    "http://demo.owasp-juice.shop/",
    "http://www.itsecgames.com/",
]

def scan_target(zap, target, scan_number):
    """Scan a single target and return results"""
    
    print(f"\n{'='*60}")
    print(f"SCAN #{scan_number}: {target}")
    print(f"Started: {datetime.now().strftime('%H:%M:%S')}")
    print(f"{'='*60}")
    
    start_time = time.time()
    
    try:
        # Spider scan
        print(f"[*] Starting Spider Scan...")
        scan_id = zap.spider.scan(target)
        
        while int(zap.spider.status(scan_id)) < 100:
            progress = zap.spider.status(scan_id)
            print(f"    Spider progress: {progress}%", end='\r')
            time.sleep(2)
        
        print(f"\n[✓] Spider Scan Completed")
        
        # Active scan
        print(f"[*] Starting Active Scan...")
        ascan_id = zap.ascan.scan(target)
        
        while int(zap.ascan.status(ascan_id)) < 100:
            progress = zap.ascan.status(ascan_id)
            print(f"    Active Scan progress: {progress}%", end='\r')
            time.sleep(5)
        
        print(f"\n[✓] Active Scan Completed")
        
        # Get alerts
        alerts = zap.core.alerts(baseurl=target)
        
        # Calculate metrics
        scan_time = time.time() - start_time
        risk_levels = {'High': 5, 'Medium': 3, 'Low': 1, 'Informational': 0}
        risk_score = sum(risk_levels.get(alert['risk'], 0) for alert in alerts)
        
        # Compile results
        results = {
            "scan_number": scan_number,
            "target": target,
            "timestamp": datetime.now().isoformat(),
            "scan_time_seconds": round(scan_time, 2),
            "total_alerts": len(alerts),
            "risk_score": risk_score,
            "alerts": alerts,
            "severity_breakdown": {
                "High": sum(1 for a in alerts if a['risk'] == 'High'),
                "Medium": sum(1 for a in alerts if a['risk'] == 'Medium'),
                "Low": sum(1 for a in alerts if a['risk'] == 'Low'),
                "Informational": sum(1 for a in alerts if a['risk'] == 'Informational')
            }
        }
        
        # Save individual scan
        safe_name = target.replace('http://', '').replace('https://', '').replace('/', '_').replace('.', '_')
        filename = f"evaluation_data/scan_{scan_number:03d}_{safe_name}.json"
        
        with open(filename, 'w') as f:
            json.dump(results, f, indent=4)
        
        print(f"\n[✓] Results saved: {filename}")
        print(f"    Vulnerabilities found: {len(alerts)}")
        print(f"    Risk score: {risk_score}")
        print(f"    Scan time: {scan_time/60:.1f} minutes")
        
        return results
        
    except Exception as e:
        print(f"\n[!] Error scanning {target}: {e}")
        return None

def main():
    """Main batch scanning function"""
    
    print("="*60)
    print("    BATCH VULNERABILITY SCANNER")
    print("="*60)
    print(f"\nTargets to scan: {len(TARGETS)}")
    print(f"Estimated time: {len(TARGETS) * 5} minutes (~{len(TARGETS)*5/60:.1f} hours)")
    print(f"\n⚠️  WARNING: This will take a while. You can stop anytime with Ctrl+C")
    print(f"⚠️  Progress is saved after each scan.")
    print("\nPress ENTER to start...")
    input()
    
    # Check ZAP connection
    try:
        zap = ZAPv2(apikey=ZAP_API_KEY, proxies={
    'http': 'http://127.0.0.1:8090',
    'https': 'http://127.0.0.1:8090'
})
        version = zap.core.version
        print(f"\n[✓] Connected to ZAP version: {version}\n")
    except Exception as e:
        print(f"\n[!] Error: Cannot connect to ZAP!")
        print(f"[!] Make sure ZAP is running on port {ZAP_PORT}")
        print(f"\nStart ZAP with:")
        print(f"zaproxy -daemon -host {ZAP_ADDRESS} -port {ZAP_PORT} -config api.key={ZAP_API_KEY} -config api.addrs.addr.name=.* -config api.addrs.addr.regex=true")
        return
    
    # Create output directory
    os.makedirs("evaluation_data", exist_ok=True)
    
    # Scan all targets
    all_results = []
    successful_scans = 0
    failed_scans = []
    
    for i, target in enumerate(TARGETS, 1):
        result = scan_target(zap, target, i)
        
        if result:
            all_results.append(result)
            successful_scans += 1
        else:
            failed_scans.append(target)
        
        # Be respectful - wait between scans
        if i < len(TARGETS):
            print(f"\n[*] Waiting 15 seconds before next scan...")
            time.sleep(15)
    
    # Save combined results
    summary = {
        "scan_date": datetime.now().isoformat(),
        "total_targets": len(TARGETS),
        "successful_scans": successful_scans,
        "failed_scans": len(failed_scans),
        "failed_targets": failed_scans,
        "total_vulnerabilities": sum(r['total_alerts'] for r in all_results),
        "average_risk_score": sum(r['risk_score'] for r in all_results) / len(all_results) if all_results else 0,
        "scans": all_results
    }
    
    with open("evaluation_data/batch_scan_summary.json", 'w') as f:
        json.dump(summary, f, indent=4)
    
    # Print summary
    print("\n" + "="*60)
    print("    BATCH SCAN COMPLETE")
    print("="*60)
    print(f"\n✅ Successful scans: {successful_scans}/{len(TARGETS)}")
    print(f"❌ Failed scans: {len(failed_scans)}")
    print(f"🔍 Total vulnerabilities: {summary['total_vulnerabilities']}")
    print(f"📊 Average risk score: {summary['average_risk_score']:.2f}")
    
    if failed_scans:
        print(f"\n⚠️  Failed targets:")
        for target in failed_scans:
            print(f"   - {target}")
    
    print(f"\n[✓] Summary saved: evaluation_data/batch_scan_summary.json")
    print("\n🎉 Data collection complete! Ready for ML training.")

if __name__ == "__main__":
    main()

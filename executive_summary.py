import json
from datetime import datetime

with open('data/automated_scan_results.json', 'r') as f:
    data = json.load(f)

print("=" * 60)
print("    📊 EXECUTIVE SECURITY SUMMARY")
print("=" * 60)
print(f"\nReport Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
print(f"Target: {data['target']}")

# Overall status
if data['risk_score'] > 20:
    status = "🔴 CRITICAL"
elif data['risk_score'] > 10:
    status = "🟡 NEEDS ATTENTION"
else:
    status = "🟢 ACCEPTABLE"

print(f"\nSecurity Posture: {status}")
print(f"Total Vulnerabilities: {data['total_alerts']}")
print(f"Risk Score: {data['risk_score']}/30")

# Risk breakdown
risks = {}
for alert in data['alerts']:
    risk = alert['risk']
    risks[risk] = risks.get(risk, 0) + 1

print("\n📈 Risk Distribution:")
for risk, count in sorted(risks.items(), 
                          key=lambda x: {'High': 3, 'Medium': 2, 'Low': 1, 'Informational': 0}.get(x[0], 0), 
                          reverse=True):
    print(f"  {risk}: {count}")

print("\n💡 Recommendations:")
if data['risk_score'] > 15:
    print("  1. Immediate security review required")
    print("  2. Prioritize high-risk vulnerabilities")
    print("  3. Schedule remediation sprint")
else:
    print("  1. Address medium-risk items in next sprint")
    print("  2. Continue regular security scanning")
    print("  3. Monitor for new vulnerabilities")

print("\n" + "=" * 60)

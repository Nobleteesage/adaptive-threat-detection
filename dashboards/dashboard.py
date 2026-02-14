import json
from collections import Counter

# Load results
with open('automated_scan_results.json', 'r') as f:
    data = json.load(f)

print("=" * 60)
print("     ADAPTIVE THREAT DETECTION - SCAN REPORT")
print("=" * 60)
print(f"\n🎯 Target: {data['target']}")
print(f"📊 Total Alerts: {data['total_alerts']}")
print(f"⚠️  Risk Score: {data['risk_score']}")
print("\n" + "=" * 60)

# Count by risk level
risks = [alert['risk'] for alert in data['alerts']]
risk_counts = Counter(risks)

print("\n📈 VULNERABILITY BREAKDOWN:")
print("-" * 60)
for risk, count in sorted(risk_counts.items(), 
                          key=lambda x: {'High': 4, 'Medium': 3, 'Low': 2, 'Informational': 1}.get(x[0], 0), 
                          reverse=True):
    bar = "█" * count
    print(f"{risk:15} | {bar} ({count})")

print("\n" + "=" * 60)
print("\n🔍 TOP VULNERABILITIES FOUND:")
print("-" * 60)

for i, alert in enumerate(data['alerts'][:5], 1):  # Show top 5
    print(f"\n{i}. {alert['alert']}")
    print(f"   Risk: {alert['risk']}")
    print(f"   URL: {alert['url'][:80]}...")
    print(f"   Description: {alert['description'][:100]}...")

print("\n" + "=" * 60)
print("\n💾 Full report saved in: automated_scan_results.json")
print("=" * 60)

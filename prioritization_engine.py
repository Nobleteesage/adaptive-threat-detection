import json

with open('data/automated_scan_results.json', 'r') as f:
    data = json.load(f)

# Priority scoring
def calculate_priority(alert):
    risk_scores = {'High': 10, 'Medium': 5, 'Low': 2, 'Informational': 1}
    base_score = risk_scores.get(alert['risk'], 0)
    
    # Increase priority for easily exploitable issues
    if 'injection' in alert['alert'].lower():
        base_score += 5
    if 'xss' in alert['alert'].lower():
        base_score += 4
    
    return base_score

# Sort by priority
prioritized = sorted(data['alerts'], key=calculate_priority, reverse=True)

print("=" * 60)
print("    📋 PRIORITIZED REMEDIATION PLAN")
print("=" * 60)

print("\n🔴 CRITICAL - Fix Immediately:")
for alert in prioritized[:3]:
    print(f"  • {alert['alert']} (Risk: {alert['risk']})")

print("\n🟡 HIGH - Fix This Week:")
for alert in prioritized[3:6]:
    print(f"  • {alert['alert']} (Risk: {alert['risk']})")

print("\n🟢 MEDIUM - Fix This Month:")
for alert in prioritized[6:]:
    print(f"  • {alert['alert']} (Risk: {alert['risk']})")

print("\n" + "=" * 60)

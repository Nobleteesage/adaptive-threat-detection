import json

# Load scan results
with open('data/automated_scan_results.json', 'r') as f:
    data = json.load(f)

# Remediation suggestions
remediation_map = {
    'Missing Anti-clickjacking Header': {
        'fix': 'Add X-Frame-Options header',
        'code': 'X-Frame-Options: SAMEORIGIN',
        'priority': 'Medium',
        'effort': 'Low'
    },
    'Content Security Policy (CSP) Header Not Set': {
        'fix': 'Implement Content Security Policy',
        'code': "Content-Security-Policy: default-src 'self'",
        'priority': 'Medium',
        'effort': 'Medium'
    },
    'X-Content-Type-Options Header Missing': {
        'fix': 'Add X-Content-Type-Options header',
        'code': 'X-Content-Type-Options: nosniff',
        'priority': 'Low',
        'effort': 'Low'
    }
}

print("=" * 60)
print("    🔧 REMEDIATION RECOMMENDATIONS")
print("=" * 60)

for i, alert in enumerate(data['alerts'], 1):
    vuln_name = alert['alert']
    
    print(f"\n{i}. {vuln_name}")
    print(f"   Current Risk: {alert['risk']}")
    
    if vuln_name in remediation_map:
        remedy = remediation_map[vuln_name]
        print(f"   ✅ Fix: {remedy['fix']}")
        print(f"   📝 Implementation: {remedy['code']}")
        print(f"   ⚡ Priority: {remedy['priority']}")
        print(f"   🛠️  Effort: {remedy['effort']}")
    else:
        print(f"   ℹ️  Refer to: {alert.get('solution', 'Manual review required')}")

print("\n" + "=" * 60)

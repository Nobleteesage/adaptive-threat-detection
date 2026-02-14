import json
from datetime import datetime
from collections import Counter

# Load scan results
with open('data/automated_scan_results.json', 'r') as f:
    data = json.load(f)

# Compliance framework mappings
OWASP_TOP_10_2021 = {
    'A01:2021-Broken Access Control': ['Missing Anti-clickjacking Header', 'CSRF'],
    'A02:2021-Cryptographic Failures': ['Weak SSL', 'Insecure Cookie'],
    'A03:2021-Injection': ['SQL Injection', 'XSS', 'Cross Site Scripting'],
    'A04:2021-Insecure Design': ['Security Misconfiguration'],
    'A05:2021-Security Misconfiguration': ['Content Security Policy', 'X-Content-Type-Options'],
    'A06:2021-Vulnerable Components': ['Outdated Libraries'],
    'A07:2021-Authentication Failures': ['Weak Authentication'],
    'A08:2021-Software Integrity Failures': ['Integrity Check'],
    'A09:2021-Logging Failures': ['Insufficient Logging'],
    'A10:2021-SSRF': ['Server Side Request Forgery']
}

PCI_DSS_REQUIREMENTS = {
    'Req 6.5.1 - Injection Flaws': ['SQL Injection', 'XSS'],
    'Req 6.5.7 - XSS': ['Cross Site Scripting'],
    'Req 6.5.9 - Improper Access Control': ['Missing Anti-clickjacking Header'],
    'Req 6.5.10 - Broken Authentication': ['Weak Authentication'],
    'Req 6.6 - Web Application Firewall': ['Security Misconfiguration']
}

def generate_compliance_report():
    
    print("=" * 80)
    print(" " * 25 + "🔒 COMPLIANCE REPORT")
    print("=" * 80)
    
    print(f"\n📅 Report Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🎯 Target: {data['target']}")
    print(f"📊 Total Findings: {data['total_alerts']}")
    
    # OWASP Top 10 Compliance
    print("\n" + "=" * 80)
    print("🛡️  OWASP TOP 10:2021 COMPLIANCE")
    print("=" * 80)
    
    owasp_findings = {}
    for alert in data['alerts']:
        for category, keywords in OWASP_TOP_10_2021.items():
            if any(keyword.lower() in alert['alert'].lower() for keyword in keywords):
                if category not in owasp_findings:
                    owasp_findings[category] = []
                owasp_findings[category].append(alert)
    
    for i, (category, _) in enumerate(OWASP_TOP_10_2021.items(), 1):
        findings = owasp_findings.get(category, [])
        status = "❌ FAIL" if findings else "✅ PASS"
        print(f"\n{category}")
        print(f"   Status: {status}")
        if findings:
            print(f"   Findings: {len(findings)}")
            for finding in findings[:2]:  # Show top 2
                print(f"      • {finding['alert']} (Risk: {finding['risk']})")
    
    # PCI-DSS Compliance
    print("\n" + "=" * 80)
    print("💳 PCI-DSS COMPLIANCE")
    print("=" * 80)
    
    pci_findings = {}
    for alert in data['alerts']:
        for requirement, keywords in PCI_DSS_REQUIREMENTS.items():
            if any(keyword.lower() in alert['alert'].lower() for keyword in keywords):
                if requirement not in pci_findings:
                    pci_findings[requirement] = []
                pci_findings[requirement].append(alert)
    
    for requirement, _ in PCI_DSS_REQUIREMENTS.items():
        findings = pci_findings.get(requirement, [])
        status = "❌ NON-COMPLIANT" if findings else "✅ COMPLIANT"
        print(f"\n{requirement}")
        print(f"   Status: {status}")
        if findings:
            print(f"   Violations: {len(findings)}")
    
    # Overall Compliance Score
    print("\n" + "=" * 80)
    print("📊 COMPLIANCE SCORECARD")
    print("=" * 80)
    
    total_owasp = len(OWASP_TOP_10_2021)
    passed_owasp = total_owasp - len(owasp_findings)
    owasp_score = (passed_owasp / total_owasp) * 100
    
    total_pci = len(PCI_DSS_REQUIREMENTS)
    passed_pci = total_pci - len(pci_findings)
    pci_score = (passed_pci / total_pci) * 100
    
    print(f"\nOWASP Top 10 Compliance: {owasp_score:.1f}%")
    print(f"   Passed: {passed_owasp}/{total_owasp} categories")
    
    print(f"\nPCI-DSS Compliance: {pci_score:.1f}%")
    print(f"   Compliant: {passed_pci}/{total_pci} requirements")
    
    # Overall verdict
    print("\n" + "=" * 80)
    print("⚖️  COMPLIANCE VERDICT")
    print("=" * 80)
    
    if owasp_score >= 90 and pci_score >= 90:
        verdict = "✅ COMPLIANT"
        action = "Continue monitoring"
    elif owasp_score >= 70 and pci_score >= 70:
        verdict = "⚠️  PARTIALLY COMPLIANT"
        action = "Remediate findings within 30 days"
    else:
        verdict = "❌ NON-COMPLIANT"
        action = "Immediate remediation required"
    
    print(f"\nOverall Status: {verdict}")
    print(f"Recommended Action: {action}")
    
    # Remediation Timeline
    print("\n" + "=" * 80)
    print("📅 COMPLIANCE REMEDIATION TIMELINE")
    print("=" * 80)
    
    high_count = sum(1 for alert in data['alerts'] if alert['risk'] == 'High')
    medium_count = sum(1 for alert in data['alerts'] if alert['risk'] == 'Medium')
    
    print("\n🎯 CRITICAL (0-7 days):")
    print(f"   • Fix {high_count} HIGH severity vulnerabilities")
    print("   • Implement emergency security controls")
    
    print("\n🎯 IMPORTANT (8-30 days):")
    print(f"   • Fix {medium_count} MEDIUM severity vulnerabilities")
    print("   • Update security policies")
    
    print("\n🎯 CONTINUOUS (Ongoing):")
    print("   • Monthly compliance scans")
    print("   • Quarterly security assessments")
    print("   • Annual penetration testing")
    
    print("\n" + "=" * 80)
    print("Report Generated by: Adaptive Threat Detection System v2.0")
    print("=" * 80 + "\n")

if __name__ == "__main__":
    generate_compliance_report()

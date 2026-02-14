import json
from datetime import datetime

with open('automated_scan_results.json', 'r') as f:
    data = json.load(f)

html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Security Scan Report</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }}
        .container {{ background: white; padding: 30px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
        h1 {{ color: #d32f2f; }}
        .stats {{ display: flex; gap: 20px; margin: 20px 0; }}
        .stat-box {{ background: #e3f2fd; padding: 20px; border-radius: 5px; flex: 1; }}
        .high {{ color: #d32f2f; font-weight: bold; }}
        .medium {{ color: #f57c00; font-weight: bold; }}
        .low {{ color: #fbc02d; font-weight: bold; }}
        table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
        th, td {{ padding: 12px; text-align: left; border-bottom: 1px solid #ddd; }}
        th {{ background: #1976d2; color: white; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🛡️ Security Scan Report</h1>
        <p><strong>Target:</strong> {data['target']}</p>
        <p><strong>Scan Date:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        
        <div class="stats">
            <div class="stat-box">
                <h3>{data['total_alerts']}</h3>
                <p>Total Alerts</p>
            </div>
            <div class="stat-box">
                <h3>{data['risk_score']}</h3>
                <p>Risk Score</p>
            </div>
        </div>
        
        <h2>Vulnerabilities Found</h2>
        <table>
            <tr>
                <th>Risk</th>
                <th>Alert</th>
                <th>URL</th>
            </tr>
"""

for alert in data['alerts']:
    risk_class = alert['risk'].lower()
    html += f"""
            <tr>
                <td class="{risk_class}">{alert['risk']}</td>
                <td>{alert['alert']}</td>
                <td>{alert['url'][:50]}...</td>
            </tr>
"""

html += """
        </table>
    </div>
</body>
</html>
"""

with open('scan_report.html', 'w') as f:
    f.write(html)

print("[✓] HTML report generated: scan_report.html")
print("[*] Open it in browser: firefox scan_report.html")

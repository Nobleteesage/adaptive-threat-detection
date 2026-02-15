import json
from xml.etree.ElementTree import Element, SubElement, tostring
from xml.dom import minidom

# Load JSON
with open('data/automated_scan_results.json', 'r') as f:
    data = json.load(f)

# Create XML structure (ZAP format)
root = Element('OWASPZAPReport')
root.set('version', '2.14.0')
root.set('generated', '2026-02-14')

# Add site
site = SubElement(root, 'site')
site.set('name', data['target'])
site.set('host', data['target'])
site.set('port', '80')
site.set('ssl', 'false')

# Add alerts
for alert_data in data['alerts']:
    alert = SubElement(site, 'alertitem')
    
    SubElement(alert, 'pluginid').text = str(alert_data.get('pluginId', '0'))
    SubElement(alert, 'alert').text = alert_data.get('alert', 'Unknown')
    SubElement(alert, 'name').text = alert_data.get('alert', 'Unknown')
    
    # Map risk levels
    risk_map = {'High': '3', 'Medium': '2', 'Low': '1', 'Informational': '0'}
    SubElement(alert, 'riskcode').text = risk_map.get(alert_data.get('risk', 'Low'), '1')
    SubElement(alert, 'confidence').text = str(alert_data.get('confidence', 'Medium'))
    SubElement(alert, 'riskdesc').text = f"{alert_data.get('risk', 'Low')} ({alert_data.get('confidence', 'Medium')})"
    SubElement(alert, 'desc').text = str(alert_data.get('description', 'No description'))
    
    # Instances
    instances = SubElement(alert, 'instances')
    instance = SubElement(instances, 'instance')
    SubElement(instance, 'uri').text = str(alert_data.get('url', data['target']))
    SubElement(instance, 'method').text = 'GET'
    
    SubElement(alert, 'solution').text = str(alert_data.get('solution', 'Review and fix'))
    SubElement(alert, 'reference').text = str(alert_data.get('reference', ''))
    SubElement(alert, 'cweid').text = str(alert_data.get('cweid', '0'))
    SubElement(alert, 'wascid').text = str(alert_data.get('wascid', '0'))

# Pretty print
xml_str = minidom.parseString(tostring(root)).toprettyxml(indent="  ")

# Save
with open('data/zap_scan_report.xml', 'w') as f:
    f.write(xml_str)

print("[✓] Converted JSON to XML format")
print("[✓] Saved to data/zap_scan_report.xml")
print(f"[✓] Converted {len(data['alerts'])} alerts")

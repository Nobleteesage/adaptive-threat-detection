import os
import xml.etree.ElementTree as ET
import pandas as pd

# Get absolute project base directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Define input and output paths
XML_PATH = os.path.join(BASE_DIR, "data", "nmap_scan.xml")
OUTPUT_PATH = os.path.join(BASE_DIR, "data", "vulnerabilities.csv")

# Parse Nmap XML
tree = ET.parse(XML_PATH)
root = tree.getroot()

rows = []

for host in root.findall("host"):
    address = host.find("address").get("addr")

    for port in host.findall(".//port"):
        port_id = port.get("portid")
        service = port.find("service")
        service_name = service.get("name") if service is not None else "unknown"

        for script in port.findall("script"):
            if script.get("id") == "vulners":
                lines = script.get("output").splitlines()
                for line in lines:
                    parts = line.strip().split()
                    if len(parts) >= 2:
                        rows.append({
                            "host": address,
                            "port": port_id,
                            "service": service_name,
                            "cve": parts[0],
                            "cvss_score": parts[1]
                        })

# Convert to DataFrame
df = pd.DataFrame(rows)

# Ensure data directory exists
os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)

# Save CSV
df.to_csv(OUTPUT_PATH, index=False)

print("[+] Vulnerabilities successfully saved to data/vulnerabilities.csv")


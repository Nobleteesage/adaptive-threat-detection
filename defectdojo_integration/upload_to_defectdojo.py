import requests
import json
import os
from datetime import datetime

# DefectDojo Configuration
DEFECTDOJO_URL = "http://localhost:8080"
API_KEY = "e2f9ca71d26815523a8e35e64a9f2b9ec341d505"  # Replace with your actual API key
HEADERS = {
    "Authorization": f"Token {API_KEY}",
    "Content-Type": "application/json"
}

# Product and Engagement settings
PRODUCT_NAME = "Adaptive Threat Detection"
ENGAGEMENT_NAME = f"Automated Scan - {datetime.now().strftime('%Y-%m-%d')}"

def create_product():
    """Create a product in DefectDojo"""
    url = f"{DEFECTDOJO_URL}/api/v2/products/"
    
    # Check if product already exists
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        products = response.json()['results']
        for product in products:
            if product['name'] == PRODUCT_NAME:
                print(f"[✓] Product '{PRODUCT_NAME}' already exists (ID: {product['id']})")
                return product['id']
    
    # Create new product
    data = {
        "name": PRODUCT_NAME,
        "description": "Automated cybersecurity threat detection and vulnerability scanning",
        "prod_type": 1  # Research and Development
    }
    
    response = requests.post(url, headers=HEADERS, json=data)
    if response.status_code == 201:
        product_id = response.json()['id']
        print(f"[✓] Created product '{PRODUCT_NAME}' (ID: {product_id})")
        return product_id
    else:
        print(f"[!] Error creating product: {response.text}")
        return None

def create_engagement(product_id):
    """Create an engagement in DefectDojo"""
    url = f"{DEFECTDOJO_URL}/api/v2/engagements/"
    
    data = {
        "name": ENGAGEMENT_NAME,
        "description": "Automated vulnerability scan using OWASP ZAP and Nmap",
        "product": product_id,
        "target_start": datetime.now().strftime('%Y-%m-%d'),
        "target_end": datetime.now().strftime('%Y-%m-%d'),
        "engagement_type": "CI/CD",
        "status": "In Progress"
    }
    
    response = requests.post(url, headers=HEADERS, json=data)
    if response.status_code == 201:
        engagement_id = response.json()['id']
        print(f"[✓] Created engagement '{ENGAGEMENT_NAME}' (ID: {engagement_id})")
        return engagement_id
    else:
        print(f"[!] Error creating engagement: {response.text}")
        return None

def upload_zap_scan(engagement_id, scan_file):
    """Upload ZAP scan results to DefectDojo"""
    url = f"{DEFECTDOJO_URL}/api/v2/import-scan/"
    
    # Read XML scan file
    if not os.path.exists(scan_file):
        print(f"[!] Scan file not found: {scan_file}")
        return False
    
    with open(scan_file, 'rb') as f:
        scan_content = f.read()
    
    # Upload XML file
    files = {
        'file': ('zap_report.xml', scan_content, 'application/xml')
    }
    
    data = {
        'engagement': engagement_id,
        'scan_type': 'ZAP Scan',
        'active': 'true',
        'verified': 'true',
        'minimum_severity': 'Info',
        'scan_date': datetime.now().strftime('%Y-%m-%d'),
        'close_old_findings': 'false'
    }
    
    # Remove Content-Type from headers for multipart upload
    upload_headers = {"Authorization": f"Token {API_KEY}"}
    
    response = requests.post(url, headers=upload_headers, data=data, files=files)
    
    if response.status_code == 201:
        print(f"[✓] Uploaded ZAP scan results successfully!")
        test_id = response.json().get('test')
        print(f"    Test ID: {test_id}")
        return True
    else:
        print(f"[!] Error uploading scan: {response.status_code}")
        print(f"    Response: {response.text}")
        return False

    # Read scan file
    if not os.path.exists(scan_file):
        print(f"[!] Scan file not found: {scan_file}")
        return False
    
    with open(scan_file, 'r') as f:
        scan_data = json.load(f)
    
    # DefectDojo expects ZAP format
    files = {
        'file': (os.path.basename(scan_file), json.dumps(scan_data), 'application/json')
    }
    
    data = {
        'engagement': engagement_id,
        'scan_type': 'ZAP Scan',
        'active': 'true',
        'verified': 'true',
        'minimum_severity': 'Info',
        'scan_date': datetime.now().strftime('%Y-%m-%d'),
        'close_old_findings': 'false'
    }
    
    # Remove Content-Type from headers for multipart upload
    upload_headers = {"Authorization": f"Token {API_KEY}"}
    
    response = requests.post(url, headers=upload_headers, data=data, files=files)
    
    if response.status_code == 201:
        print(f"[✓] Uploaded ZAP scan results successfully!")
        test_id = response.json().get('test')
        print(f"    Test ID: {test_id}")
        return True
    else:
        print(f"[!] Error uploading scan: {response.status_code}")
        print(f"    Response: {response.text}")
        return False

def get_findings(engagement_id):
    """Retrieve findings from DefectDojo"""
    url = f"{DEFECTDOJO_URL}/api/v2/findings/?engagement={engagement_id}"
    
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        findings = response.json()['results']
        print(f"\n[✓] Retrieved {len(findings)} findings from DefectDojo")
        
        # Display summary
        severity_count = {}
        for finding in findings:
            severity = finding['severity']
            severity_count[severity] = severity_count.get(severity, 0) + 1
        
        print("\n📊 Findings by Severity:")
        for severity in ['Critical', 'High', 'Medium', 'Low', 'Info']:
            count = severity_count.get(severity, 0)
            if count > 0:
                print(f"   {severity}: {count}")
        
        return findings
    else:
        print(f"[!] Error retrieving findings: {response.text}")
        return []

def main():
    print("=" * 60)
    print("    🔄 DEFECTDOJO INTEGRATION")
    print("=" * 60)
    
    # Step 1: Create product
    print("\n[*] Step 1: Creating product...")
    product_id = create_product()
    if not product_id:
        return
    
    # Step 2: Create engagement
    print("\n[*] Step 2: Creating engagement...")
    engagement_id = create_engagement(product_id)
    if not engagement_id:
        return
    
    # Step 3: Upload ZAP scan
    print("\n[*] Step 3: Uploading ZAP scan results...")
    scan_file = "data/zap_scan_report.xml"
    success = upload_zap_scan(engagement_id, scan_file)
    
    if success:
        # Step 4: Retrieve findings
        print("\n[*] Step 4: Retrieving findings...")
        findings = get_findings(engagement_id)
        
        print("\n" + "=" * 60)
        print("✅ INTEGRATION COMPLETE!")
        print("=" * 60)
        print(f"\n🌐 View in DefectDojo: {DEFECTDOJO_URL}")
        print(f"📊 Product ID: {product_id}")
        print(f"📋 Engagement ID: {engagement_id}")
        print(f"🔍 Total Findings: {len(findings)}")
    else:
        print("\n[!] Upload failed. Check your API key and scan file.")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Generate evaluation spreadsheet from scan data
"""

import json
import glob
import pandas as pd
from datetime import datetime

def create_spreadsheet():
    """Create comprehensive evaluation spreadsheet"""
    
    # Load all scans
    scan_files = sorted(glob.glob("evaluation_data/scan_*.json"))
    scan_files = [f for f in scan_files if 'summary' not in f]
    
    if not scan_files:
        print("[!] No scan files found. Run batch_scanner.py first!")
        return
    
    rows = []
    
    for file in scan_files:
        with open(file, 'r') as f:
            data = json.load(f)
            
            # Extract metrics
            row = {
                'Scan #': data['scan_number'],
                'Target': data['target'],
                'Date': data['timestamp'][:10],
                'Total Vulns': data['total_alerts'],
                'High': data['severity_breakdown']['High'],
                'Medium': data['severity_breakdown']['Medium'],
                'Low': data['severity_breakdown']['Low'],
                'Info': data['severity_breakdown']['Informational'],
                'Risk Score': data['risk_score'],
                'Scan Time (min)': f"{data['scan_time_seconds']/60:.1f}",
            }
            
            rows.append(row)
    
    # Create DataFrame
    df = pd.DataFrame(rows)
    
    # Add summary statistics
    summary = {
        'Scan #': 'SUMMARY',
        'Target': f'{len(df)} scans',
        'Date': datetime.now().strftime('%Y-%m-%d'),
        'Total Vulns': df['Total Vulns'].sum(),
        'High': df['High'].sum(),
        'Medium': df['Medium'].sum(),
        'Low': df['Low'].sum(),
        'Info': df['Info'].sum(),
        'Risk Score': f"{df['Risk Score'].mean():.1f} avg",
        'Scan Time (min)': f"{pd.to_numeric(df['Scan Time (min)']).mean():.1f} avg",
    }
    
    df = pd.concat([df, pd.DataFrame([summary])], ignore_index=True)
    
    # Save to CSV
    df.to_csv('evaluation_data/evaluation_summary.csv', index=False)
    print(f"[✓] Spreadsheet saved: evaluation_data/evaluation_summary.csv")
    
    # Print preview
    print("\n" + "="*100)
    print("EVALUATION SUMMARY")
    print("="*100)
    print(df.to_string(index=False))
    print("="*100)

if __name__ == "__main__":
    create_spreadsheet()

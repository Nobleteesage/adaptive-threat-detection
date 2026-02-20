#!/usr/bin/env python3
"""
Generate all figures needed for the arXiv paper
"""

import json
import glob
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
import os

# Set style
plt.style.use('seaborn-v0_8-paper')
sns.set_palette("husl")

def load_all_data():
    """Load all scan and ML data"""
    
    # Load scans
    scan_files = glob.glob("evaluation_data/scan_*.json")
    scan_files = [f for f in scan_files if 'summary' not in f]
    
    scans = []
    all_alerts = []
    
    for file in scan_files:
        with open(file, 'r') as f:
            data = json.load(f)
            scans.append(data)
            all_alerts.extend(data.get('alerts', []))
    
    # Load ML metrics
    with open('evaluation_data/ml_metrics.json', 'r') as f:
        ml_metrics = json.load(f)
    
    return scans, all_alerts, ml_metrics

def figure1_scan_summary(scans):
    """Figure 1: Scan Summary Statistics"""
    
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    
    # Extract data
    total_vulns = [s['total_alerts'] for s in scans]
    risk_scores = [s['risk_score'] for s in scans]
    scan_times = [s['scan_time_seconds']/60 for s in scans]
    
    # Plot 1: Vulnerabilities per scan
    axes[0, 0].bar(range(1, len(scans)+1), total_vulns, color='steelblue')
    axes[0, 0].set_xlabel('Scan Number')
    axes[0, 0].set_ylabel('Total Vulnerabilities')
    axes[0, 0].set_title('Vulnerabilities Detected Per Target')
    axes[0, 0].axhline(y=np.mean(total_vulns), color='r', linestyle='--', 
                       label=f'Mean: {np.mean(total_vulns):.1f}')
    axes[0, 0].legend()
    axes[0, 0].grid(True, alpha=0.3)
    
    # Plot 2: Risk scores
    axes[0, 1].bar(range(1, len(scans)+1), risk_scores, color='coral')
    axes[0, 1].set_xlabel('Scan Number')
    axes[0, 1].set_ylabel('Risk Score')
    axes[0, 1].set_title('Risk Score Per Target')
    axes[0, 1].axhline(y=np.mean(risk_scores), color='r', linestyle='--',
                       label=f'Mean: {np.mean(risk_scores):.1f}')
    axes[0, 1].legend()
    axes[0, 1].grid(True, alpha=0.3)
    
    # Plot 3: Scan time distribution
    axes[1, 0].hist(scan_times, bins=15, color='lightgreen', edgecolor='black')
    axes[1, 0].set_xlabel('Scan Time (minutes)')
    axes[1, 0].set_ylabel('Frequency')
    axes[1, 0].set_title('Scan Time Distribution')
    axes[1, 0].axvline(x=np.mean(scan_times), color='r', linestyle='--',
                       label=f'Mean: {np.mean(scan_times):.1f} min')
    axes[1, 0].legend()
    axes[1, 0].grid(True, alpha=0.3)
    
    # Plot 4: Severity breakdown (stacked bar)
    severities = ['High', 'Medium', 'Low', 'Informational']
    severity_data = {sev: [] for sev in severities}
    
    for scan in scans:
        for sev in severities:
            severity_data[sev].append(scan['severity_breakdown'][sev])
    
    x = range(1, len(scans)+1)
    bottom = np.zeros(len(scans))
    
    colors = {'High': 'red', 'Medium': 'orange', 'Low': 'yellow', 'Informational': 'lightblue'}
    
    for sev in severities:
        axes[1, 1].bar(x, severity_data[sev], bottom=bottom, 
                       label=sev, color=colors[sev], edgecolor='black')
        bottom += severity_data[sev]
    
    axes[1, 1].set_xlabel('Scan Number')
    axes[1, 1].set_ylabel('Count')
    axes[1, 1].set_title('Severity Breakdown Per Scan')
    axes[1, 1].legend()
    axes[1, 1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('figures/figure1_scan_summary.png', dpi=300, bbox_inches='tight')
    print("[✓] Figure 1 saved: figures/figure1_scan_summary.png")
    plt.close()

def figure2_severity_distribution(all_alerts):
    """Figure 2: Overall Severity Distribution"""
    
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    
    # Count severities
    severities = [a['risk'] for a in all_alerts]
    sev_counts = Counter(severities)
    
    # Plot 1: Pie chart
    colors = {'High': '#ff6b6b', 'Medium': '#ffa500', 
              'Low': '#ffd93d', 'Informational': '#95e1d3'}
    
    labels = list(sev_counts.keys())
    sizes = list(sev_counts.values())
    pie_colors = [colors.get(label, 'gray') for label in labels]
    
    axes[0].pie(sizes, labels=labels, colors=pie_colors, autopct='%1.1f%%',
                startangle=90, textprops={'fontsize': 12, 'weight': 'bold'})
    axes[0].set_title('Vulnerability Severity Distribution', fontsize=14, weight='bold')
    
    # Plot 2: Bar chart
    axes[1].bar(sev_counts.keys(), sev_counts.values(), 
                color=[colors.get(k, 'gray') for k in sev_counts.keys()],
                edgecolor='black', linewidth=1.5)
    axes[1].set_ylabel('Count', fontsize=12)
    axes[1].set_title('Vulnerability Count by Severity', fontsize=14, weight='bold')
    axes[1].grid(True, alpha=0.3, axis='y')
    
    # Add count labels on bars
    for i, (k, v) in enumerate(sev_counts.items()):
        axes[1].text(i, v + max(sev_counts.values())*0.02, str(v), 
                     ha='center', fontsize=12, weight='bold')
    
    plt.tight_layout()
    plt.savefig('figures/figure2_severity_distribution.png', dpi=300, bbox_inches='tight')
    print("[✓] Figure 2 saved: figures/figure2_severity_distribution.png")
    plt.close()

def figure3_top_vulnerabilities(all_alerts):
    """Figure 3: Top 10 Most Common Vulnerabilities"""
    
    # Count vulnerability types
    vuln_types = [a['alert'] for a in all_alerts]
    vuln_counts = Counter(vuln_types).most_common(10)
    
    fig, ax = plt.subplots(figsize=(12, 6))
    
    names = [v[0][:50] + '...' if len(v[0]) > 50 else v[0] for v in vuln_counts]
    counts = [v[1] for v in vuln_counts]
    
    bars = ax.barh(range(len(names)), counts, color='teal', edgecolor='black')
    ax.set_yticks(range(len(names)))
    ax.set_yticklabels(names, fontsize=10)
    ax.set_xlabel('Occurrences', fontsize=12)
    ax.set_title('Top 10 Most Common Vulnerabilities', fontsize=14, weight='bold')
    ax.grid(True, alpha=0.3, axis='x')
    
    # Add count labels
    for i, (bar, count) in enumerate(zip(bars, counts)):
        ax.text(count + max(counts)*0.02, i, str(count), 
                va='center', fontsize=10, weight='bold')
    
    plt.tight_layout()
    plt.savefig('figures/figure3_top_vulnerabilities.png', dpi=300, bbox_inches='tight')
    print("[✓] Figure 3 saved: figures/figure3_top_vulnerabilities.png")
    plt.close()

def figure4_ml_performance(ml_metrics):
    """Figure 4: ML Model Performance Metrics"""
    
    # Note: confusion matrix already created by improved_ml_model.py
    # This creates additional performance visualizations
    
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    
    # Plot 1: Accuracy bar
    accuracy = ml_metrics['accuracy'] * 100
    
    axes[0].bar(['Model Accuracy'], [accuracy], color='green', width=0.5, edgecolor='black')
    axes[0].set_ylim([0, 100])
    axes[0].set_ylabel('Accuracy (%)', fontsize=12)
    axes[0].set_title('ML Model Classification Accuracy', fontsize=14, weight='bold')
    axes[0].axhline(y=70, color='orange', linestyle='--', linewidth=2, label='Acceptable (70%)')
    axes[0].axhline(y=80, color='green', linestyle='--', linewidth=2, label='Excellent (80%)')
    axes[0].text(0, accuracy + 3, f'{accuracy:.1f}%', ha='center', fontsize=16, weight='bold')
    axes[0].legend()
    axes[0].grid(True, alpha=0.3, axis='y')
    
    # Plot 2: Class distribution
    class_dist = ml_metrics['class_distribution']
    
    axes[1].bar(class_dist.keys(), class_dist.values(), 
                color=['lightblue', 'yellow', 'orange', 'red'],
                edgecolor='black', linewidth=1.5)
    axes[1].set_ylabel('Sample Count', fontsize=12)
    axes[1].set_title('Training Data Class Distribution', fontsize=14, weight='bold')
    axes[1].grid(True, alpha=0.3, axis='y')
    
    # Add count labels
    for i, (k, v) in enumerate(class_dist.items()):
        axes[1].text(i, v + max(class_dist.values())*0.02, str(v),
                     ha='center', fontsize=12, weight='bold')
    
    plt.tight_layout()
    plt.savefig('figures/figure4_ml_performance.png', dpi=300, bbox_inches='tight')
    print("[✓] Figure 4 saved: figures/figure4_ml_performance.png")
    plt.close()

def create_summary_table(scans, ml_metrics):
    """Create summary statistics table (for LaTeX)"""
    
    total_scans = len(scans)
    total_vulns = sum(s['total_alerts'] for s in scans)
    avg_vulns = total_vulns / total_scans
    avg_risk = np.mean([s['risk_score'] for s in scans])
    avg_time = np.mean([s['scan_time_seconds']/60 for s in scans])
    ml_accuracy = ml_metrics['accuracy'] * 100
    
    # Create LaTeX table
    table = f"""
\\begin{{table}}[h]
\\centering
\\caption{{Experimental Results Summary}}
\\begin{{tabular}}{{|l|r|}}
\\hline
\\textbf{{Metric}} & \\textbf{{Value}} \\\\
\\hline
Total Targets Scanned & {total_scans} \\\\
Total Vulnerabilities Found & {total_vulns} \\\\
Average Vulnerabilities per Target & {avg_vulns:.1f} \\\\
Average Risk Score & {avg_risk:.2f} \\\\
Average Scan Time (minutes) & {avg_time:.1f} \\\\
ML Classification Accuracy & {ml_accuracy:.1f}\\% \\\\
Training Samples & {ml_metrics['training_samples']} \\\\
Test Samples & {ml_metrics['test_samples']} \\\\
\\hline
\\end{{tabular}}
\\label{{tab:results}}
\\end{{table}}
"""
    
    with open('arxiv_paper/results_table.tex', 'w') as f:
        f.write(table)
    
    print("[✓] LaTeX table saved: arxiv_paper/results_table.tex")
    
    # Also save as text summary
    summary = f"""
EXPERIMENTAL RESULTS SUMMARY
{'='*50}

Total Targets Scanned:           {total_scans}
Total Vulnerabilities Found:     {total_vulns}
Average Vulnerabilities/Target:  {avg_vulns:.1f}
Average Risk Score:              {avg_risk:.2f}
Average Scan Time:               {avg_time:.1f} minutes
ML Classification Accuracy:      {ml_accuracy:.1f}%
Training Samples:                {ml_metrics['training_samples']}
Test Samples:                    {ml_metrics['test_samples']}

{'='*50}
"""
    
    with open('evaluation_data/summary_statistics.txt', 'w') as f:
        f.write(summary)
    
    print("[✓] Text summary saved: evaluation_data/summary_statistics.txt")
    print("\n" + summary)

def main():
    """Generate all figures"""
    
    print("\n" + "="*60)
    print("    GENERATING PAPER FIGURES")
    print("="*60)
    
    # Create directories
    os.makedirs('figures', exist_ok=True)
    os.makedirs('arxiv_paper', exist_ok=True)
    
    # Load data
    print("\n[*] Loading data...")
    scans, all_alerts, ml_metrics = load_all_data()
    
    print(f"[✓] Loaded {len(scans)} scans with {len(all_alerts)} vulnerabilities")
    
    # Generate figures
    print("\n[*] Creating figures...\n")
    
    figure1_scan_summary(scans)
    figure2_severity_distribution(all_alerts)
    figure3_top_vulnerabilities(all_alerts)
    figure4_ml_performance(ml_metrics)
    
    # Create tables
    print("\n[*] Creating summary tables...\n")
    create_summary_table(scans, ml_metrics)
    
    print("\n" + "="*60)
    print("✅ ALL FIGURES CREATED!")
    print("="*60)
    print("\nGenerated files:")
    print("  - figures/figure1_scan_summary.png")
    print("  - figures/figure2_severity_distribution.png")
    print("  - figures/figure3_top_vulnerabilities.png")
    print("  - figures/figure4_ml_performance.png")
    print("  - figures/confusion_matrix.png (from ML training)")
    print("  - figures/feature_importance.png (from ML training)")
    print("  - arxiv_paper/results_table.tex")
    print("  - evaluation_data/summary_statistics.txt")
    print("\nReady for paper writing!")
    print("="*60)

if __name__ == "__main__":
    main()

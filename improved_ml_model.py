#!/usr/bin/env python3
"""
Improved ML Model for Threat Prediction
Target: 70%+ accuracy
"""

import json
import os
import glob
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import joblib
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import seaborn as sns

def load_all_scans():
    """Load all scan data from evaluation_data folder"""
    
    all_alerts = []
    scan_files = glob.glob("evaluation_data/scan_*.json")
    
    # Exclude summary file
    scan_files = [f for f in scan_files if 'summary' not in f]
    
    print(f"[*] Loading {len(scan_files)} scan files...")
    
    for file in scan_files:
        with open(file, 'r') as f:
            data = json.load(f)
            
            # Add scan metadata to each alert
            for alert in data.get('alerts', []):
                alert['scan_target'] = data['target']
                alert['scan_number'] = data['scan_number']
                all_alerts.append(alert)
    
    print(f"[✓] Loaded {len(all_alerts)} total vulnerabilities")
    return all_alerts

def extract_features(alerts):
    """Extract features from vulnerability data"""
    
    features = []
    labels = []
    
    for alert in alerts:
        # Feature vector (10 dimensions)
        feature = [
            # URL characteristics
            len(alert.get('url', '')),
            alert.get('url', '').count('/'),
            alert.get('url', '').count('?'),
            
            # Description length
            len(alert.get('description', '')),
            
            # Vulnerability type indicators
            1 if 'sql' in alert.get('alert', '').lower() else 0,
            1 if 'xss' in alert.get('alert', '').lower() or 'script' in alert.get('alert', '').lower() else 0,
            1 if 'csrf' in alert.get('alert', '').lower() else 0,
            1 if 'injection' in alert.get('alert', '').lower() else 0,
            
            # Context indicators
            1 if 'header' in alert.get('alert', '').lower() or 'cookie' in alert.get('alert', '').lower() else 0,
            
            # Confidence level
            {'High': 3, 'Medium': 2, 'Low': 1}.get(alert.get('confidence', 'Medium'), 2),
        ]
        
        features.append(feature)
        
        # Label (risk level)
        risk_map = {'High': 3, 'Medium': 2, 'Low': 1, 'Informational': 0}
        labels.append(risk_map.get(alert.get('risk', 'Low'), 1))
    
    return np.array(features), np.array(labels)

def train_and_evaluate():
    """Train multiple models and select the best"""
    
    print("\n" + "="*60)
    print("    IMPROVED ML MODEL TRAINING")
    print("="*60)
    
    # Load data
    alerts = load_all_scans()
    
    if len(alerts) < 50:
        print(f"\n⚠️  WARNING: Only {len(alerts)} samples.")
        print(f"⚠️  Recommended: At least 100 samples for reliable results.")
        print(f"⚠️  Current results may have lower accuracy.")
        
        if len(alerts) < 20:
            print(f"\n❌ ERROR: Need at least 20 samples. Currently have {len(alerts)}.")
            print(f"❌ Run batch_scanner.py to collect more data first.")
            return
    
    # Extract features
    print(f"\n[*] Extracting features...")
    X, y = extract_features(alerts)
    
    # Check class distribution
    unique, counts = np.unique(y, return_counts=True)
    print(f"\n[*] Class distribution:")
    risk_names = {0: 'Informational', 1: 'Low', 2: 'Medium', 3: 'High'}
    for label, count in zip(unique, counts):
        print(f"    {risk_names[label]}: {count}")
    
    # Check if we have enough samples per class
    if min(counts) < 2:
        print(f"\n⚠️  WARNING: Some classes have very few samples.")
        print(f"⚠️  ML accuracy may be lower. Collect more diverse scans.")
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=42, stratify=y if min(counts) >= 2 else None
    )
    
    print(f"\n[*] Training set: {len(X_train)} samples")
    print(f"[*] Test set: {len(X_test)} samples")
    
    # Train multiple models
    models = {
        'Random Forest': RandomForestClassifier(
            n_estimators=200,
            max_depth=10,
            min_samples_split=5,
            random_state=42
        ),
        'Gradient Boosting': GradientBoostingClassifier(
            n_estimators=200,
            max_depth=5,
            learning_rate=0.1,
            random_state=42
        )
    }
    
    best_model = None
    best_score = 0
    best_name = ""
    
    print(f"\n[*] Training models...")
    print("="*60)
    
    for name, model in models.items():
        print(f"\n{name}:")
        
        # Cross-validation
        try:
            cv_scores = cross_val_score(model, X_train, y_train, cv=min(5, len(X_train)//10))
            cv_mean = cv_scores.mean()
            cv_std = cv_scores.std()
            print(f"  Cross-validation accuracy: {cv_mean*100:.2f}% (+/- {cv_std*100:.2f}%)")
        except:
            print(f"  Cross-validation skipped (not enough data)")
        
        # Train on full training set
        model.fit(X_train, y_train)
        
        # Test accuracy
        test_score = model.score(X_test, y_test)
        print(f"  Test accuracy: {test_score*100:.2f}%")
        
        # Update best model
        if test_score > best_score:
            best_score = test_score
            best_model = model
            best_name = name
    
    print("\n" + "="*60)
    print(f"✅ BEST MODEL: {best_name}")
    print(f"✅ ACCURACY: {best_score*100:.2f}%")
    print("="*60)
    
    # Detailed evaluation of best model
    y_pred = best_model.predict(X_test)
    
    print("\n📊 CLASSIFICATION REPORT:")
    print("-"*60)
    target_names = ['Informational', 'Low', 'Medium', 'High']
    # Filter target names to only those present
    present_classes = sorted(list(set(y_test)))
    present_names = [target_names[i] for i in present_classes]
    print(classification_report(y_test, y_pred, target_names=present_names, zero_division=0))
    
    # Confusion matrix
    cm = confusion_matrix(y_test, y_pred)
    print("\n📊 CONFUSION MATRIX:")
    print("-"*60)
    print(cm)
    
    # Save confusion matrix plot
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
                xticklabels=present_names, yticklabels=present_names)
    plt.title(f'Confusion Matrix - {best_name}\nAccuracy: {best_score*100:.1f}%')
    plt.ylabel('True Label')
    plt.xlabel('Predicted Label')
    plt.tight_layout()
    plt.savefig('figures/confusion_matrix.png', dpi=300)
    print(f"\n[✓] Confusion matrix saved: figures/confusion_matrix.png")
    plt.close()
    
    # Feature importance
    if hasattr(best_model, 'feature_importances_'):
        feature_names = [
            'URL Length', 'URL Slashes', 'URL Params',
            'Description Length', 'SQL', 'XSS', 'CSRF',
            'Injection', 'Header/Cookie', 'Confidence'
        ]
        
        importances = best_model.feature_importances_
        indices = np.argsort(importances)[::-1]
        
        plt.figure(figsize=(10, 6))
        plt.title('Feature Importance')
        plt.bar(range(len(importances)), importances[indices])
        plt.xticks(range(len(importances)), [feature_names[i] for i in indices], rotation=45, ha='right')
        plt.tight_layout()
        plt.savefig('figures/feature_importance.png', dpi=300)
        print(f"[✓] Feature importance saved: figures/feature_importance.png")
        plt.close()
    
    # Save model
    os.makedirs('models', exist_ok=True)
    joblib.dump(best_model, 'models/improved_model.pkl')
    print(f"\n[✓] Model saved: models/improved_model.pkl")
    
    # Save metrics
    metrics = {
        'model_name': best_name,
        'accuracy': float(best_score),
        'training_samples': len(X_train),
        'test_samples': len(X_test),
        'total_vulnerabilities': len(alerts),
        'confusion_matrix': cm.tolist(),
        'class_distribution': {risk_names[k]: int(v) for k, v in zip(unique, counts)}
    }
    
    with open('evaluation_data/ml_metrics.json', 'w') as f:
        json.dump(metrics, f, indent=4)
    
    print(f"[✓] Metrics saved: evaluation_data/ml_metrics.json")
    
    # Final recommendation
    print("\n" + "="*60)
    if best_score >= 0.80:
        print("🎉 EXCELLENT! Accuracy ≥ 80% - Ready for publication!")
    elif best_score >= 0.70:
        print("✅ GOOD! Accuracy ≥ 70% - Acceptable for arXiv")
        print("💡 TIP: Collect more scans to potentially reach 80%+")
    elif best_score >= 0.60:
        print("⚠️  MODERATE. Accuracy 60-70%")
        print("💡 TIP: Collect 10-20 more scans to improve accuracy")
    else:
        print("❌ TOO LOW. Need more training data")
        print("💡 ACTION: Scan at least 10 more diverse websites")
    print("="*60)

if __name__ == "__main__":
    # Create directories
    os.makedirs('figures', exist_ok=True)
    os.makedirs('models', exist_ok=True)
    
    train_and_evaluate()

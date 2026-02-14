# Adaptive Cybersecurity Threat Detection System

## 📌 Overview

This project implements an **adaptive cybersecurity threat detection system** designed to identify, analyze, and predict security risks from network vulnerability scans. Unlike static scanners, the system integrates **machine learning** to dynamically assess and predict threat severity, making it suitable for modern, evolving threat landscapes.

The project was developed and tested on **Kali Linux** and is intended for **academic research, cybersecurity portfolios, and practical demonstrations**.

---

## 🎯 Objectives

* Perform live vulnerability scanning using Nmap
* Extract and structure vulnerability intelligence (CVEs & CVSS)
* Preprocess and classify vulnerabilities by severity
* Quantify overall system risk
* Train a machine-learning model for adaptive risk prediction
* Predict severity of new threats in real time

---

## 🧠 System Architecture

1. **Scanning Layer** – Nmap vulnerability scan
2. **Parsing Layer** – XML parsing and data extraction
3. **Preprocessing Layer** – Data cleaning and severity labeling
4. **Risk Analysis Layer** – Risk scoring and prioritization
5. **Machine Learning Layer** – Model training and evaluation
6. **Prediction Layer** – Real-time severity prediction
7. **Alerting Layer** – Live scan alerting (Critical/High)

---

## 🛠 Tools & Technologies

* **Operating System:** Kali Linux
* **Scanner:** Nmap
* **Programming Language:** Python 3
* **Libraries:** pandas, scikit-learn, joblib
* **Machine Learning Model:** Random Forest Classifier

---

## 📂 Project Structure

```
adaptive-threat-detection/
│
├── data/
│   ├── nmap_scan.xml
│   ├── vulnerabilities.csv
│   └── processed_vulnerabilities.csv
│
├── scripts/
│   ├── parse_nmap.py
│   ├── preprocess_data.py
│   ├── risk_analysis.py
│   ├── train_model.py
│   ├── predict_risk.py
│   └── live_scan_alert.py
│
├── models/
│   └── risk_model.pkl
│
└── README.md
```

---

## ⚙️ Methodology

### 1. Vulnerability Scanning

Nmap is used with version and vulnerability detection scripts:

```bash
nmap -sV --script vuln localhost -oX data/nmap_scan.xml
```

### 2. Parsing & Extraction

The XML output is parsed to extract:

* Host IP
* Open ports
* Services
* CVE identifiers
* CVSS scores

### 3. Data Preprocessing

CVSS scores are normalized and classified into severity levels:

* Low (0.0 – 3.9)
* Medium (4.0 – 6.9)
* High (7.0 – 8.9)
* Critical (9.0 – 10.0)

### 4. Risk Analysis

The system computes:

* Severity distribution
* Average CVSS score
* Overall weighted risk score
* Most vulnerable service

### 5. Machine Learning Model

A Random Forest classifier is trained using:

* Features: Port number, CVSS score
* Label: Severity category

The trained model is stored and reused for predictions.

### 6. Real-Time Prediction

New vulnerabilities can be evaluated instantly:

```bash
python3 scripts/predict_risk.py 443 9.4
```
---

## 📸 Screenshots

### 1. Interactive Terminal Dashboard
![Dashboard Output](screenshots/ADAPTIVE_1.PNG)
*Real-time vulnerability breakdown showing 8 alerts with risk score of 13*

### 2. Automated Web Scanner in Action
![Scanner Running](screenshots/ADAPTIVE_2.PNG)
*Spider and Active scan progress tracking in real-time*

### 3. Machine Learning Threat Predictions
![ML Predictions](screenshots/ADAPTIVE_3.PNG)
*AI-powered threat predictor with confidence scores*

### 4. Professional HTML Security Report
![HTML Report](screenshots/ADAVPTIVE_4.PNG)
*Clean, professional HTML report with complete vulnerability details*

---
---

## 🚨 Live Scan Alerting

The system performs a live scan, analyzes results, and **raises alerts when Critical or High risks are detected**.

Example alert output:

```
[ALERT] Critical vulnerability detected on port 443 (CVSS: 9.4)
```

---

## 📊 Results

* Accurate extraction of vulnerability intelligence
* Correct severity classification
* Machine learning accuracy above acceptable academic thresholds
* Successful real-time risk prediction

---

## 🎓 Academic Relevance

This project demonstrates:

* Practical cybersecurity tooling
* Secure data processing pipelines
* Applied machine learning in security
* Risk-based decision-making
* Adaptive threat detection concepts

It is suitable for:

* Master’s-level coursework
* Cybersecurity research projects
* Portfolio demonstrations

---

## 🔮 Future Enhancements

* Integration with SIEM platforms
* Automated mitigation suggestions
* Live dashboard visualization
* Continuous learning with new scan data
* Network-wide multi-host scanning

---

## 👤 Author

**Babatunde Goriola-Obafemi**
Cybersecurity | Threat Detection | Machine Learning

---

## 📜 License

This project is for academic and educational purposes.

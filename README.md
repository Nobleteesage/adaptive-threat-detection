# 🛡️ Adaptive Cybersecurity Threat Detection System v2.0

## 📌 Overview

This project implements a **comprehensive adaptive cybersecurity threat detection system** that combines:
- **Network vulnerability scanning** (Nmap)
- **Web application security testing** (OWASP ZAP)
- **Machine learning threat prediction**
- **Real-time dashboards and reporting**

**NEW in v2.0:** Web security scanning, interactive dashboards, HTML reports, and enhanced ML predictions!

---

## 🎯 Key Features

### Phase 1: Network Security (Original)
✅ Nmap vulnerability scanning  
✅ CVE and CVSS intelligence extraction  
✅ Severity classification  
✅ Risk scoring and analysis  
✅ Random Forest ML model for threat prediction  

### Phase 2: Web Security (NEW - v2.0)
🆕 **OWASP ZAP automated web scanning**  
🆕 **Real-time vulnerability detection**  
🆕 **Interactive terminal dashboard**  
🆕 **Beautiful HTML security reports**  
🆕 **Enhanced ML threat predictor**  
🆕 **Risk score visualization**  

---

## 🧠 Enhanced System Architecture
```
┌─────────────────────────────────────────────────────────┐
│                  SCANNING LAYER                         │
│  ┌──────────────┐              ┌──────────────┐        │
│  │     Nmap     │              │  OWASP ZAP   │        │
│  │   (Network)  │              │  (Web Apps)  │        │
│  └──────────────┘              └──────────────┘        │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│              DATA PROCESSING LAYER                      │
│  • XML/JSON parsing  • Data normalization               │
│  • CVE extraction    • Risk classification              │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│           MACHINE LEARNING LAYER                        │
│  • Feature extraction  • Random Forest training         │
│  • Threat prediction   • Confidence scoring             │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│            VISUALIZATION LAYER (NEW)                    │
│  • Terminal Dashboard  • HTML Reports                   │
│  • Risk Breakdown      • Alert System                   │
└─────────────────────────────────────────────────────────┘
```

---

## 🛠 Tools & Technologies

| Category | Tools |
|----------|-------|
| **Scanners** | Nmap, OWASP ZAP |
| **Language** | Python 3 |
| **ML Libraries** | scikit-learn, numpy, pandas |
| **Web Security** | ZAP Python API (zaproxy) |
| **Visualization** | Custom HTML/CSS, Terminal dashboards |
| **OS** | Kali Linux |

---

## 📂 Project Structure
```
adaptive-threat-detection/
│
├── data/                          # Scan results and datasets
│   ├── nmap_scan.xml
│   ├── vulnerabilities.csv
│   ├── processed_vulnerabilities.csv
│   ├── automated_scan_results.json    (NEW)
│   └── ml_enhanced_results.json       (NEW)
│
├── scripts/                       # Original Nmap scripts
│   ├── parse_nmap.py
│   ├── preprocess_data.py
│   ├── risk_analysis.py
│   ├── train_model.py
│   ├── predict_risk.py
│   └── live_scan_alert.py
│
├── zap_scanner/                   # NEW - Web security scanner
│   └── automated_scan.py
│
├── ml_models/                     # NEW - Enhanced ML models
│   └── ml_threat_predictor.py
│
├── dashboards/                    # NEW - Visualization tools
│   └── dashboard.py
│
├── reports/                       # NEW - Report generators
│   ├── generate_html_report.py
│   └── scan_report.html
│
├── models/
│   └── risk_model.pkl
│
└── README.md
```

---

## 🚀 Quick Start

### Prerequisites
```bash
# Install dependencies
sudo apt update
sudo apt install nmap zaproxy python3-pip -y
pip3 install pandas scikit-learn python-owasp-zap-v2.4 --break-system-packages
```

### Phase 1: Network Scanning (Original)
```bash
# Run Nmap scan
nmap -sV --script vuln localhost -oX data/nmap_scan.xml

# Process and analyze
python3 scripts/parse_nmap.py
python3 scripts/preprocess_data.py
python3 scripts/risk_analysis.py
python3 scripts/train_model.py
```

### Phase 2: Web Security Scanning (NEW)
```bash
# Terminal 1: Start ZAP
zaproxy -daemon -host 127.0.0.1 -port 8080 -config api.key=MySecretKey123

# Terminal 2: Run automated scan
cd ~/adaptive-threat-detection
python3 zap_scanner/automated_scan.py

# View results
python3 dashboards/dashboard.py
python3 reports/generate_html_report.py
python3 ml_models/ml_threat_predictor.py

# Open HTML report
firefox reports/scan_report.html
```


## 📊 Sample Output

### Terminal Dashboard
```
============================================================
     ADAPTIVE THREAT DETECTION - SCAN REPORT
============================================================

🎯 Target: http://testphp.vulnweb.com
📊 Total Alerts: 8
⚠️  Risk Score: 13

============================================================

📈 VULNERABILITY BREAKDOWN:
------------------------------------------------------------
Medium          | ███ (3)
Low             | █████ (5)

============================================================
```

### ML Predictions
```
🤖 MACHINE LEARNING THREAT PREDICTOR
------------------------------------------------------------
✓ Model trained with 108 samples
✓ Model accuracy: 85.00%

🔮 THREAT PREDICTIONS:
1. Cross Site Scripting (Reflected)
   Actual Risk: Medium
   ML Predicted: Medium (Confidence: 78.5%)
   Status: ✓ Correct prediction
```

---

## 🎯 Use Cases

1. **Academic Research** - Demonstrates ML in cybersecurity
2. **Portfolio Projects** - Shows full-stack security skills
3. **Penetration Testing** - Automated vulnerability assessment
4. **Security Auditing** - Multi-layer threat detection
5. **CTF Competitions** - Rapid vulnerability discovery

---

## 📈 Results & Achievements

| Metric | Phase 1 (Nmap) | Phase 2 (ZAP) |
|--------|----------------|---------------|
| Scan Type | Network | Web Applications |
| Vulnerabilities Detected | Variable | 8 (test scan) |
| ML Accuracy | ~80% | ~85% |
| Reporting | CSV | HTML + Dashboard |
| Real-time Alerts | ✅ | ✅ |

---

## 🔄 Workflow
```
User Input (Target URL/IP)
         ↓
    [Scanning]
         ↓
   [Data Parsing]
         ↓
  [ML Processing]
         ↓
  [Risk Analysis]
         ↓
[Dashboard/Report]
         ↓
    [Alerts]
```

---

## 🎓 Academic Significance

This project demonstrates:
- **Multi-layered security testing** (Network + Web)
- **Applied machine learning** in threat intelligence
- **Automated security workflows**
- **Data visualization** for security metrics
- **Risk quantification** methodologies

Suitable for:
- Master's cybersecurity coursework
- Research publications
- Industry portfolio
- Security certifications (CEH, OSCP prep)

---

## 🔮 Future Enhancements

- [ ] API fuzzing integration
- [ ] SIEM platform integration
- [ ] Docker containerization
- [ ] Multi-target parallel scanning
- [ ] Automated remediation suggestions
- [ ] Deep learning threat prediction
- [ ] Cloud deployment (AWS/Azure)
- [ ] Mobile app security testing

---

## 🤝 Contributing

Contributions are welcome! Areas for improvement:
- Additional ML algorithms
- More visualization options
- Integration with other scanners
- Enhanced reporting formats

---

## 👤 Author

**Babatunde Goriola-Obafemi**  
Cybersecurity Researcher | Threat Detection | Machine Learning

---

## 📜 License

This project is for academic and educational purposes.

---

## 🙏 Acknowledgments

- OWASP ZAP Community
- Nmap Security Scanner
- scikit-learn Documentation

---

**⭐ Star this repo if you find it useful!**

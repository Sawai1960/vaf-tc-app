# VAF-TC Precision Analyzer: Clinical Genetics Support Tool

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://vaf-tc-app.streamlit.app/)

## 🧬 Overview
**VAF-TC Precision Analyzer** is a clinical decision-support tool for differentiating somatic and germline variants by modeling the relationship between **Pathological Tumor Content (TC)** and **Variant Allele Frequency (VAF)**. 

Distinguishing germline variants (e.g., HBOC) from somatic drivers with LOH is critical for treatment and genetic counseling. This tool identifies mathematical "Grey Zones" where VAF-based interpretation becomes ambiguous.

---

## 🚀 Key Clinical Features

### 1. The "50% VAF Trap" (TC 60-75%)
In clinical NGS, VAF ≈ 50% is often incorrectly assumed to be a germline variant. 
- **The Intersection:** At TC ≈ 66.7%, a **Somatic LOH (deletion)** event yields a theoretical VAF of **50%**.
- **Dynamic Alert:** The app warns users when TC is in the 60-75% range, highlighting that somatic mutations can mimic germline findings.

### 2. High TC Convergence Zone (≥90%)
At very high tumor purity, theoretical models for Somatic LOH and Germline LOH mathematically converge toward 100%.
- **The Logic:** As $TC \to 100\%$, both models' VAFs approach 1.0. 
- **Impact:** The tool flags this as a "Mathematical Limit," notifying clinicians that VAF alone cannot distinguish the variant's origin (e.g., *TP53* somatic LOH vs. germline LOH) without clinical correlation.

### 3. Multi-Model Compatibility (±10% Range)
Accounting for NGS technical variance and genomic complexity, the tool lists all theoretical models within a **±10% VAF margin**, supporting a conservative diagnostic approach.

---

## 🩺 Clinical & Regulatory Guidance

### Pathological TC as Gold Standard
This tool prioritizes **Pathological Tumor Content** assessed by a pathologist to avoid the circular reasoning inherent in NGS-derived purity estimates.

### PARP Inhibitor (PARPi) Indications
While Biallelic Inactivation (LOH) is a biological driver of sensitivity, clinical indications are organ-specific:
- **Ovarian & Prostate:** Approved for both **gBRCA and sBRCA**.
- **Breast & Pancreatic:** Typically limited to **gBRCA Only**.

---

## 🌐 Live Application
👉 **[https://vaf-tc-app.streamlit.app/](https://vaf-tc-app.streamlit.app/)**

---

## 📊 Mathematical Foundation
Models used ($f$ = Tumor Fraction):
- **Somatic Heterozygous:** $VAF = f / 2$
- **Somatic LOH (Deletion):** $VAF = f / (2 - f)$
- **Germline Heterozygous:** $VAF = 0.5$
- **Germline LOH (Deletion):** $VAF = 1 / (2 - f)$

---

## 🛠 Usage
```bash
git clone [https://github.com/Clinical-Genetics-Suite-App/vaf-tc-app.git](https://github.com/Clinical-Genetics-Suite-App/vaf-tc-app.git)
pip install -r requirements.txt
streamlit run app.py

# VAF-TC Relationship Visualizer 🧬

## Overview
The **VAF-TC Relationship Visualizer** is an interactive clinical tool designed to assist in the interpretation of genetic variants by modeling the mathematical relationship between **Pathological Tumor Content (TC)** and **Variant Allele Fraction (VAF)**. 

This tool helps clinicians and researchers evaluate the likelihood of germline vs. somatic events, providing a theoretical framework based on Knudson's Two-Hit Theory and various copy number alteration models.

## 🚀 Live Application
Access the interactive web tool here:
**[https://vaf-tc-app.streamlit.app/](https://vaf-tc-app.streamlit.app/)**

## Key Features
* **Automated Interpretation:** Dynamically identifies all theoretical models that align with the sample within a **±10% measurement error threshold**, acknowledging the inherent variance in clinical NGS data.
* **Convergence Zone (Gray Zone) Alert:** A targeted warning system for samples where theoretical curves for germline LOH and somatic LOH converge (typically TC 60–75%). In this range, distinguishing events based on VAF alone is mathematically challenging.
* **Pathological Integration:** Designed to work with **Pathological TC (%)** determined by a pathologist to ensure higher diagnostic reliability compared to NGS-based estimations.
* **Clinical Notes:** Provides essential insights into measurement tolerance, high-TC context (TC ≥ 90%), and therapeutic implications regarding PARP inhibitors.

## Clinical Significance
Distinguishing between germline and somatic variants is a complex task in tumor-only sequencing. As demonstrated in clinical studies, samples with high tumor content (TC ≥ 90%) and elevated VAFs are at risk of being misidentified as somatic events, while they may actually represent **Germline LOH**.

Accurate identification of **Biallelic inactivation (LOH)** is therapeutically significant. Regardless of whether the initial variant is germline or somatic in origin, the presence of LOH is a critical indicator for sensitivity to targeted therapies, such as **PARP inhibitors** in ovarian and breast cancers.

## How to Use
1. **Input Parameters:** Use the sidebar to input the **Gene Name**, **Pathological TC (%)**, and observed **VAF (%)**. A guide is provided in the sidebar for new users.
2. **Analyze:** The black circle represents your specific clinical sample.
3. **Automated Interpretation:** The tool lists all theoretical models that fall within the ±10% error margin of your data.
4. **Clinical Correlation:** If the sample falls into the **Convergence Zone**, a warning will appear prompting further clinical correlation (e.g., family history or drug response).

## Installation (Local Execution)
To run this tool locally:
```bash
git clone [https://github.com/Clinical-Genetics-Suite/vaf-tc-app.git](https://github.com/Clinical-Genetics-Suite/vaf-tc-app.git)
cd vaf-tc-app
pip install -r requirements.txt
streamlit run app.py

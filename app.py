import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# --- Professional Page Configuration ---
st.set_page_config(page_title="VAF-TC Visualizer | Clinical Decision Support", layout="wide")
st.title("🧪 VAF–Tumor Content Graph Visualizer")

# Custom CSS for the Advice Box (Corrected parameter name)
st.markdown("""
<style>
.advice-box { padding: 15px; border-radius: 5px; border: 1px solid #d4af37; background-color: #f9f9f9; color: #333; }
.advice-title { font-weight: bold; font-size: 1.1em; color: #b71c1c; margin-bottom: 5px; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
### Interactive interpretation of variant allele fraction in tumor-only sequencing data.
---
**Overview:** This application visualizes the relationship between **Variant Allele Fraction (VAF)** and **Pathological Tumor Content (TC)** based on the **Knudson two-hit hypothesis**. By plotting observed patient data against theoretical reference lines, it assists in the discrimination between germline (hereditary) and somatic (acquired) variants.
""")

# --- Sidebar for Data Input ---
st.sidebar.header("Patient Data Input")
st.sidebar.markdown("---")
tc = st.sidebar.slider("Pathological Tumor Content (TC)", 0.0, 1.0, 0.5, 0.01)
vaf = st.sidebar.slider("Observed VAF", 0.0, 1.0, 0.5, 0.01)
gene = st.sidebar.text_input("Variant Identifier (e.g., BRCA2 p.L2848*)", "Variant X")

st.sidebar.info("""
**Instructions:** Adjust the sliders to plot the patient's data point (black dot). Proximity to theoretical lines indicates potential genomic mechanisms.
""")

# --- Interpretation Logic ---
tol = 0.05
germline_hetero = 0.5
germline_loh_del = 1 / (2 - tc) if tc < 1 else 1.0
germline_loh_cn = 0.5 * tc + 0.5
somatic_hetero = 0.5 * tc
somatic_loh_del = tc / (2 - tc) if tc < 2 else 1.0
somatic_loh_cn = tc

advice_text = ""

# Intersection Case: TC 0.5 / VAF 0.5
if abs(tc - 0.5) < 0.05 and abs(vaf - 0.5) < 0.05:
    advice_text = "**Inconclusive Intersection:** This data point lies where 'Heterozygous Germline' and 'Somatic with Copy-neutral LOH' converge. VAF analysis alone cannot distinguish the origin. Detailed family history and confirmatory germline testing are essential."
# Gray Zone: TC 0.6-0.7
elif 0.60 <= tc <= 0.70:
    advice_text = "**TC Gray Zone Alert (60-70%):** At this tumor content, theoretical lines for germline and somatic LOH overlap significantly. Interpret with caution. Clinical integration (age of onset, pedigree) is prioritized over VAF-based modeling."
# Likely Germline LOH (Deletion or CN-LOH)
elif abs(vaf - germline_loh_cn) < tol or abs(vaf - germline_loh_del) < tol:
    advice_text = "**Likely Germline with LOH:** The high VAF relative to TC suggests a hereditary variant that has undergone biallelic inactivation (Loss of Heterosity) within the tumor."
# Likely Germline Hetero
elif abs(vaf - germline_hetero) < tol:
    advice_text = "**Likely Heterozygous Germline:** The VAF remains stable at approximately 0.5, consistent with a constitutional heterozygous state regardless of tumor content."
# Likely Somatic LOH
elif abs(vaf - somatic_loh_cn) < tol or abs(vaf - somatic_loh_del) < tol:
    advice_text = "**Likely Somatic with LOH:** The VAF correlates strongly with tumor content, suggesting an acquired variant that has undergone clonal selection and LOH."
# Likely Somatic Hetero
elif abs(vaf - somatic_hetero) < tol:
    advice_text = "**Likely Heterozygous Somatic:** The VAF is approximately half of the tumor content, indicating a typical acquired subclonal or clonal event without copy number changes."
# No Match
else:
    advice_text = "**Atypical Distribution:** The observed VAF does not align with standard diploid models. Consider potential subclonality, non-diploid tumor states, or technical noise."

# --- Main Visualization Area ---
col1, col2 = st.columns([3, 1])

with col1:
    x_range = np.linspace(0.01, 1.0, 100)
    fig, ax = plt.subplots(figsize=(10, 7))
    
    # Plotting Lines
    ax.plot(x_range, 0.5 * x_range + 0.5, color='#D4AF37', label="Germline + cnLOH")
    ax.plot(x_range, 1 / (2 - x_range), color='red', label="Germline + LOH (Del)")
    ax.axhline(0.5, color='brown', linewidth=2, label="Germline (Hetero)")
    ax.plot(x_range, x_range, color='green', linestyle='--', alpha=0.5, label="Somatic + cnLOH")
    ax.plot(x_range, x_range / (2 - x_range), color='gray', linestyle=':', label="Somatic + LOH (Del)")
    ax.plot(x_range, 0.5 * x_range, color='gray', linestyle='--', alpha=0.5, label="Somatic (Hetero)")
    
    ax.scatter(tc, vaf, color='black', s=200, zorder=5, label=f"Patient: {gene}")
    
    ax.set_xlabel("Tumor Content (TC)", fontsize=12)
    ax.set_ylabel("Variant Allele Fraction (VAF)", fontsize=12)
    ax.set_xlim

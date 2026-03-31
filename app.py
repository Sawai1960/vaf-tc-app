import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# --- Page Configuration ---
st.set_page_config(page_title="VAF-TC Precision Analyzer", layout="wide")

st.title("🧬 VAF-TC Clinical Genetics Analyzer")
st.markdown("""
This tool analyzes the relationship between **Pathological Tumor Content (TC)** and **Variant Allele Frequency (VAF)** to differentiate between Somatic and Germline variants, specifically considering LOH (Loss of Heterozygosity) and therapeutic indications.
""")

# --- Sidebar Inputs ---
st.sidebar.header("📋 Patient Data Input")
tc_input = st.sidebar.slider("Pathological Tumor Content (%)", 10, 100, 50, help="Assessment by a pathologist is the gold standard for this model.")
vaf_input = st.sidebar.slider("Observed VAF (%)", 1, 100, 25)
st.sidebar.info("Note: 'Pathological TC' is prioritized over NGS-derived estimates to avoid circular reasoning.")

# --- Mathematical Models (f = Tumor Fraction) ---
f = tc_input / 100

models = {
    "Somatic Heterozygous": (f / 2) * 100,
    "Somatic LOH (with Del)": (f / (2 - f)) * 100,
    "Germline Heterozygous": 50.0,
    "Germline LOH (with Del)": (1 / (2 - f)) * 100
}

# --- 1. Dynamic Alert Logic ---
st.subheader("🚨 Real-time Clinical Alerts")

# Point 1: The 50% VAF Trap (TC 60-75%)
if 60 <= tc_input <= 75:
    theoretical_vaf_loh = models["Somatic LOH (with Del)"]
    st.warning(f"""
    **Alert: The 50% VAF Trap (Grey Zone)**
    At TC {tc_input}%, the theoretical VAF for **Somatic LOH (with Del)** is {theoretical_vaf_loh:.1f}%.
    Crucially, at TC ≈ 66.7%, this somatic model crosses the **50% threshold**.
    A somatic mutation in this range can perfectly mimic a germline variant. 
    **Recommendation:** Do not assume VAF ≈ 50% is Germline. Consider paired-normal testing.
    """)

# Point 5: High TC Convergence (TC >= 90%)
elif tc_input >= 90:
    st.info(f"""
    **⚠️ High TC Analysis Limit (≥90%):**
    At very high tumor purity, the theoretical VAFs for both **Somatic LOH** and **Germline LOH** converge toward 100% (currently {models['Somatic LOH (with Del)']:.1f}% vs {models['Germline LOH (with Del)']:.1f}%). 
    Mathematical differentiation between somatic (e.g., *TP53*) and germline origin is unreliable based on VAF alone. 
    Clinical history and pedigree analysis are mandatory.
    """)
else:
    st.success("Current TC range: No critical mathematical intersections detected.")

# --- 2. Compatible Models (±10% Range) ---
st.subheader("🔍 Compatible Theoretical Models")
st.write(f"Models within a ±10% margin of the observed VAF ({vaf_input}%):")

compatible_data = []
for name, theory_vaf in models.items():
    diff = abs(vaf_input - theory_vaf)
    if diff <= 10.0:
        compatible_data.append({
            "Model Name": name,
            "Theoretical VAF (%)": f"{theory_vaf:.2f}%",
            "Difference (%)": f"{diff:.2f}%"
        })

if compatible_data:
    st.table(pd.DataFrame(compatible_data))
else:
    st.error("No standard models match the observed VAF within a ±10% margin. Consider clonal heterogeneity, aneuploidy, or mosaicism.")

# --- 3. Clinical Interpretation & PARPi Guidance ---
with st.expander("📝 Clinical Interpretation & PARP Inhibitor (PARPi) Notes"):
    st.markdown(f"""
    ### Interpretation Factors
    - **NGS Variance:** Sequencing depth and library prep may cause ±5-10% fluctuations.
    - **Aneuploidy / Copy Number Changes:** Deviations often suggest large-scale genomic gains/losses.
    - **Clonal Heterogeneity:** Subclonal mutations will present with lower-than-expected VAF.

    ### PARP Inhibitor (PARPi) Indications & Regulatory Status
    The identification of **Biallelic Inactivation (LOH)** is a key biomarker for HRD, but clinical indications vary by organ and regulation:
    
    | Organ System | Sensitivity Rationale | Clinical Indication (Typical) |
    | :--- | :--- | :--- |
    | **Ovarian Cancer** | Biallelic inactivation (LOH) | **gBRCA and sBRCA** (Olaparib, Niraparib) |
    | **Prostate Cancer** | Biallelic inactivation (LOH) | **gBRCA and sBRCA** (Olaparib, Rubraca) |
    | **Breast Cancer** | Biallelic inactivation (LOH) | **gBRCA Only** (Olaparib, Talazoparib) |
    | **Pancreatic Cancer** | Biallelic inactivation (LOH) | **gBRCA Only** (Olaparib) |

    *Disclaimer: This tool provides biological insights based on mathematical models. Clinical decisions must align with regional drug labels and professional guidelines (NCCN, ESMO, etc.).*
    """)

# --- 4. Visualization ---
st.subheader("📈 VAF-TC Theoretical Projection")
tc_range = np.linspace(10, 100, 100)
f_range = tc_range / 100

fig = go.Figure()
fig.add_trace(go.Scatter(x=tc_range, y=(f_range/2)*100, name="Somatic Het", line=dict(color='blue', width=1)))
fig.add_trace(go.Scatter(x=tc_range, y=(f_range/(2-f_range))*100, name="Somatic LOH (Del)", line=dict(color='blue', dash='dash')))
fig.add_trace(go.Scatter(x=tc_range, y=[50]*100, name="Germline Het", line=dict(color='green', width=1)))
fig.add_trace(go.Scatter(x=tc_range, y=(1/(2-f_range))*100, name="Germline LOH (Del)", line=dict(color='red', width=2)))

# User Case Point
fig.add_trace(go.Scatter(x=[tc_input], y=[vaf_input], mode='markers+text', 
                         name="Current Case", text=["Case"], textposition="top center",
                         marker=dict(color='black', size=15, symbol='x')))

fig.update_layout(
    xaxis_title="Pathological Tumor Content (%)", 
    yaxis_title="Theoretical VAF (%)",
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    hovermode="x unified"
)
st.plotly_chart(fig, use_container_width=True)

st.divider()
st.caption("Developed by Clinical Genetics Suite (Maintainer: Sawai1960). Version 2.1 (Clinical-Grade Update).")

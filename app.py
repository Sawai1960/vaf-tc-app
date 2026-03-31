import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import io

# 1. Page Configuration
st.set_page_config(page_title="VAF-TC Precision Analyzer", layout="wide")

# 2. Title & Header
st.title("🧬 VAF-TC Precision Analyzer")
st.markdown("Interactive clinical decision-support tool for germline/somatic variant differentiation.")

# 3. Sidebar Input Parameters
st.sidebar.header("📋 Patient Data Input")

# Reverted to English as per your instruction
st.sidebar.markdown("👉 **Please enter Gene Name, TC, and VAF.**")

gene_name = st.sidebar.text_input("Gene Name", value="BRCA2")
tc_input = st.sidebar.slider("Pathological Tumor Content (TC %)", 0, 100, 70)
vaf_input = st.sidebar.slider("Variant Allele Fraction (VAF %)", 0, 100, 57)

st.sidebar.markdown("---")
st.sidebar.info(f"💡 **Analysis Mode:** {gene_name}")

# Normalize inputs
tc = tc_input / 100.0
vaf = vaf_input / 100.0

# 4. Mathematical Foundation (5-Line "Masterpiece" Logic)
x_range = np.linspace(0.01, 1.0, 100)
# Formulas from your high-level version
y_germ_cnloh = (1 + x_range) / 2
y_germ_del = 1 / (2 - x_range)
y_germ_hetero = np.full_like(x_range, 0.5)
y_som_cnloh = x_range
y_som_del = x_range / (2 - x_range)

# 5. Main Layout (Left 1 : Right 2)
# Comments/Alerts on the LEFT, Graph on the RIGHT
col_alerts, col_graph = st.columns([1, 2])

# --- LEFT COLUMN: Clinical Interpretation ---
with col_alerts:
    st.subheader("📋 Interpretation")
    
    # Mathematical Match Analysis (±10% error margin)
    error_margin = 0.10
    models_check = {
        "Germline + cnLOH": (1 + tc) / 2,
        "Germline + LOH (Del)": 1 / (2 - tc),
        "Germline (Hetero)": 0.5,
        "Somatic + cnLOH": tc,
        "Somatic + LOH (Del)": tc / (2 - tc)
    }
    
    compatible_models = [name for name, val in models_check.items() if abs(val - vaf) <= error_margin]

    if compatible_models:
        st.success(f"**Compatible Models for {gene_name}:**")
        for m in compatible_models:
            st.markdown(f"- **{m}**")
    else:
        st.info(f"**Insight:** VAF does not closely align with standard models for {gene_name}.")

    # 3-Tier Dynamic Clinical Alerts
    if 60 <= tc_input <= 75:
        st.warning(f"⚠️ **50% VAF Trap:** At TC {tc_input}%, Somatic LOH mimics Germline Heterozygous. Distinguishing origin by VAF alone is difficult.")

    if tc_input >= 70:
        st.error("⚠️ **LOH Convergence Alert:** High purity causes Germline and Somatic LOH lines to converge. Clinical correlation required.")

    if tc_input >= 90:
        st.info("💡 **Mathematical Limit:** At TC ≥ 90%, models converge toward 100%. Family history is essential.")

    st.divider()

    # Feature: Excel Template Download
    st.subheader("📊 Multi-variant Workflow")
    template_df = pd.DataFrame({"Gene": [gene_name, "TP53"], "TC": [tc_input, tc_input], "VAF": [vaf_input, 0.0]})
    csv_buffer = io.BytesIO()
    template_df.to_csv(csv_buffer, index=False)
    st.download_button("📥 Download Excel/CSV Template", csv_buffer.getvalue(), "VAF_TC_Template.csv", "text/csv")

    # Therapeutic Implications (README Integration)
    with st.expander("📝 Clinical Notes", expanded=True):
        st.markdown("""
        **PARPi Indications:**
        - **Ovarian/Prostate:** gBRCA & sBRCA eligible.
        - **Breast/Pancreas:** gBRCA Only (includes **Talazoparib**).
        
        **Lynch Syndrome (MMR-d):**
        - High responsiveness to **ICIs**. Biallelic loss is a key differentiator.
        """)

# --- RIGHT COLUMN: Visualization ---
with col_graph:
    st.subheader("📈 VAF-TC Projection")
    fig = go.Figure()
    
    # 5 Specific Theoretical Lines
    fig.add_trace(go.Scatter(x=x_range*100, y=y_germ_cnloh*100, name="Germline + cnLOH", line=dict(color='#d4af37', width=2)))
    fig.add_trace(go.Scatter(x=x_range*100, y=y_germ_del*100, name="Germline + LOH (Del)", line=dict(color='#e41a1c', width=2)))
    fig.add_trace(go.Scatter(x=x_range*100, y=y_germ_hetero*100, name="Germline (Hetero)", line=dict(color='#a65628', width=2)))
    fig.add_trace(go.Scatter(x=x_range*100, y=y_som_cnloh*100, name="Somatic + cnLOH", line=dict(color='#4daf4a', dash='dash')))
    fig.add_trace(go.Scatter(x=x_range*100, y=y_som_del*100, name="Somatic + LOH (Del)", line=dict(color='#377eb8', dash='dot')))

    # Case Plot with Marker & Text
    fig.add_trace(go.Scatter(
        x=[tc_input], y=[vaf_input],
        mode='markers+text',
        name=f"Current Case: {gene_name}",
        text=[f"{gene_name}<br>TC:{tc_input}%<br>VAF:{vaf_input}%"],
        textposition="top right",
        marker=dict(color='black', size=14, symbol='x')
    ))

    # Low Confidence Zone Annotation
    fig.add_vrect(x0=0, x1=30, fillcolor="gray", opacity=0.1, layer="below", line_width=0, 
                  annotation_text="Low Confidence Zone", annotation_position="top left")

    fig.update_layout(
        xaxis_title="Pathological Tumor Content (%)", yaxis_title="Variant Allele Fraction (%)",
        yaxis=dict(range=[0, 105]), xaxis=dict(range=[0, 105]),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        template="simple_white", height=600
    )
    st.plotly_chart(fig, use_container_width=True)

# 6. Footer
st.divider()
st.caption("VAF-TC Precision Analyzer | Clinical Genetics Suite | ver 2.5 ✅")

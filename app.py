import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import io

# 1. Page Configuration
st.set_page_config(page_title="VAF-TC Precision Analyzer", layout="wide")

# 2. Title
st.title("🧬 VAF-TC Precision Analyzer")
st.markdown("Interactive visual tool for germline/somatic variant differentiation in tumor-only sequencing.")
st.caption("⚠️ This tool is intended as a supportive aid for genetic counseling. It does not replace confirmatory germline testing or established clinical guidelines.")

# 3. Sidebar Input Parameters
st.sidebar.header("📋 Patient Data Input")
st.sidebar.markdown("👉 **Please enter Gene Name, TC, and VAF.**")

gene_name = st.sidebar.text_input("Gene Name", value="BRCA2")
tc_input = st.sidebar.slider("Pathological Tumor Content (TC %)", 0, 100, 50)
vaf_input = st.sidebar.slider("Variant Allele Fraction (VAF %)", 0, 100, 50)

st.sidebar.markdown("---")
st.sidebar.info(f"💡 **Analysis Mode:** {gene_name}")

tc = tc_input / 100.0
vaf = vaf_input / 100.0

# 4. Mathematical Foundation (diploid model)
x_range = np.linspace(0.01, 1.0, 100)
y_germ_cnloh = (1 + x_range) / 2
y_germ_del = 1 / (2 - x_range)
y_germ_hetero = np.full_like(x_range, 0.5)
y_som_cnloh = x_range
y_som_del = x_range / (2 - x_range)

# 5. Main Layout (Left 1 : Right 2)
col_alerts, col_graph = st.columns([1, 2])

# --- LEFT COLUMN: Clinical Interpretation & Alerts ---
with col_alerts:
    st.subheader("📋 Interpretation & Alerts")

    # Mathematical Match Analysis (±10% error margin)
    error_margin = 0.10
    models_check = {
        "Germline + cnLOH": (1 + tc) / 2,
        "Germline + LOH (Del)": 1 / (2 - tc),
        "Germline (Hetero)": 0.5,
        "Somatic + cnLOH": tc,
        "Somatic + LOH (Del)": tc / (2 - tc)
    }
    compatible_models = [
        (name, val) for name, val in models_check.items()
        if abs(val - vaf) <= error_margin
    ]

    if compatible_models:
        st.success(f"**Compatible Models for {gene_name} (±10%):**")
        for name, val in compatible_models:
            st.markdown(f"- **{name}** — theoretical VAF {val*100:.1f}%")
    else:
        st.info(f"**Insight:** VAF {vaf_input}% does not align with any standard model at TC {tc_input}% (±10%).")

    # --- Clinical Alerts ---

    # Pre-compute key thresholds
    som_cnloh_vaf = tc * 100                        # Somatic + cnLOH = TC
    som_del_vaf = tc / (2 - tc) * 100               # Somatic + LOH (Del)
    germ_del_vaf = 1 / (2 - tc) * 100               # Germline + LOH (Del)

    # Trap 1: Somatic cnLOH Trap (TC 40–60%)
    #   At TC ≈ 50%, Somatic+cnLOH = TC ≈ 50% = Germline Hetero
    if 40 <= tc_input <= 60:
        st.warning(
            f"⚠️ **Somatic cnLOH Trap:** At TC {tc_input}%, Somatic cnLOH (UPD) "
            f"produces VAF = {som_cnloh_vaf:.0f}%, which falls within ±10% of "
            f"Germline Heterozygous (50%). A somatic variant with cnLOH can "
            f"masquerade as a germline heterozygous variant. "
            f"Pair-normal testing is essential."
        )

    # Trap 2: Somatic LOH (Del) approaching 50% (TC 61–66%)
    #   Gray Zone: Somatic+LOH(Del) approaches Germline Hetero from below
    elif 61 <= tc_input <= 66:
        st.warning(
            f"⚠️ **Gray Zone (Somatic LOH Del):** At TC {tc_input}%, "
            f"Somatic LOH (deletion) produces VAF = {som_del_vaf:.1f}%, "
            f"approaching Germline Heterozygous (50%). "
            f"Confirmation testing is recommended."
        )

    # Alert 3: LOH Convergence Zone (TC ≥ 67%)
    #   At TC = 2/3 ≈ 66.7%, Somatic+LOH(Del) = Germline Hetero = 50%
    #   Above this TC, the somatic and germline LOH lines converge
    elif tc_input >= 67:
        if vaf_input >= tc / (2 - tc) * 100:
            st.error(
                f"🔴 **LOH Convergence Alert:** At TC {tc_input}% and VAF {vaf_input}%, "
                f"the variant falls at or above the Somatic LOH (deletion) line "
                f"({som_del_vaf:.1f}%). In this region, Germline LOH (Del) = "
                f"{germ_del_vaf:.1f}% and Somatic LOH (Del) = {som_del_vaf:.1f}% "
                f"converge — origin cannot be determined by VAF alone. "
                f"Germline confirmation is essential."
            )
        if tc_input >= 90:
            st.warning(
                f"⚠️ **Extreme Tumor Purity:** At TC {tc_input}%, all theoretical "
                f"models compress into a narrow VAF range. Variants may still be "
                f"of somatic origin even at high VAF. "
                f"Family history review and germline testing are essential."
            )

    st.divider()

    # Feature: CSV Template Download
    st.subheader("📊 Multi-variant Workflow")
    template_df = pd.DataFrame({"Gene": [gene_name, "TP53"], "TC": [tc_input, tc_input], "VAF": [vaf_input, 0.0]})
    csv_buffer = io.BytesIO()
    template_df.to_csv(csv_buffer, index=False)
    st.download_button("📥 Download CSV Template", csv_buffer.getvalue(), "VAF_TC_Template.csv", "text/csv")

    # Clinical Notes
    with st.expander("📝 Clinical Notes", expanded=True):
        st.markdown("""
        **PARPi Indications:**
        - **Ovarian/Prostate:** gBRCA & sBRCA eligible.
        - **Breast/Pancreas:** gBRCA only.

        **Lynch Syndrome:**
        - High responsiveness to **ICIs**. Biallelic loss is a key differentiator.
        """)

# --- RIGHT COLUMN: Visualization ---
with col_graph:
    st.subheader("📈 VAF-TC Projection")
    fig = go.Figure()

    fig.add_trace(go.Scatter(x=x_range*100, y=y_germ_cnloh*100, name="Germline + cnLOH", line=dict(color='#d4af37', width=2)))
    fig.add_trace(go.Scatter(x=x_range*100, y=y_germ_del*100, name="Germline + LOH (Del)", line=dict(color='#e41a1c', width=2)))
    fig.add_trace(go.Scatter(x=x_range*100, y=y_germ_hetero*100, name="Germline (Hetero)", line=dict(color='#a65628', width=2)))
    fig.add_trace(go.Scatter(x=x_range*100, y=y_som_cnloh*100, name="Somatic + cnLOH", line=dict(color='#4daf4a', dash='dash')))
    fig.add_trace(go.Scatter(x=x_range*100, y=y_som_del*100, name="Somatic + LOH (Del)", line=dict(color='#377eb8', dash='dot')))

    # Case Plot
    fig.add_trace(go.Scatter(
        x=[tc_input], y=[vaf_input],
        mode='markers+text',
        name=f"Current: {gene_name}",
        text=[f"{gene_name}<br>TC:{tc_input}%<br>VAF:{vaf_input}%"],
        textposition="top right",
        marker=dict(color='black', size=14, symbol='circle')
    ))

    # Low Confidence Zone (TC < 30%)
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
st.caption("VAF-TC Precision Analyzer | Clinical Genetics Suite | ver 3.0 ✅")

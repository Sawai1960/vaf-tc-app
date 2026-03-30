import streamlit as st
import plotly.graph_objects as go
import numpy as np

# Page Configuration
st.set_page_config(page_title="VAF-TC Visualizer", layout="wide")

st.title("🧬 VAF-TC Relationship Visualizer")
st.write("Interactive tool to visualize the theoretical relationship between Tumor Content (TC) and Variant Allele Fraction (VAF).")

# --- Sidebar Inputs ---
st.sidebar.header("📊 Parameter Input")
tc_input = st.sidebar.slider("Pathological Tumor Content (TC %)", 0, 100, 50)
vaf_input = st.sidebar.slider("Variant Allele Fraction (VAF %)", 0, 100, 50)

# --- Theoretical Curve Calculations ---
def calculate_curves():
    tc_range = np.linspace(0, 1, 101)
    
    # Germline Models
    g_hetero = np.full_like(tc_range, 0.5)
    g_loh_del = 1 / (2 - tc_range)
    g_cnloh = 0.5 * (1 + tc_range)
    
    # Somatic Models
    s_hetero = 0.5 * tc_range
    s_loh_del = tc_range / (2 - tc_range)
    s_cnloh = tc_range
    
    return tc_range * 100, g_hetero * 100, g_loh_del * 100, g_cnloh * 100, s_hetero * 100, s_loh_del * 100, s_cnloh * 100

tc_plot, g_het, g_del, g_cn, s_het, s_del, s_cn = calculate_curves()

# --- Graph Construction ---
fig = go.Figure()

# Plotting Theoretical Lines
fig.add_trace(go.Scatter(x=tc_plot, y=g_cn, name="Germline + cnLOH", line=dict(color='#D4AF37', width=2)))
fig.add_trace(go.Scatter(x=tc_plot, y=g_del, name="Germline + LOH (Del)", line=dict(color='red', width=2)))
fig.add_trace(go.Scatter(x=tc_plot, y=g_het, name="Germline (Hetero)", line=dict(color='brown', width=2)))
fig.add_trace(go.Scatter(x=tc_plot, y=s_cn, name="Somatic + cnLOH", line=dict(color='green', dash='dash')))
fig.add_trace(go.Scatter(x=tc_plot, y=s_del, name="Somatic + LOH (Del)", line=dict(color='#666', dash='dot')))

# Low Confidence Zone Shading
fig.add_vrect(x0=0, x1=30, fillcolor="rgba(200, 200, 200, 0.2)", layer="below", line_width=0, 
              annotation_text="Low Confidence Zone", annotation_position="top left")

# User Input Point
fig.add_trace(go.Scatter(x=[tc_input], y=[vaf_input], name="Current Sample", mode='markers+text',
                         marker=dict(color='black', size=12, symbol='circle'),
                         text=[f"TC:{tc_input}% VAF:{vaf_input}%"], textposition="top right"))

# Layout Settings (Fixed 0-100% Scales)
fig.update_layout(
    xaxis=dict(title="Pathological Tumor Content (%)", range=[0, 100], dtick=10),
    yaxis=dict(title="Variant Allele Fraction (%)", range=[0, 100], dtick=25),
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    margin=dict(l=40, r=40, t=80, b=40),
    height=600
)

st.plotly_chart(fig, use_container_width=True)

# --- Alert Section ---

# 1. Convergence Zone (Gray Zone) Alert (TC >= 70%)
if tc_input >= 70:
    st.warning(f"""
    ⚠️ **Convergence Zone (Gray Zone) Alert**:  
    The current Tumor Content is **{tc_input}%**. In this high-purity range, the theoretical curves for **Germline LOH** and **Somatic LOH** converge significantly. 
    Distinguishing between germline and somatic events based on VAF alone may be challenging. 
    Clinical correlation (e.g., family history, drug response) is strongly recommended.
    """)

# 2. Low Confidence Alert (TC < 30%)
elif tc_input < 30:
    st.info("ℹ️ **Low Confidence Zone**: Analysis reliability may be reduced when TC is below 30%.")

# --- Clinical Context Section ---
st.markdown("---")
st.subheader("📖 Clinical Interpretation Notes")
st.write(f"""
- **Convergence Zone**: As TC increases, the mathematical gap between Germline and Somatic LOH VAF values narrows.
- **Clinical Significance**: As demonstrated in high-TC cases (TC $\ge$ 90%), variants with high VAF values can be misidentified as somatic events. Our study confirmed these as **Germline LOH**, supported by clinical outcomes such

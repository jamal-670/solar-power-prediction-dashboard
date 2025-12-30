import streamlit as st
import pandas as pd
import numpy as np
import joblib

# ==========================================
# 1. PAGE SETUP (Professional Business Layout)
# ==========================================
st.set_page_config(
    page_title="Solar Expansion Planning Tool", 
    page_icon="🏗️",
    layout="centered"
)

# ==========================================
# 2. LOAD MODEL
# ==========================================
@st.cache_resource
def load_model():
    try:
        model = joblib.load('solar_xgboost_model.pkl')
        return model
    except FileNotFoundError:
        st.error("⚠️ Error: Model file not found.")
        return None

model = load_model()

# ==========================================
# 3. SIDEBAR (CONTEXT & INPUTS)
# ==========================================
st.sidebar.title("🏗️ Project Parameters")

# --- CONTEXT SECTION (UPDATED DETAILS) ---
with st.sidebar.expander("ℹ️ Technical Specifications", expanded=True):
    st.markdown("""
    **Reference Site Comparison:**
    Both sites operate **22 String Inverters**, providing a direct A/B comparison for the new facility. However, they utilize different mounting and panel technologies:

    ---
    **📍 Reference Site A (Baseline)**
    * **Configuration:** Fixed-Tilt Mounting (20°)
    * **Technology:** Polycrystalline Panels
    * **Efficiency:** Standard Commercial Grade
    * *Role: Conservative lower-bound estimate.*

    ---
    **📍 Reference Site B (Optimized)**
    * **Configuration:** Seasonal Tilt / Optimized Orientation
    * **Technology:** Monocrystalline PERC (High Efficiency)
    * **Efficiency:** Premium Grade
    * *Role: Performance upper-bound estimate.*
    """)

st.sidebar.divider()
st.sidebar.header("Forecast Inputs")

# Inputs
date_time = st.sidebar.time_input("Target Time", value=pd.to_datetime("12:00").time())
ambient_temp = st.sidebar.slider("Ambient Temperature (°C)", 20.0, 45.0, 32.0)
module_temp = st.sidebar.slider("Panel Temperature (°C)", 20.0, 75.0, 50.0)
irradiation = st.sidebar.slider("Irradiation (kW/m²)", 0.0, 1.2, 0.8)

# ==========================================
# 4. MAIN PAGE
# ==========================================
st.title("Solar Plant Feasibility Dashboard")
st.markdown("""
### 📊 New Construction Benchmarking
Use this tool to predict power generation capacity for the **Proposed Solar Facility**. 
Calculations are based on historical performance data from Reference Sites A & B.
""")

st.divider()

# ==========================================
# 5. PREDICTION LOGIC
# ==========================================
if st.button("Calculate Estimated Output", type="primary"):
    if model:
        # Extract features
        hour = date_time.hour
        minute = date_time.minute
        
        # Create input for both reference plants to compare
        input_data = pd.DataFrame({
            'AMBIENT_TEMPERATURE': [ambient_temp, ambient_temp],
            'MODULE_TEMPERATURE': [module_temp, module_temp],
            'IRRADIATION':         [irradiation, irradiation],
            'HOUR':                [hour, hour],
            'MINUTE':              [minute, minute],
            'PLANT_CODE':          [0, 1] 
        })
        
        # Predict
        predictions = model.predict(input_data)
        
        # Results
        site_a_power = max(0, predictions[0]) 
        site_b_power = max(0, predictions[1])
        
        # We assume the new plant might be a mix or sum of these capabilities
        total_capacity = site_a_power + site_b_power
        
        # ==========================================
        # 6. RESULTS DISPLAY
        # ==========================================
        st.subheader("💡 Feasibility Analysis Results")
        
        # High Level Metric
        st.success(f"**Projected System Output:** {total_capacity:,.2f} kW")
        st.caption(f"Estimated output for a dual-array facility under defined weather conditions.")
        
        # Comparison Columns
        col1, col2 = st.columns(2)
        
        with col1:
            st.info("📉 **Conservative Estimate**")
            st.metric("Based on Site A (Fixed Tilt)", f"{site_a_power:,.2f} kW")
            st.write("Baseline yield using standard polycrystalline tech.")
            
        with col2:
            st.info("📈 **Optimized Estimate**")
            st.metric("Based on Site B (Optimized)", f"{site_b_power:,.2f} kW")
            st.write("Potential yield using premium monocrystalline tech.")
            
        # Recommendation Logic
        st.divider()
        if irradiation > 0.8 and total_capacity > 8000:
            st.markdown("### ✅ Recommendation: High Viability")
            st.write("Conditions are ideal for high ROI. The proposed location shows excellent potential for peak load generation matching the Optimized Site B profile.")
        elif irradiation < 0.2:
            st.markdown("### ⚠️ Recommendation: Storage Required")
            st.write("Low irradiation conditions. Feasibility depends on battery storage integration.")
        else:
            st.markdown("### ℹ️ Recommendation: Standard Operation")
            st.write("Output falls within nominal ranges. Financial viability depends on grid tariff rates.")

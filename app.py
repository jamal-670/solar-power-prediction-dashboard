import streamlit as st
import pandas as pd
import numpy as np
import joblib

# ==========================================
# 1. PAGE SETUP
# ==========================================
st.set_page_config(
    page_title="Solar Energy Predictor", 
    page_icon="☀️",
    layout="centered"
)

# ==========================================
# 2. LOAD MODEL FUNCTION
# ==========================================
@st.cache_resource
def load_model():
    try:
        # Load the trained model from the same folder
        model = joblib.load('solar_xgboost_model.pkl')
        return model
    except FileNotFoundError:
        st.error("⚠️ Error: 'solar_xgboost_model.pkl' not found.")
        st.info("Please make sure the model file is in the same folder as this app.py file.")
        return None

model = load_model()

# ==========================================
# 3. SIDEBAR UI (USER INPUTS)
# ==========================================
st.title("☀️ Combined Solar Power Predictor")
st.markdown("""
Predict the **Total Power Output** for the entire solar farm (Plant 1 + Plant 2) 
based on weather forecast data.
""")

st.sidebar.header("Weather Conditions")

# Input: Time
date_time = st.sidebar.time_input("Time of Day", value=pd.to_datetime("12:00").time())

# Input: Weather Variables
ambient_temp = st.sidebar.slider("Ambient Temperature (°C)", 20.0, 45.0, 32.0)
module_temp = st.sidebar.slider("Module Temperature (°C)", 20.0, 75.0, 50.0)
irradiation = st.sidebar.slider("Irradiation (Sunlight)", 0.0, 1.2, 0.8)

# ==========================================
# 4. PREDICTION LOGIC
# ==========================================
if st.button("Predict Total Power", type="primary"):
    if model:
        # Get Hour and Minute
        hour = date_time.hour
        minute = date_time.minute
        
        # We need to predict for BOTH plants simultaneously.
        # We create a dataframe with 2 rows:
        # Row 0 = Plant 1 (Code 0)
        # Row 1 = Plant 2 (Code 1)
        
        input_data = pd.DataFrame({
            'AMBIENT_TEMPERATURE': [ambient_temp, ambient_temp],
            'MODULE_TEMPERATURE': [module_temp, module_temp],
            'IRRADIATION':         [irradiation, irradiation],
            'HOUR':                [hour, hour],
            'MINUTE':              [minute, minute],
            'PLANT_CODE':          [0, 1] 
        })
        
        # Run Prediction
        predictions = model.predict(input_data)
        
        # Extract results (ensure no negative numbers using max(0, value))
        p1_power = max(0, predictions[0]) 
        p2_power = max(0, predictions[1])
        total_power = p1_power + p2_power
        
        # ==========================================
        # 5. DISPLAY RESULTS
        # ==========================================
        st.divider()
        st.subheader("Results")
        
        # BIG METRIC: Total Power
        st.success(f"⚡ **Total Farm Output:** {total_power:,.2f} kW")
        
        # Breakdown Metrics
        col1, col2 = st.columns(2)
        with col1:
            st.metric("🏭 Plant 1", f"{p1_power:,.2f} kW")
        with col2:
            st.metric("🏭 Plant 2", f"{p2_power:,.2f} kW")
            
        # Fun Logic / Context
        if irradiation == 0:
            st.info("🌙 It is night time. Power generation is zero.")
        elif total_power > 8000:
            st.balloons()
            st.info("🔥 High efficiency detected! The panels are working hard.")

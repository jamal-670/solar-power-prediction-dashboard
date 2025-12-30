
import streamlit as st
import pandas as pd
import numpy as np
import joblib

# ==========================================
# 1. SETUP & LOADING
# ==========================================
st.set_page_config(page_title="Solar Energy Predictor", layout="centered")

@st.cache_resource
def load_model():
    try:
        # Load the model you downloaded from Colab
        model = joblib.load('solar_xgboost_model.pkl')
        return model
    except FileNotFoundError:
        st.error("⚠️ Model file not found! Please make sure 'solar_xgboost_model.pkl' is in the same folder.")
        return None

model = load_model()

# ==========================================
# 2. THE UI (SIDEBAR INPUTS)
# ==========================================
st.title("☀️ Solar Power Generation Predictor")
st.write("Enter the weather conditions below to predict the power output.")

st.sidebar.header("User Input Parameters")

# Sliders for user input
plant_choice = st.sidebar.selectbox("Select Plant", ["Plant 1", "Plant 2"])
date_time = st.sidebar.time_input("Time of Day", value=None)
ambient_temp = st.sidebar.slider("Ambient Temperature (°C)", 20.0, 40.0, 30.0)
module_temp = st.sidebar.slider("Module Temperature (°C)", 20.0, 70.0, 45.0)
irradiation = st.sidebar.slider("Irradiation (Sunlight Intensity)", 0.0, 1.2, 0.5)

# ==========================================
# 3. PREDICTION LOGIC
# ==========================================
if st.button("Predict Power Output"):
    if model:
        # Prepare input data matching the training columns:
        # ['AMBIENT_TEMPERATURE', 'MODULE_TEMPERATURE', 'IRRADIATION', 'HOUR', 'MINUTE', 'PLANT_CODE']
        
        # 1. Handle Time
        if date_time:
            hour = date_time.hour
            minute = date_time.minute
        else:
            hour = 12
            minute = 0
            
        # 2. Handle Plant Code
        plant_code = 0 if plant_choice == "Plant 1" else 1
        
        # 3. Create DataFrame
        input_data = pd.DataFrame({
            'AMBIENT_TEMPERATURE': [ambient_temp],
            'MODULE_TEMPERATURE': [module_temp],
            'IRRADIATION': [irradiation],
            'HOUR': [hour],
            'MINUTE': [minute],
            'PLANT_CODE': [plant_code]
        })
        
        # 4. Make Prediction
        prediction = model.predict(input_data)[0]
        
        # ==========================================
        # 4. SHOW RESULTS
        # ==========================================
        st.success(f"⚡ Predicted DC Power: {prediction:,.2f} kW")
        
        # Visual Logic check
        if prediction < 0:
            st.warning("Note: Predicted negative power. In real life, this means 0 kW (Night time).")
        
        # Fun Context
        if irradiation == 0:
            st.info("It's dark! Solar panels don't work at night. 🌙")
        elif prediction > 10000:
            st.balloons() # Celebration for high power!
            st.info("Excellent generation conditions! ☀️")
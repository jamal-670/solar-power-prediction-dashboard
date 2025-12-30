☀️ Solar Power Generation Predictor

A full-stack Machine Learning project that predicts the DC Power Output of a solar power plant based on weather sensor data.

Built with Python, XGBoost, and Streamlit.

🚀 Live Demo

Click here to view the Dashboard (Update this link after deploying)

📌 Project Overview

Solar energy is intermittent and depends heavily on weather conditions. This project uses historical sensor data (Irradiation, Temperature) to predict power generation, helping grid operators optimize energy flow.

Key Features:

Data Processing: Merged generation and weather data from two different solar plants (68k+ rows).

Feature Engineering: Extracted temporal features (Hour, Minute) to capture daily solar cycles.

Model: Trained an XGBoost Regressor achieving an R² Score of 0.98.

Deployment: Interactive Web Dashboard for real-time predictions.

📊 Dataset

The data comes from two solar power plants in India over a 34-day period.

Inputs: Ambient Temperature, Module Temperature, Irradiation.

Outputs: DC Power, AC Power, Daily Yield.

🛠️ Tech Stack

Language: Python 3.9

Data Manipulation: Pandas, NumPy

Machine Learning: Scikit-Learn, XGBoost

Visualization: Matplotlib, Seaborn, Plotly

Web App: Streamlit

⚙️ How to Run Locally

Clone the repository:

git clone [https://github.com/your-username/solar-power-predictor.git](https://github.com/your-username/solar-power-predictor.git)
cd solar-power-predictor


Install dependencies:

pip install -r requirements.txt


Run the App:

streamlit run app.py


📈 Model Performance

Algorithm: XGBoost Regressor (Gradient Boosting)

R² Score: 0.9823

Insight: "Irradiation" (Sunlight) was the most critical feature, followed by "Module Temperature" (Efficiency loss due to heat).

📂 Project Structure

├── data/                  # Raw CSV files
├── notebooks/             # Jupyter Notebooks for EDA & Training
├── app.py                 # Streamlit Dashboard Code
├── requirements.txt       # Dependencies
├── solar_xgboost_model.pkl # Trained Model File
└── README.md              # Project Documentation


Created by [Your Name]

import streamlit as st
import requests
import joblib
import numpy as np
import os

# ----------------------------------------------------
# Page Configuration
# ----------------------------------------------------
st.set_page_config(page_title="Smart Farming Advisory", page_icon="🌱", layout="centered")

# ----------------------------------------------------
# Custom CSS for UI Enhancement
# ----------------------------------------------------
st.markdown("""
<style>

body {
    background-color: #f3f8f2;
    font-family: "Helvetica Neue", sans-serif;
}

/* Center header text */
.center-text {
    text-align: center;
}

/* Beautiful full-width button */
div.stButton > button {
    width: 100%;
    background-color: #4CAF50 !important;
    color: white !important;
    padding: 16px;
    font-size: 20px !important;
    border-radius: 10px;
    border: none;
    transition: 0.3s;
}

div.stButton > button:hover {
    background-color: #45a049 !important;
    transform: scale(1.01);
}

/* Card container styling */
.card {
    background: #ffffff;
    padding: 25px;
    border-radius: 14px;
    border: 1px solid #d8e6d5;
    box-shadow: 0 2px 8px rgba(0,0,0,0.04);
    margin-bottom: 20px;
}

/* Section titles */
.section-title {
    font-size: 24px;
    font-weight: 600;
    margin-bottom: 10px;
    color: #335c33;
}
</style>
""", unsafe_allow_html=True)

# ----------------------------------------------------
# Load ML Model
# ----------------------------------------------------
MODEL_PATH = os.path.join(os.path.dirname(__file__), "temp_model.pkl")
model = joblib.load(MODEL_PATH)

API_KEY = "ebab3d399da1c49079f35277706aaf7a"

# ----------------------------------------------------
# Weather Fetch Function
# ----------------------------------------------------
def get_weather_data(city):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    if response.status_code != 200:
        raise ValueError("City not found or API request failed.")
    data = response.json()
    return {
        'max_temp': data["main"]["temp_max"],
        'humidity': data["main"]["humidity"],
        'rainfall': data.get("rain", {}).get("1h", 0)
    }

# ----------------------------------------------------
# Generate Advice
# ----------------------------------------------------
def generate_advice(temp, humidity, rainfall):
    advice = []
    if temp > 30:
        advice.append("🔥 High temperature — Consider mulching to help retain moisture.")
    if humidity > 80:
        advice.append("💧 High humidity — Risk of fungal diseases. Monitor closely.")
    if rainfall < 5:
        advice.append("🚿 Low rainfall — Irrigation recommended.")
    if rainfall > 20:
        advice.append("🌧️ Heavy rainfall — Risk of waterlogging.")
    if 20 <= temp <= 30 and rainfall > 5:
        advice.append("🌱 Ideal planting conditions — Soil moisture is sufficient.")
    if temp < 15:
        advice.append("❄️ Low temperature — Delay planting due to poor germination.")
    if not advice:
        advice.append("🌾 Weather conditions are stable for normal farming activities.")
    return advice


# ----------------------------------------------------
# UI Section
# ----------------------------------------------------
st.markdown("""
<div class="center-text">
    <h1>🌱 Smart Farming Advisory App</h1>
    <p style="font-size:18px; color:#666;">
        Get personalized crop guidance based on live weather insights.
    </p>
</div>
""", unsafe_allow_html=True)

# Input Box Container
with st.container():
    city = st.text_input("📍 Enter your city or town:", value="Muranga", help="Enter any valid global city name.")

# Main Button
st.button("Get Farming Advice")

# Logic Execution
if st.button("Get Farming Advice"):
    with st.spinner("Fetching weather data..."):
        try:
            # Weather Retrieval
            weather = get_weather_data(city)

            # Prediction
            features = np.array([[weather['max_temp'], weather['humidity'], weather['rainfall']]])
            predicted_temp = round(model.predict(features)[0], 1)

            advice_list = generate_advice(predicted_temp, weather['humidity'], weather['rainfall'])

            # --- Weather Card ---
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.markdown("<div class='section-title'>🌦️ Current Weather</div>", unsafe_allow_html=True)
            st.write(f"**Temperature:** {weather['max_temp']}°C")
            st.write(f"**Humidity:** {weather['humidity']}%")
            st.write(f"**Rainfall (1 hr):** {weather['rainfall']} mm")
            st.markdown("</div>", unsafe_allow_html=True)

            # --- Prediction Card ---
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.markdown("<div class='section-title'>🔮 Predicted Temperature</div>", unsafe_allow_html=True)
            st.write(f"**Expected Temperature:** {predicted_temp}°C")
            st.markdown("</div>", unsafe_allow_html=True)

            # --- Advice Card ---
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.markdown("<div class='section-title'>🌾 Farming Advice</div>", unsafe_allow_html=True)
            for tip in advice_list:
                st.write(f"- {tip}")
            st.markdown("</div>", unsafe_allow_html=True)

        except Exception as e:
            st.error(f"⚠️ Error: {e}")








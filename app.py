import streamlit as st
import requests
import joblib
import numpy as np
import os

# Load model
MODEL_PATH = os.path.join(os.path.dirname(__file__), "temp_model.pkl")
model = joblib.load(MODEL_PATH)

API_KEY = "ebab3d399da1c49079f35277706aaf7a"

# --------------------------
# Weather API Function
# --------------------------
def get_weather_data(city):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    
    if response.status_code != 200:
        raise ValueError("City not found or API request failed.")
    
    data = response.json()
    return {
        'max_temp': data["main"]["temp_max"],
        'humidity': data['main']['humidity'],
        'rainfall': data.get('rain', {}).get('1h', 0)
    }

# --------------------------
# Advice Generator
# --------------------------
def generate_advice(temp, humidity, rainfall):
    advice = []

    if temp > 30:
        advice.append("🔥 **High temperature** — Consider mulching (matandazo).")
    if humidity > 80:
        advice.append("💧 **High humidity** — Increased risk of fungal diseases.")
    if rainfall < 5:
        advice.append("🚿 **Low rainfall** — Irrigation is recommended.")
    if rainfall > 20:
        advice.append("🌧️ **Heavy rainfall** — Risk of waterlogging.")
    if 20 <= temp <= 30 and rainfall > 5:
        advice.append("🌱 **Ideal planting conditions** — Soil moisture is sufficient.")
    if temp < 15:
        advice.append("❄️ **Low temperature** — Delay planting due to poor germination risk.")

    if not advice:
        advice.append("🌾 Conditions are stable for normal farming activities.")

    return advice

# --------------------------
# UI Design
# --------------------------
st.set_page_config(page_title="Smart Farming Advisory", page_icon="🌱", layout="centered")

# Header Section
st.markdown(
    """
    <div style="text-align: center;">
        <h1>🌱 Smart Farming Advisory App</h1>
        <p style="font-size:18px; color:#555;">
            Get real-time farming recommendations based on your local weather.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

# Input
city = st.text_input("📍 Enter your city or town:", value="Muranga")

st.write("")

# Action Button
if st.button("Get Farming Advice"):
    with st.spinner("Fetching weather data..."):
        try:
            # Fetch weather
            weather = get_weather_data(city)

            # Prepare input features
            features = np.array([[weather['max_temp'], weather['humidity'], weather['rainfall']]])
            predicted_temp = round(model.predict(features)[0], 1)

            # Generate advice
            advice_list = generate_advice(predicted_temp, weather['humidity'], weather['rainfall'])

            # -----------------------------------
            # Display Weather Section
            # -----------------------------------
            st.markdown("### 🌦️ Current Weather")
            st.info(
                f"""
                **Temperature:** {weather['max_temp']}°C  
                **Humidity:** {weather['humidity']}%  
                **Rainfall (1 hr):** {weather['rainfall']} mm  
                """
            )

            # -----------------------------------
            # Prediction Section
            # -----------------------------------
            st.markdown("### 🔮 Predicted Temperature")
            st.success(f"**{predicted_temp}°C** expected.")

            # -----------------------------------
            # Advice Section
            # -----------------------------------
            st.markdown("### 🌾 Farming Advice")
            for tip in advice_list:
                st.markdown(f"- {tip}")

        except Exception as e:
            st.error(f"⚠️ Error: {e}")



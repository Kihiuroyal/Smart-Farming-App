import streamlit as st
import requests
import joblib
import numpy as np
import os

# ----------------------------------------------------
# Page Configuration
# ----------------------------------------------------
st.set_page_config(
    page_title="Smart Farming Advisory",
    page_icon="🌱",
    layout="centered"
)

# ----------------------------------------------------
# Custom CSS Styling
# ----------------------------------------------------
st.markdown("""
<style>

/* Background */
body {
    background-color: #f5faf4;
}

/* Full-width beautiful button */
div.stButton > button {
    width: 100%;
    background-color: #4CAF50 !important;
    color: white !important;
    padding: 15px 0px;
    font-size: 20px;
    border-radius: 10px;
    border: none;
}

/* Card Style */
.big-card {
    padding: 25px !important;
    border-radius: 12px !important;
    background-color: #e7f4e4 !important; 
    border: 1px solid #b5d8b0 !important;
    margin-bottom: 20px;
}

/* Larger text inside cards */
.big-card p, .big-card strong {
    font-size: 18px !important;
}

/* Center heading */
.center-text {
    text-align: center;
}

</style>
""", unsafe_allow_html=True)

# ----------------------------------------------------
# Load ML Model
# ----------------------------------------------------
MODEL_PATH = os.path.join(os.path.dirname(__file__), "temp_model.pkl")
model = joblib.load(MODEL_PATH)

API_KEY = "YOUR_OPENWEATHERMAP_API_KEY"   # Replace with your key


# ----------------------------------------------------
# Weather Fetching Function
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
# Generate Farming Advice
# ----------------------------------------------------
def generate_advice(temp, humidity, rainfall):
    advice = []

    if temp > 30:
        advice.append("🔥 **High temperature** — Consider mulching to retain soil moisture.")
    if humidity > 80:
        advice.append("💧 **High humidity** — Increased risk of fungal diseases.")
    if rainfall < 5:
        advice.append("🚿 **Low rainfall** — Irrigation is recommended.")
    if rainfall > 20:
        advice.append("🌧️ **Heavy rainfall** — Risk of waterlogging.")
    if 20 <= temp <= 30 and rainfall > 5:
        advice.append("🌱 **Ideal planting conditions** — Soil moisture is sufficient.")
    if temp < 15:
        advice.append("❄️ **Low temperature** — Consider delaying planting.")

    if not advice:
        advice.append("🌾 Weather conditions are stable for normal farming activities.")

    return advice


# ----------------------------------------------------
# UI Content
# ----------------------------------------------------
st.markdown("""
<div class="center-text">
    <h1>🌱 Smart Farming Advisory App</h1>
    <p style="font-size:18px; color:#555;">
        Get real-time farming recommendations based on live weather conditions.
    </p>
</div>
""", unsafe_allow_html=True)

# Input Field
city = st.text_input("📍 Enter your city or town:", value="Muranga")

# Button
if st.button("Get Farming Advice"):
    with st.spinner("Fetching weather data..."):
        try:
            weather = get_weather_data(city)

            # Predict temperature
            features = np.array([[weather['max_temp'], weather['humidity'], weather['rainfall']]])
            predicted_temp = round(model.predict(features)[0], 1)

            advice_list = generate_advice(predicted_temp, weather['humidity'], weather['rainfall'])

            # -----------------------
            # Current Weather Card
            # -----------------------
            st.markdown(
                f"""
                <div class="big-card">
                    <h3>🌦️ Current Weather</h3>
                    <p><strong>Temperature:</strong> {weather['max_temp']}°C</p>
                    <p><strong>Humidity:</strong> {weather['humidity']}%</p>
                    <p><strong>Rainfall (1 hr):</strong> {weather['rainfall']} mm</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

            # -----------------------
            # Predicted Temperature Card
            # -----------------------
            st.markdown(
                f"""
                <div class="big-card">
                    <h3>🔮 Temperature Prediction</h3>
                    <p><strong>Expected Temperature:</strong> {predicted_temp}°C</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

            # -----------------------
            # Advice Section
            # -----------------------
            st.markdown("### 🌾 Farming Advice")
            for tip in advice_list:
                st.markdown(f"- {tip}")

        except Exception as e:
            st.error(f"⚠️ Error: {e}")


        except Exception as e:
            st.error(f"⚠️ Error: {e}")




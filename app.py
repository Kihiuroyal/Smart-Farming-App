import streamlit as st
import requests
import joblib
import numpy as np
import os

# =========================
# Load Model
# =========================
MODEL_PATH = os.path.join(os.path.dirname(__file__), "temp_model.pkl")
model = joblib.load(MODEL_PATH)

API_KEY = "ebab3d399da1c49079f35277706aaf7a"


# =========================
# Weather Fetch Function
# =========================
def get_weather(city):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    r = requests.get(url)

    if r.status_code != 200:
        raise ValueError("City not found")

    data = r.json()
    return {
        "max_temp": data["main"]["temp_max"],
        "humidity": data["main"]["humidity"],
        "rainfall": data.get("rain", {}).get("1h", 0)
    }


# =========================
# Styling to mimic your HTML layout
# =========================

st.set_page_config(page_title="Smart Crop Advisory", page_icon="🌱", layout="centered")

st.markdown("""
<style>

:root {
    --primary: #2e7d32;
    --primary-light: #4caf50;
    --primary-dark: #1b5e20;
    --accent: #ffab00;
    --text: #263238;
    --light-text: #78909c;
    --background: #f8f9fa;
    --card-bg: #ffffff;
    --radius: 12px;
    --shadow: 0 4px 8px rgba(0,0,0,0.08);
}

body { background: var(--background); }

.container {
    max-width: 750px;
    margin: auto;
}

h1 {
    color: var(--primary-dark);
    text-align: center;
    font-size: 2.5rem;
    margin-bottom: -10px;
}

.tagline {
    text-align: center;
    color: var(--light-text);
    font-size: 1.1rem;
    margin-bottom: 30px;
}

.input-card {
    background: var(--card-bg);
    padding: 22px;
    border-radius: var(--radius);
    box-shadow: var(--shadow);
    margin-bottom: 30px;
}

label { font-weight: 600; color: var(--primary-dark); }

input {
    padding: 12px;
    width: 100%;
    border-radius: 8px;
    border: 2px solid #d9d9d9;
    font-size: 1rem;
    margin-top: 8px;
}

button[kind="primaryBtn"] {
    width: 100%;
    background: var(--primary);
    color: white !important;
    border-radius: 10px;
    padding: 14px;
    font-size: 1.05rem;
    margin-top: 14px;
}

button[kind="primaryBtn"]:hover { background: var(--primary-dark); }

/* Weather Cards */
.weather-grid {
    display: grid;
    grid-template-columns: repeat(2,1fr);
    gap: 14px;
}

.card {
    background: rgba(46,125,50,0.08);
    text-align: center;
    padding: 16px;
    border-radius: 10px;
}

.card-value { font-size: 1.8rem; color: var(--primary-dark); font-weight: 700; }
.card-label { color: var(--light-text); font-size: .85rem; }

/* Advice Section */
.advice-box {
    margin-top: 25px;
}

.advice-item {
    border-bottom: 1px solid #e3e3e3;
    padding: 12px 0;
    display: flex;
    gap: 8px;
}
.advice-item:last-child { border-bottom:none; }
.advice-icon { color: var(--accent); font-weight:bold; }

footer { text-align:center; margin-top:30px; color:var(--light-text); font-size:.9rem; }

</style>
""", unsafe_allow_html=True)

# =========================
# UI Layout
# =========================
st.markdown("<div class='container'>", unsafe_allow_html=True)

st.markdown("## 🌱 Smart Crop Advisory System")
st.markdown("<p class='tagline'>Get personalized recommendations based on your local weather</p>", unsafe_allow_html=True)

st.markdown("<div class='input-card'>", unsafe_allow_html=True)
city = st.text_input("Enter your location", "Nairobi")

if st.button("Get Crop Advice", key="btn", type="primary", help="Click to fetch weather & receive farm guidance"):
    try:
        weather = get_weather(city)

        # ML Prediction
        features = np.array([[weather['max_temp'], weather['humidity'], weather['rainfall']]])
        predicted_temp = round(float(model.predict(features)[0]), 1)

        st.success(f"📍 Weather in **{city.title()}**")

        st.markdown("""<div class='weather-grid'>""", unsafe_allow_html=True)

        st.markdown(f"""
            <div class='card'>
                <div class='card-value'>{weather['max_temp']}°C</div>
                <div class='card-label'>Maximum Temperature</div>
            </div>
            <div class='card'>
                <div class='card-value'>{weather['humidity']}%</div>
                <div class='card-label'>Humidity</div>
            </div>
            <div class='card'>
                <div class='card-value'>{weather['rainfall']} mm</div>
                <div class='card-label'>Rainfall (1hr)</div>
            </div>
            <div class='card'>
                <div class='card-value'>{predicted_temp}°C</div>
                <div class='card-label'>Predicted Avg Temp</div>
            </div>
        """, unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

        # =========================
        # Farming Advice Output
        # =========================

        st.markdown("<h3>🌾 Farming Recommendations</h3>", unsafe_allow_html=True)

        from textwrap import dedent
        advice = []

        if weather["humidity"] > 80:
            advice.append("💧 High humidity — Increased risk of fungal diseases; monitor crops.")
        if weather["rainfall"] < 5:
            advice.append("🚿 Low rainfall — Consider supplemental irrigation.")
        if weather["max_temp"] < 16:
            advice.append("❄️ Low temperature — Delay planting; germination may be poor.")

        if len(advice) == 0:
            advice.append("🌱 Conditions suitable — You can plant normally.")

        st.markdown("<div class='advice-box'>", unsafe_allow_html=True)

        for tip in advice:
            st.markdown(
                f"<div class='advice-item'><span class='advice-icon'>✓</span><div>{tip}</div></div>",
                unsafe_allow_html=True
            )

        st.markdown("</div>", unsafe_allow_html=True)

    except Exception as e:
        st.error(f"⚠ Error: {e}")

st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<footer>Smart Crop Advisory © 2025 | Data-driven farming for a better future</footer>",
            unsafe_allow_html=True)















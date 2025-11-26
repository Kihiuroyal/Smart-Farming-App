# app.py (fixed rendering)
import streamlit as st
import requests
import joblib
import numpy as np
import os
import html
import math
import st                    # keep imports explicit if needed

# ----------------------
# Config
# ----------------------
st.set_page_config(page_title="Smart Crop Advisory system", page_icon="🌱", layout="centered")

# Load model (adjust path if necessary)
MODEL_PATH = os.path.join(os.path.dirname(__file__), "temp_model.pkl")
model = joblib.load(MODEL_PATH)

API_KEY = "ebab3d399da1c49079f35277706aaf7a"

# ----------------------
# CSS (same as before)
# ----------------------
CSS = """
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
    --border-radius: 12px;
    --shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

* { margin: 0; padding: 0; box-sizing: border-box; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }

body { background-color: var(--background); color: var(--text); line-height: 1.6; padding: 0; }

.container { max-width: 800px; margin: 16px auto; padding: 20px; }

header { text-align: center; margin-bottom: 18px; }

h1 { color: var(--primary-dark); font-size: 2.1rem; margin-bottom: 8px; }

.tagline { color: var(--light-text); font-size: 1rem; }

.search-container { background-color: var(--card-bg); padding: 20px; border-radius: var(--border-radius); box-shadow: var(--shadow); margin-bottom: 22px; }

.form-label { font-weight: 600; margin-bottom: 8px; color: var(--primary-dark); display: block; font-size: 0.95rem; }

.input-text { padding: 12px 15px; border: 2px solid #e0e0e0; border-radius: 8px; font-size: 1rem; transition: all 0.3s ease; width: 100%; margin-bottom: 12px; }

.input-text:focus { border-color: var(--primary); outline: none; box-shadow: 0 0 0 3px rgba(76, 175, 80, 0.12); }

.btn-primary { background-color: var(--primary); color: white; border: none; padding: 12px 16px; border-radius: 8px; font-size: 1rem; font-weight: 600; cursor: pointer; transition: all 0.22s ease; display: inline-flex; align-items: center; justify-content: center; gap: 8px; width: 100%; }

.btn-primary:hover { background-color: var(--primary-dark); transform: translateY(-2px); }

.result { background-color: var(--card-bg); border-radius: var(--border-radius); box-shadow: var(--shadow); padding: 20px; animation: fadeIn 0.45s ease; margin-bottom: 16px; }

@keyframes fadeIn { from { opacity: 0; transform: translateY(12px); } to { opacity: 1; transform: translateY(0); } }

.result h2 { color: var(--primary-dark); margin-bottom: 12px; display: flex; align-items: center; gap: 8px; }

.weather-stats { display: grid; grid-template-columns: repeat(auto-fit, minmax(160px, 1fr)); gap: 12px; margin-bottom: 18px; }

.stat-card { background-color: rgba(46, 125, 50, 0.07); padding: 12px; border-radius: 8px; text-align: center; }

.stat-value { font-size: 1.6rem; font-weight: 700; color: var(--primary-dark); margin: 6px 0; }

.stat-label { color: var(--light-text); font-size: 0.9rem; }

h3 { color: var(--primary-dark); margin: 16px 0 10px; padding-bottom: 6px; border-bottom: 2px solid var(--primary-light); }

.advice-list { list-style: none; padding-left: 0; }

.advice-item { padding: 10px 0; border-bottom: 1px solid #eaeaea; display: flex; align-items: flex-start; gap: 10px; }

.advice-item:last-child { border-bottom: none; }

.advice-icon { color: var(--accent); flex-shrink: 0; margin-top: 3px; }

footer { text-align: center; margin-top: 18px; color: var(--light-text); font-size: 0.9rem; }

@media (max-width: 600px) { h1 { font-size: 1.6rem; } .container { padding: 12px; } }
</style>
"""

# ----------------------
# Helper functions
# ----------------------
def get_weather_data(city):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={requests.utils.quote(city)}&appid={API_KEY}&units=metric"
    resp = requests.get(url, timeout=8)
    if resp.status_code != 200:
        raise ValueError("City not found or API request failed.")
    data = resp.json()
    return {
        "max_temp": data["main"]["temp_max"],
        "humidity": data["main"]["humidity"],
        "rainfall": data.get("rain", {}).get("1h", 0)
    }

def generate_advice(temp, humidity, rainfall):
    advice = []
    if temp > 30:
        advice.append("🔥 High temperature — Consider mulching (retain soil moisture).")
    if humidity > 80:
        advice.append("💧 High humidity — Increased risk of fungal diseases; monitor crops.")
    if rainfall < 5:
        advice.append("🚿 Low rainfall — Consider supplemental irrigation.")
    if rainfall > 20:
        advice.append("🌧️ Heavy rainfall — Risk of waterlogging; check drainage.")
    if 20 <= temp <= 30 and rainfall > 5:
        advice.append("🌱 Ideal planting conditions — Soil moisture looks sufficient.")
    if temp < 15:
        advice.append("❄️ Low temperature — Delay planting; germination may be poor.")
    if not advice:
        advice.append("🌾 Conditions stable — Normal farming activities are OK.")
    return advice

# ----------------------
# Page header + form
# ----------------------
st.markdown(CSS, unsafe_allow_html=True)

# header block
header_html = """
<div class="container">
  <header>
    <h1>🌱 Smart Crop Advisory System</h1>
    <p class="tagline">Get personalized farming recommendations based on local weather data</p>
  </header>
"""
st.markdown(header_html, unsafe_allow_html=True)

with st.form(key="city_form"):
    st.markdown('<div class="search-container">', unsafe_allow_html=True)
    st.markdown('<label class="form-label" for="city">Enter your location</label>', unsafe_allow_html=True)
    city_input = st.text_input(" ", value="Nairobi", key="city_input", placeholder="e.g. Nairobi")
    submit_btn = st.form_submit_button(label="Get Crop Advice")
    st.markdown('</div>', unsafe_allow_html=True)

# ----------------------
# On submit: fetch and render entire HTML with components.html
# ----------------------
if submit_btn:
    city = (city_input or "").strip()
    try:
        with st.spinner("Retrieving live weather & advice..."):
            weather = get_weather_data(city)
            # model predict
            features = np.array([[weather["max_temp"], weather["humidity"], weather["rainfall"]]])
            predicted_temp = model.predict(features)[0]
            # ensure nice formatting (one decimal)
            predicted_display = f"{predicted_temp:.1f}"
            advice = generate_advice(float(predicted_display), weather["humidity"], weather["rainfall"])

        # Build full HTML (CSS already included above in the page, but we produce a self-contained block for consistent rendering)
        result_html = f"""
        {CSS}
        <div class="container">
          <header>
            <h1>🌱 Smart Crop Advisory System</h1>
            <p class="tagline">Get personalized farming recommendations based on local weather data</p>
          </header>

          <div class="result">
            <h2>
              <svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" fill="currentColor" viewBox="0 0 16 16" style="margin-right:8px;">
                <path d="M7 16a4 4 0 0 1-4-4V5a1 1 0 0 1 1-1h1V1a1 1 0 0 1 2 0v3h1a1 1 0 0 1 1 1v7a4 4 0 0 1-4 4zm3-9H6v5a3 3 0 0 0 6 0V7h-2z"/>
              </svg>
              Weather in {html.escape(city)}
            </h2>

            <div class="weather-stats">
              <div class="stat-card">
                <div class="stat-value">{weather['max_temp']:.1f}°C</div>
                <div class="stat-label">Maximum Temperature</div>
              </div>
              <div class="stat-card">
                <div class="stat-value">{weather['humidity']}%</div>
                <div class="stat-label">Humidity</div>
              </div>
              <div class="stat-card">
                <div class="stat-value">{weather['rainfall']} mm</div>
                <div class="stat-label">Rainfall (1 hr)</div>
              </div>
              <div class="stat-card">
                <div class="stat-value">{predicted_display}°C</div>
                <div class="stat-label">Predicted Avg Temp</div>
              </div>
            </div>

            <h3>Farming Recommendations</h3>
            <ul class="advice-list">
        """

        for item in advice:
            safe_item = html.escape(item)
            result_html += f"""
                <li class="advice-item">
                  <span class="advice-icon">✓</span>
                  <div>{safe_item}</div>
                </li>
            """

        result_html += """
            </ul>
          </div>

          <footer>
            <p>Smart Crop Advisory &copy; 2025 | Helping farmers make data-driven decisions</p>
          </footer>
        </div>

        <script>
        (function() {
            const elements = document.querySelectorAll('.container > *');
            elements.forEach((element, index) => {
                element.style.opacity = '0';
                element.style.transform = 'translateY(20px)';
                element.style.transition = 'opacity 0.45s ease, transform 0.45s ease';
                setTimeout(() => {
                    element.style.opacity = '1';
                    element.style.transform = 'translateY(0)';
                }, 80 + (index * 80));
            });
        })();
        </script>
        """

        # Render the whole HTML content using st.components.v1.html so it's actually interpreted by the browser
        # Height can be adjusted; using 700 to accomodate result content
        st.components.v1.html(result_html, height=700, scrolling=True)

    except Exception as e:
        st.error(f"⚠️ Error: {e}")

else:
    # show the footer when no result
    st.markdown("""
      <footer>
        <p>Smart Crop Advisory &copy; 2025 | Helping farmers make data-driven decisions</p>
      </footer>
    </div>
    """, unsafe_allow_html=True)













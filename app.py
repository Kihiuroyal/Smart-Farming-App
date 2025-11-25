import streamlit as st
import requests
import joblib
import numpy as np
import os

# Ensure we load the model from the current directory
MODEL_PATH = os.path.join(os.path.dirname(__file__), "temp_model.pkl")
model = joblib.load(MODEL_PATH)

API_KEY = "ebab3d399da1c49079f35277706aaf7a"

def get_weather_data(city):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    data = response.json()
    return {
        'max_temp': data["main"]["temp_max"],
        'humidity': data['main']['humidity'],
        'rainfall': data.get('rain', {}).get('1h', 0)
    }

def generate_advice(temp, humidity, rainfall):
    advice = []
    if temp > 30:
        advice.append("High temperature, consider mulching (Joto kali, fikiria kutumia matandazo)")
    if humidity > 80:
        advice.append("High humidity, risk of fungal diseases (Unyevu mwingi, kuna hatari ya magonjwa ya kuvu).")
    if rainfall < 5:
        advice.append("Low rainfall, consider irrigation (Mvua ni kidogo, fikiria kumwagilia maji).")
    if rainfall > 20:
        advice.append("Heavy rain, risk of waterlogging (Mvua kubwa, kuna hatari ya mafuriko ya mashambani).")
    if 20 <= temp <= 30 and rainfall > 5:
        advice.append("Ideal conditions for planting, Soil moisture is sufficient (Hali nzuri kwa kupanda, unyevu wa udongo unatosha).")
    elif temp < 15:
        advice.append("Low temperatures, Delay planting as seed germination may be poor (Joto la chini, chelewesha kupanda kwani mbegu zinaweza zisichipue vizuri).")
    return advice

# Streamlit UI
st.title("🌱 Smart Farming Advisory App")

city = st.text_input("Enter your city", value="Muranga")

if st.button("Get Advice"):
    try:
        weather = get_weather_data(city)
        features = np.array([[weather['max_temp'], weather['humidity'], weather['rainfall']]])
        predicted_temp = model.predict(features)[0]
        predicted_temp = round(predicted_temp, 1)

        advice = generate_advice(predicted_temp, weather['humidity'], weather['rainfall'])

        st.subheader(f"Weather in {city}")
        st.write(weather)

        st.subheader("Predicted Temperature")
        st.write(f"{predicted_temp} °C")

        st.subheader("Advice for Farmers")
        for tip in advice:
            st.write("- " + tip)
    except Exception as e:
        st.error(f"Error fetching data: {e}")

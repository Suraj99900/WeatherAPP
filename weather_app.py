import streamlit as st
import requests
import json
from datetime import datetime

# OpenWeatherMap API Key (Replace with your actual API key)
OPENWEATHER_API_KEY = "2c69c329f98dee919d2095e846d11ba1"

# Google Gemini API Key (Replace with your actual API key)
GEMINI_API_KEY = "AIzaSyBku97zn0rnClmtlspJ4wr27e9uuxQF4fc"

# Function to get weather data from OpenWeatherMap API
def get_weather_data(city, api_key):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    data = response.json()
    
    if data["cod"] == "404":
        return None  # City not found
    else:
        return data

# Function to generate AI-based weather insights using Google Gemini API
# Function to generate AI-based weather insights using Google Gemini API
def get_ai_weather_insights(weather_data):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
    
    # Prepare input text for AI model
    prompt_text = f"""
    The weather in {weather_data['name']} is currently {weather_data['weather'][0]['description']}. 
    The temperature is {weather_data['main']['temp']}°C with a humidity of {weather_data['main']['humidity']}%. 
    The wind speed is {weather_data['wind']['speed']} m/s.

    Provide a visually appealing weather summary using bullet points, emojis, and structured categories.
    
    **🌡️ Temperature:**  
    - Current: {weather_data['main']['temp']}°C  
    - Feels like: {weather_data['main'].get('feels_like', 'N/A')}°C  
    - Max: {weather_data['main'].get('temp_max', 'N/A')}°C | Min: {weather_data['main'].get('temp_min', 'N/A')}°C  

    **💨 Wind:**  
    - Speed: {weather_data['wind']['speed']} m/s  
    - Direction: {weather_data['wind'].get('deg', 'N/A')}°  

    **🌦️ Weather Conditions:**  
    - {weather_data['weather'][0]['description'].capitalize()}  
    - Pressure: {weather_data['main']['pressure']} hPa  
    - Humidity: {weather_data['main']['humidity']}%  

    **🕒 Sunrise & Sunset:**  
    - 🌅 Sunrise: {datetime.utcfromtimestamp(weather_data['sys']['sunrise']).strftime('%H:%M:%S')}  
    - 🌇 Sunset: {datetime.utcfromtimestamp(weather_data['sys']['sunset']).strftime('%H:%M:%S')}  

    **📢 Recommendations:**  
    - ☀️ If it's sunny, wear sunglasses and stay hydrated!  
    - ☔ If it's rainy, carry an umbrella and wear waterproof shoes.  
    - 🏖️ If it's hot, avoid direct sun exposure during peak hours.  
    - ❄️ If it's cold, wear warm clothing and keep yourself cozy.  
    """

    payload = {
        "contents": [{"parts": [{"text": prompt_text}]}]
    }
    
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, headers=headers, json=payload)
    
    if response.status_code == 200:
        ai_response = response.json()
        return ai_response["candidates"][0]["content"]["parts"][0]["text"]
    else:
        return "AI insights are currently unavailable."


# Streamlit Application
def app():
    st.set_page_config(page_title="Weather AI App", page_icon="🌤️", layout="wide")
    st.title("🌤️ AI-Powered Weather Application")

    # Input for city name
    city = st.text_input("Enter city name", "Pune")

    # Search button
    if st.button("Search Weather"):
        if city:
            # Fetch weather data
            weather_data = get_weather_data(city, OPENWEATHER_API_KEY)
            
            if weather_data is None:
                st.error("City not found! Please try again.")
            else:
                # Create two columns for layout
                col1, col2 = st.columns(2)

                # Weather Details
                with col1:
                    st.subheader(f"🌍 Weather in {city}")
                    st.image(f"http://openweathermap.org/img/wn/{weather_data['weather'][0]['icon']}@2x.png")
                    st.write(f"**Temperature:** {weather_data['main']['temp']}°C 🌡️")
                    st.write(f"**Weather:** {weather_data['weather'][0]['description'].capitalize()} 🌤️")
                    st.write(f"**Humidity:** {weather_data['main']['humidity']}% 💧")
                    st.write(f"**Pressure:** {weather_data['main']['pressure']} hPa ☁️")
                    st.write(f"**Wind Speed:** {weather_data['wind']['speed']} m/s 🌬️")
                    st.write(f"**Sunrise:** {datetime.utcfromtimestamp(weather_data['sys']['sunrise']).strftime('%H:%M:%S')} 🌅")
                    st.write(f"**Sunset:** {datetime.utcfromtimestamp(weather_data['sys']['sunset']).strftime('%H:%M:%S')} 🌇")

                # AI Weather Insights
                with col2:
                    st.subheader("🤖 AI Weather Insights")
                    with st.spinner("Generating AI insights..."):
                        ai_insights = get_ai_weather_insights(weather_data)
                    st.write(ai_insights)

        else:
            st.error("Please enter a city name.")

# Run the Streamlit app
if __name__ == "__main__":
    app()

import streamlit as st
import requests
from datetime import datetime

# Function to get weather data from OpenWeatherMap API
def get_weather_data(city, api_key):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    data = response.json()
    
    if data["cod"] == "404":
        return None  # City not found
    else:
        return data

# Streamlit application
def app():
    st.set_page_config(page_title="Weather Data App", page_icon="🌤️", layout="wide")
    st.title("🌤️ Weather Data Application")

    # Input for city name
    city = st.text_input("Enter city name", "London")

    # Search button
    if st.button("Search Weather"):
        if city:
            # OpenWeatherMap API key (replace with your actual API key)
            api_key = "2c69c329f98dee919d2095e846d11ba1"  # Replace with your API key

            # Fetch weather data
            weather_data = get_weather_data(city, api_key)
            
            if weather_data is None:
                st.error("City not found! Please try again.")
            else:
                # Display weather data with icons and better formatting
                st.write(f"**Weather in {city}:**")
                
                # Unicode characters for weather data
                st.markdown(f"**Temperature**: {weather_data['main']['temp']}°C 🌡️")
                st.markdown(f"**Weather**: {weather_data['weather'][0]['description'].capitalize()} 🌤️")
                st.markdown(f"**Humidity**: {weather_data['main']['humidity']}% 💧")
                st.markdown(f"**Pressure**: {weather_data['main']['pressure']} hPa ☁️")
                st.markdown(f"**Wind Speed**: {weather_data['wind']['speed']} m/s 🌬️")
                
                # Sunrise and Sunset (convert from Unix timestamp to readable format)
                sunrise = datetime.utcfromtimestamp(weather_data['sys']['sunrise']).strftime('%H:%M:%S')
                sunset = datetime.utcfromtimestamp(weather_data['sys']['sunset']).strftime('%H:%M:%S')
                st.markdown(f"**Sunrise**: {sunrise} 🌅")
                st.markdown(f"**Sunset**: {sunset} 🌇")

                # Optionally, display weather icon from OpenWeatherMap
                icon_code = weather_data['weather'][0]['icon']
                icon_url = f"http://openweathermap.org/img/wn/{icon_code}@2x.png"
                st.image(icon_url, width=100)
        else:
            st.error("Please enter a city name.")

# Run the Streamlit app
if __name__ == "__main__":
    app()

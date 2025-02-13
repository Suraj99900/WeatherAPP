import requests
from datetime import datetime
import gradio as gr

# Function to get weather data from OpenWeatherMap API
def get_weather_data(city, api_key):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    data = response.json()
    
    if data["cod"] == "404":
        return None  # City not found
    else:
        return data

# Function to display weather data in Gradio interface
def gradio_weather(city):
    # OpenWeatherMap API key (replace with your actual API key)
    api_key = "2c69c329f98dee919d2095e846d11ba1"  # Replace with your API key

    weather_data = get_weather_data(city, api_key)
    
    if weather_data is None:
        return "City not found! Please try again.", None
    else:
        # Prepare weather data
        temperature = f"**Temperature:** {weather_data['main']['temp']}°C 🌡️"
        description = f"**Weather:** {weather_data['weather'][0]['description'].capitalize()} 🌤️"
        humidity = f"**Humidity:** {weather_data['main']['humidity']}% 💧"
        pressure = f"**Pressure:** {weather_data['main']['pressure']} hPa ☁️"
        wind_speed = f"**Wind Speed:** {weather_data['wind']['speed']} m/s 🌬️"
        
        # Sunrise and Sunset (convert from Unix timestamp to readable format)
        sunrise = datetime.utcfromtimestamp(weather_data['sys']['sunrise']).strftime('%H:%M:%S')
        sunset = datetime.utcfromtimestamp(weather_data['sys']['sunset']).strftime('%H:%M:%S')
        
        sunrise_sunset = f"**Sunrise:** {sunrise} 🌅\n**Sunset:** {sunset} 🌇"
        
        # Weather icon
        icon_code = weather_data['weather'][0]['icon']
        icon_url = f"http://openweathermap.org/img/wn/{icon_code}@2x.png"
        
        # Combine all the data into a nicely formatted string
        weather_info = f"""
        {temperature}
        {description}
        {humidity}
        {pressure}
        {wind_speed}
        {sunrise_sunset}
        """
        
        return weather_info, icon_url

# Gradio interface function
def gradio_app():
    # Gradio interface layout
    with gr.Blocks() as demo:  # Default theme (removes 'huggingface' theme)
        # Title and introduction
        gr.Markdown("# 🌤️ Weather Data Application", elem_id="title")
        gr.Markdown("Welcome to the Weather App! Enter the city name below to get the current weather data.", elem_id="intro")
        
        # User input for city name
        with gr.Row():
            city_input = gr.Textbox(
                label="Enter City Name", 
                placeholder="e.g. Pune", 
                max_lines=1, 
                show_label=True, 
                elem_id="city_input"
            )
        
        # Weather info output area
        with gr.Row():
            with gr.Column(scale=1):
                weather_output = gr.Markdown(
                    label="Weather Information", 
                    elem_id="weather_output"
                )
            with gr.Column(scale=0.5):
                icon_output = gr.Image(
                    type="pil", 
                    height=200, 
                    elem_id="weather_icon"
                )
        
        # Button to trigger the weather data fetch
        fetch_button = gr.Button("Get Weather", elem_id="fetch_button")

        # Define button click behavior
        def update_weather(city):
            weather_output_text, icon_url = gradio_weather(city)
            return gr.update(value=weather_output_text), gr.update(value=icon_url)
        
        fetch_button.click(update_weather, inputs=city_input, outputs=[weather_output, icon_output])
    
    # Launch app with custom styling and responsiveness
    demo.launch()

# Run Gradio app
if __name__ == "__main__":
    gradio_app()

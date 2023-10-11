# Import necessary libraries
import sys  # System-related functions and constants
import requests  # HTTP requests library
from flask import Flask, jsonify, render_template, request  # Flask for web app
from mailjet_rest import Client  # Mailjet API client
from uagents import Agent, Model  # Agent and Model for periodic tasks
from decouple import config

WEATHER_API = config('WEATHER_API')
API_KEY = config('API_KEY')
SECRET_KEY = config('SECRET_KEY')
MAILJET_EMAIL = config('MAILJET_EMAIL')

count = 0
# Initialize Flask app
app = Flask(__name__)

# Create a weather agent
weather_agent = Agent(name="weather_agent", seed="your_secret_seed")

# Define the TemperatureAlert message model
class TemperatureAlert(Model):
    message: str

# Replace with your OpenWeatherMap API key
API_KEY = WEATHER_API
API_ENDPOINT = "https://api.openweathermap.org/data/2.5/weather"

# Initialize the Mailjet client with your API key and secret
mailjet = Client(auth=(API_KEY, SECRET_KEY), version='v3.1')

# Initialize variables to store inputs
stored_inputs = {
    "name": "",
    "email": "",
    "location": "",
    "min_temperature": 0.0,
    "max_temperature": 0.0,
}

# Route to get weather information
@app.route("/get_weather", methods=["GET"])
def get_weather():
    # Get stored input values
    location = stored_inputs["location"]
    temperature = fetch_weather_data(location)
    email = stored_inputs.get("email", "")
    min_temperature = stored_inputs["min_temperature"]
    max_temperature = stored_inputs["max_temperature"]
    
    global count 
    if count>0:
        sys.exit(1)

    if temperature is not None:
        # Check if temperature is below the minimum threshold
        if min_temperature >= temperature:
            weather_data = f"The temperature in {location} is {temperature}°C, which is below the minimum threshold temperature value."
            response_message = f"The temperature in {location} is {temperature}°C, which is below the minimum threshold temperature value."
            send_email(email, response_message)  # Send email alert
            count += 1
        # Check if temperature is above the maximum threshold
        elif max_temperature <= temperature:
            weather_data = f"The temperature in {location} is {temperature}°C, which is above the maximum threshold temperature value."
            response_message = f"The temperature in {location} is {temperature}°C, which is above the maximum threshold temperature value."
            send_email(email, response_message)  # Send email alert
            count += 1
        else:
            weather_data = f"The temperature in {location} is {temperature}°C, which is within the specified range of {min_temperature}°C to {max_temperature}°C."
    else:
        weather_data = f"Sorry, I couldn't retrieve the temperature for {location}."
    return jsonify({"weather_data": weather_data})

# Route to display weather information on a web page
@app.route("/weather", methods=["GET"])
def weather():
    name = stored_inputs.get("name", "")
    email = stored_inputs.get("email", "")
    location = stored_inputs["location"]
    min_temperature = stored_inputs["min_temperature"]
    max_temperature = stored_inputs["max_temperature"]

    temperature = fetch_weather_data(location)
    if temperature is not None:
        # Check if temperature is below the minimum threshold
        if min_temperature >= temperature:
            temperature_status = f"The temperature in {location} is {temperature}°C, which is below the minimum threshold temperature value."
            response_message = f"The temperature in {location} is {temperature}°C, which is below the minimum threshold temperature value."
        # Check if temperature is above the maximum threshold
        elif max_temperature <= temperature:
            temperature_status = f"The temperature in {location} is {temperature}°C, which is above the maximum threshold temperature value."
            response_message = f"The temperature in {location} is {temperature}°C, which is above the maximum threshold temperature value."
        else:
            temperature_status = f"The temperature in {location} is {temperature}°C, which is within the specified range of {min_temperature}°C to {max_temperature}°C."
    else:
        temperature_status = f"Sorry, I couldn't retrieve the temperature for {location}."

    return render_template("weather.html", weather_data=temperature_status)

# Periodically check the temperature using the weather_agent
@weather_agent.on_interval(period=120)  # Check every 6 minutes (360 seconds)
async def check_temperature():
    global stored_inputs

    # Get stored inputs or ask for new inputs if they are empty
    name = stored_inputs.get("name", "")
    email = stored_inputs.get("email", "")
    location = stored_inputs.get("location", "")
    min_temperature = stored_inputs.get("min_temperature", 0.0)
    max_temperature = stored_inputs.get("max_temperature", 0.0)

    if not name:
        name = input("Enter your name: ")
        stored_inputs["name"] = name

    if not email:
        email = input("Enter your email: ")
        stored_inputs["email"] = email

    if not location:
        location = input("Enter a location: ")
        min_temperature = float(input("Enter Minimum Temperature (in degree Celsius): "))
        max_temperature = float(input("Enter Maximum Temperature (in degree Celsius): "))

        # Store the inputs
        stored_inputs["location"] = location
        stored_inputs["min_temperature"] = min_temperature
        stored_inputs["max_temperature"] = max_temperature

    if name and email and location:
        temperature = fetch_weather_data(location)
        if temperature is not None:
            response_message = f"The temperature in {location} is {temperature}°C"
            # Check if temperature is below the minimum threshold
            if min_temperature >= temperature:
                response_message += f", which is below the minimum threshold temperature value. Sending alert..."
            # Check if temperature is above the maximum threshold
            elif max_temperature <= temperature:
                response_message += f", which is above the maximum threshold temperature value. Sending alert..."
            else:
                response_message += f", which is inside the range of {min_temperature}°C to {max_temperature}°C."
        else:
            response_message = f"Sorry, I couldn't retrieve the temperature for {location}."
        print(response_message)

# Function to fetch weather data from OpenWeatherMap API
def fetch_weather_data(location):
    params = {
        "q": location,
        "appid": API_KEY,
        "units": "metric",  # Use Celsius
    }

    try:
        response = requests.get(API_ENDPOINT, params=params)
        data = response.json()

        if "main" in data and "temp" in data["main"]:
            temperature = data["main"]["temp"]
            return temperature
        else:
            return None
    except Exception as e:
        return None

# Function to send an email using Mailjet
def send_email(email, message):
    data = {
        'Messages': [
            {
                'From': {
                    'Email': MAILJET_EMAIL ,
                    'Name': 'Weather Temperature Alert System'
                },
                'To': [
                    {
                        'Email': email,
                    }
                ],
                'Subject': 'Temperature Alert',
                'TextPart': message,
                'HTMLPart': '<h3>' + message + '</h3>'
            }
        ]
    }
    response = mailjet.send.create(data=data)
    print(f"Email sent to {email}")

# Main route for the index page
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        location = request.form["location"]
        min_temperature = float(request.form["min_temperature"])
        max_temperature = float(request.form["max_temperature"])

        # Store the inputs
        stored_inputs["name"] = name
        stored_inputs["email"] = email
        stored_inputs["location"] = location
        stored_inputs["min_temperature"] = min_temperature
        stored_inputs["max_temperature"] = max_temperature

        # Fetch temperature and prepare the response
        temperature = fetch_weather_data(location)
        if temperature is not None:
            response_message = f"The temperature in {location} is {temperature}°C"
            # Check if temperature is below the minimum threshold
            if min_temperature >= temperature:
                response_message += f", which is below the minimum threshold temperature value. Sending alert..."
            # Check if temperature is above the maximum threshold
            elif max_temperature <= temperature:
                response_message += f", which is above the maximum threshold temperature value. Sending alert..."
            else:
                response_message += f", which is inside the range of {min_temperature}°C to {max_temperature}°C."
                # Temperature is within the specified range, no email is sent
        else:
            response_message = f"Sorry, I couldn't retrieve the temperature for {location}."

        # Return a JSON response with the temperature status
        return render_template("weather.html", weather_data=response_message)
        return jsonify({"temperature_status": response_message})

    name = stored_inputs["name"]
    email = stored_inputs["email"]
    location = stored_inputs["location"]
    min_temperature = stored_inputs["min_temperature"]
    max_temperature = stored_inputs["max_temperature"]

    return render_template("index.html", name=name, email=email, location=location,
                           min_temperature=min_temperature, max_temperature=max_temperature)

# Run the weather_agent
if __name__ == "__main__":
    weather_agent.run()

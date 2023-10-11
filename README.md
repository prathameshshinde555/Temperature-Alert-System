

# Temperature Alert System

The Temperature Alert System is a Python application that checks the current temperature at a specified location and sends an email alert if the temperature falls below or exceeds a certain threshold.
# Demo 

Home Page
![Demo](https://github.com/prathameshshinde555/Temperature-Alert-System/blob/main/images/Demo1.png?raw=true)

Weather Information
![Demo](https://github.com/prathameshshinde555/Temperature-Alert-System/blob/main/images/Demo2.png?raw=true)

## Features

- Periodically checks the temperature at a specified location.
- Sends an email alert if the temperature goes below or exceeds a set threshold.
- User-friendly command-line interface for providing inputs.
- Uses the OpenWeatherMap API to fetch weather data.
- Utilizes the Mailjet API to send email alerts.

## Prerequisites

Before running the Temperature Alert System, make sure you have the following:

- Python 3.x installed on your system.
- The required Python packages installed. You can install them using `pip` and the `requirements.txt` file.

    ```bash
    pip install -r requirements.txt
    ```

- API keys for OpenWeatherMap and Mailjet. Follow the instructions below to obtain these API keys.

## Obtaining API Keys

### OpenWeatherMap API Key

To obtain an API key for the OpenWeatherMap API, follow these steps:

1. Create an OpenWeatherMap Account:
   - If you don't have an account already, visit the OpenWeatherMap website [here](https://openweathermap.org/) and create a free account.

2. Log In to Your OpenWeatherMap Account:
   - Log in to your newly created OpenWeatherMap account using your credentials.

3. Access API Key:
   - After logging in, navigate to your OpenWeatherMap dashboard or account settings. Look for an option related to API access or API keys.

4. Generate a New API Key:
   - In the API access or API keys section, you should find an option to generate a new API key. Click on it to create a new key.

5. Configure API Key Settings (Optional):
   - Some API providers allow you to configure settings for your API key, such as limiting the number of requests or setting usage restrictions. You can configure these settings if needed.

6. Copy Your API Key:
   - Once you have generated the API key, it should be displayed on the screen. Copy this API key to your clipboard. It will typically be a long alphanumeric string.

7. Set Up API Endpoint:
   - The API endpoint for OpenWeatherMap is a URL where you send your API requests. The base URL for OpenWeatherMap's current weather data API is `https://api.openweathermap.org/data/2.5/weather`.

8. Use the API Key in Your Requests:
   - When making requests to the OpenWeatherMap API, you will need to include your API key as a query parameter. The parameter name for the API key is usually "appid." For example, if your API key is "YOUR_API_KEY," you would include it in your requests like this:
     ```
     https://api.openweathermap.org/data/2.5/weather?q=city_name&appid=YOUR_API_KEY
     ```

9. Start Making API Requests:
   - With your API key and the API endpoint, you can start making requests to OpenWeatherMap's API. You can use various query parameters to specify the location, units, and other options for your weather data requests.

10. Handle API Responses:
    - Depending on your application, you will need to parse and handle the JSON responses you receive from the API to extract the weather data you require.

Remember to keep your API key secure and avoid sharing it publicly. Many APIs, including OpenWeatherMap, have usage limits and terms of service that you should review and adhere to while using the API.

### Mailjet API Keys

To obtain API keys (API key and secret key) from Mailjet, follow these stepwise instructions:

1. Create a Mailjet Account:
   - If you don't have a Mailjet account, visit the Mailjet website [here](https://www.mailjet.com/) and create a free account.

2. Log In to Your Mailjet Account:
   - After creating your Mailjet account, log in using your credentials.

3. Access the Mailjet Dashboard:
   - Once logged in, you will be directed to the Mailjet dashboard.

4. Navigate to the "API Keys" Section:
   - In the Mailjet dashboard, look for an option related to API keys. This section may be called "API keys," "Integration," or something similar. Click on it to access your API keys.

5. Create a New API Key Pair:
   - In the API keys section, you should find an option to create a new API key pair (an API key and a secret key). Click on it to generate a new set of keys.

6. Configure API Key Settings (Optional):
   - Some API providers allow you to configure settings for your API key pair, such as limiting the number of requests, setting usage restrictions, or associating it with specific services. You can configure these settings if needed.

7. Copy Your API Key and Secret Key:
   - Once you have generated the API key pair, both the API key and secret key should be displayed on the screen. Copy both of these keys to your clipboard. They will typically be long alphanumeric strings.

8. Store API Keys Securely:
   - It's essential to keep your API keys secure and avoid sharing them publicly. Store them in a safe place, such as environment variables or a secure configuration file, if you're using them in a software application.

9. Use API Keys in Your Integration:
   - To make API requests to Mailjet services, you will need to include your API key and secret key in your requests. The specific method for including these keys will depend on the programming language and libraries you are using.

10. Test Your Integration:
    - With your API keys integrated into your application, you can test sending emails, managing contacts, or performing other tasks using Mailjet's services.

Remember to follow Mailjet's terms of service and usage limits while using their services. Additionally, consider implementing security best practices to protect your API keys from unauthorized access or exposure.

# Running the Flask Application

1. Open a terminal and navigate to the project directory.
2. Make sure your virtual environment is activated (if you created one).
3. Run the Flask application:

```bash
flask run
```
## Working of Functions

### `get_weather` Function:

- This function handles the `/get_weather` route, which is used to fetch weather information based on user inputs.
- It retrieves the user's specified location from `stored_inputs`.
- It fetches the current temperature for the location using the `fetch_weather_data` function.
- It also retrieves the user's email address and temperature thresholds.
- If the temperature is below the minimum threshold, it sends an email alert using the `send_email` function and increments the `count` to prevent further alerts.
- If the temperature is above the maximum threshold, it does the same.
- It returns a JSON response containing weather-related information.

### `weather` Function:

- This function handles the `/weather` route, which is used to display weather information on a web page.
- It retrieves user inputs, such as name, email, location, and temperature thresholds, from `stored_inputs`.
- It fetches the current temperature for the location using the `fetch_weather_data` function.
- Based on the temperature and thresholds, it prepares a `temperature_status` message.
- This message is then rendered on an HTML template using Flask's `render_template` function.

### `check_temperature` Function:

- This function is decorated with `@weather_agent.on_interval(period=120)`, which means it runs periodically every 120 seconds (2 minutes).
- It retrieves or prompts the user for inputs (name, email, location, min_temperature, max_temperature) if they are empty.
- It fetches the current temperature for the location using the `fetch_weather_data` function.
- It prepares a response message based on the temperature and thresholds.
- It prints the response message to the console.

### `fetch_weather_data` Function:

- This function fetches weather data for a given location from the OpenWeatherMap API.
- It constructs an API request with the specified location and API key.
- It makes an HTTP GET request to the API and processes the JSON response.
- If successful, it returns the current temperature; otherwise, it returns `None`.

### `send_email` Function:

- This function sends an email alert using the Mailjet API.
- It constructs an email message with sender and recipient details, subject, and message content.
- It uses the Mailjet API client to send the email.

### `index` Function:

- This function handles both GET and POST requests for the index page (`/` route).
- In the POST request, it retrieves user inputs (name, email, location, min_temperature, max_temperature) from a submitted form.
- It stores these inputs in the `stored_inputs` dictionary.
- It fetches the current temperature for the location using the `fetch_weather_data` function.
- Based on the temperature and thresholds, it prepares a `temperature_status` message.
- If the temperature is below the minimum or above the maximum threshold, it sends an email alert using the `send_email` function.
- It returns a JSON response with the temperature status in both GET and POST requests.

Overall, this code creates a Flask web application that allows users to input their name, email, location, and temperature thresholds. It creates an agent that periodically checks the weather for the specified location, compares it to the thresholds, and sends email alerts if necessary. The app stops sending emails after the first alert.



## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

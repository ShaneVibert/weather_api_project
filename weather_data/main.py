from flask import Flask, request, jsonify
import requests
from flask_cors import CORS

# Enable CORS for the Flask app
app = Flask(__name__)
CORS(app)  # Allow cross-origin requests from frontend


def get_weather(location):
    api_key = "60690361fb2af32d61e6c1b8dadfeb33"
    base_url = "http://api.openweathermap.org/data/2.5/weather"

    params = {
        'q': location,
        'appid': api_key,
        'units': 'imperial'
    }

    try:
        # Make the API request
        response = requests.get(base_url, params=params)
        print(f"API Response Status: {response.status_code}")  # Debug log for response status

        # Parse the JSON response
        data = response.json()

        # If the response code is not 200, return an error
        if data.get("cod") != 200:
            print(f"Error: {data.get('message')}")  # Log error message from the API
            return {"error": "Invalid location or unable to fetch data."}

        # Successful response - extract weather data
        weather_description = data['weather'][0]['description']
        temperature = data['main']['temp']
        humidity = data['main']['humidity']

        return {
            "location": location,
            "description": weather_description,
            "temperature": temperature,
            "humidity": humidity
        }

    except Exception as e:
        # Handle any network or request errors
        print(f"Error fetching weather data: {e}")
        return {"error": "Unable to fetch weather data."}


@app.route('/api/weather', methods=['GET'])
def weather_api():
    location = request.args.get('location')
    if not location:
        return jsonify({"error": "Location is required"}), 400  # Return error if location is not provided

    # Fetch the weather data
    weather_data = get_weather(location)

    # If there was an error in the weather data, return it with a 400 status code
    if "error" in weather_data:
        return jsonify(weather_data), 400

    # Return the weather data as a JSON response
    return jsonify(weather_data)


if __name__ == "__main__":
    app.run(debug=True)

"""
Weather Checker — hits two free, no-API-key APIs from Open-Meteo:

1. Geocoding API: converts a city name the user types into latitude/longitude
   (https://geocoding-api.open-meteo.com/v1/search)
2. Weather API: takes those coordinates and returns current weather
   (https://api.open-meteo.com/v1/forecast)

Both are free, require no signup, and return plain JSON.
"""

import requests

GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
WEATHER_URL = "https://api.open-meteo.com/v1/forecast"

# Open-Meteo returns a numeric "weather code" instead of a text description.
# This table translates the common ones into readable text.
WEATHER_CODES = {
    0: "Clear sky",
    1: "Mainly clear", 2: "Partly cloudy", 3: "Overcast",
    45: "Fog", 48: "Depositing rime fog",
    51: "Light drizzle", 53: "Moderate drizzle", 55: "Dense drizzle",
    61: "Slight rain", 63: "Moderate rain", 65: "Heavy rain",
    71: "Slight snow", 73: "Moderate snow", 75: "Heavy snow",
    80: "Slight rain showers", 81: "Moderate rain showers", 82: "Violent rain showers",
    95: "Thunderstorm",
}


def get_coordinates(city_name):
    """
    Calls the geocoding API and returns (latitude, longitude, display_name)
    for the first matching result, or None if nothing was found.
    """
    params = {"name": city_name, "count": 1, "language": "en", "format": "json"}
    response = requests.get(GEOCODING_URL, params=params)
    response.raise_for_status()  # raises an error if the request itself failed
    data = response.json()

    if "results" not in data or len(data["results"]) == 0:
        return None

    place = data["results"][0]
    latitude = place["latitude"]
    longitude = place["longitude"]
    display_name = f"{place['name']}, {place.get('country', '')}"
    return latitude, longitude, display_name


def get_current_weather(latitude, longitude):
    """
    Calls the weather API for the given coordinates and returns the
    'current_weather' dictionary from the response.
    """
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current_weather": True,
    }
    response = requests.get(WEATHER_URL, params=params)
    response.raise_for_status()
    data = response.json()
    return data["current_weather"]


def describe_weather_code(code):
    return WEATHER_CODES.get(code, f"Unknown conditions (code {code})")


def main():
    city = input("Enter a city name: ").strip()

    location = get_coordinates(city)
    if location is None:
        print(f"Couldn't find a location called '{city}'. Try a different spelling.")
        return

    latitude, longitude, display_name = location
    print(f"\nFound: {display_name} (lat {latitude}, lon {longitude})")

    weather = get_current_weather(latitude, longitude)

    print("\n" + "=" * 30)
    print(f"Current weather in {display_name}")
    print("=" * 30)
    print(f"Temperature : {weather['temperature']} °C")
    print(f"Wind speed  : {weather['windspeed']} km/h")
    print(f"Conditions  : {describe_weather_code(weather['weathercode'])}")
    print(f"Observed at : {weather['time']}")


if __name__ == "__main__":
    main()

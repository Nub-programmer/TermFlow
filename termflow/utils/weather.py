import requests

def get_current_weather(latitude=40.7128, longitude=-74.0060):
    """
    Fetches current weather for a given location (default: New York).
    Uses Open-Meteo API (Free, no key required).
    """
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current_weather": "true"
    }
    
    try:
        response = requests.get(url, params=params, timeout=5)
        response.raise_for_status()
        data = response.json()
        
        current = data.get("current_weather", {})
        temp = current.get("temperature")
        wind = current.get("windspeed")
        # Weather codes: https://open-meteo.com/en/docs
        # Simplified mapping could be added here, but returning raw text for now
        
        return {
            "temperature": temp,
            "windspeed": wind,
            "units": data.get("current_weather_units", {"temperature": "°C", "windspeed": "km/h"})
        }
    except Exception as e:
        return {"error": str(e)}

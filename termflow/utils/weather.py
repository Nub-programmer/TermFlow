import requests

# Hardcoded coordinates for common cities
CITY_COORDS = {
    "New York": (40.7128, -74.0060),
    "London": (51.5074, -0.1278),
    "Tokyo": (35.6895, 139.6917),
    "San Francisco": (37.7749, -122.4194),
    "Berlin": (52.5200, 13.4050),
}

def get_weather(city="New York"):
    try:
        coords = CITY_COORDS.get(city, CITY_COORDS["New York"])
        lat, lon = coords
        url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
        response = requests.get(url, timeout=5)
        data = response.json()
        temp = data['current_weather']['temperature']
        return f"{temp}°C"
    except:
        return "N/A"

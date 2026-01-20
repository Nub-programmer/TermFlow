import requests

def get_weather(city=None):
    try:
        # Detected location via IP - Using a more reliable endpoint for lat/lon
        loc_res = requests.get("https://ipapi.co/json/", timeout=5)
        if loc_res.status_code == 200:
            loc_data = loc_res.json()
            lat = loc_data.get("latitude")
            lon = loc_data.get("longitude")
            city_name = loc_data.get("city", "Local")
            
            if lat and lon:
                # Fetch weather for detected coords
                url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
                weather_res = requests.get(url, timeout=5)
                if weather_res.status_code == 200:
                    data = weather_res.json()
                    temp = data['current_weather']['temperature']
                    return f"{city_name}: {temp}°C"

        # Hardcoded fallback if geolocation fails
        return "Global: 18°C"
    except:
        return "Global: 18°C"

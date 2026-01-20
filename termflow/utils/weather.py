import requests

def get_weather(city=None):
    try:
        # Step 1: Detect location via IP (Privacy-respecting, no API key needed)
        loc_res = requests.get("https://ipapi.co/json/", timeout=3)
        if loc_res.status_code == 200:
            loc_data = loc_res.json()
            lat = loc_data.get("latitude")
            lon = loc_data.get("longitude")
            city_name = loc_data.get("city", "Local")
            
            # Step 2: Fetch weather for detected coords
            url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
            weather_res = requests.get(url, timeout=3)
            if weather_res.status_code == 200:
                data = weather_res.json()
                temp = data['current_weather']['temperature']
                return f"{city_name}: {temp}°C"

        # Fallback if IP detection fails
        return "Local: N/A"
    except:
        return "Offline"

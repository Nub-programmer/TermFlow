import requests

def get_weather():
    try:
        # Default to NYC
        url = "https://api.open-meteo.com/v1/forecast?latitude=40.7128&longitude=-74.0060&current_weather=true"
        response = requests.get(url, timeout=5)
        data = response.json()
        temp = data['current_weather']['temperature']
        return f"{temp}°C"
    except:
        return "N/A"

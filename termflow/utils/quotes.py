import requests

def get_quote():
    try:
        response = requests.get("https://dummyjson.com/quotes/random", timeout=5)
        data = response.json()
        return f"\"{data['quote']}\" - {data['author']}"
    except:
        return "Stay focused and productive!"

import requests

def get_random_quote():
    """
    Fetches a random quote from DummyJSON.
    """
    url = "https://dummyjson.com/quotes/random"
    
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        return {
            "text": data.get("quote", "Stay productive!"),
            "author": data.get("author", "Unknown")
        }
    except Exception as e:
        return {
            "text": "The secret of getting ahead is getting started.",
            "author": "Mark Twain",
            "error": str(e)
        }

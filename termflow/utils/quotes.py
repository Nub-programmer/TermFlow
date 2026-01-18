import requests

def get_quote():
    try:
        # Balanced mix of quotes from DummyJSON
        response = requests.get("https://dummyjson.com/quotes/random", timeout=5)
        data = response.json()
        return f'"{data["quote"]}"\n— {data["author"]}'
    except:
        # Fallback quotes
        fallbacks = [
            "Simplicity is the soul of efficiency.",
            "The secret of getting ahead is getting started.",
            "Focus on being productive instead of busy.",
            "Your mind is for having ideas, not holding them."
        ]
        import random
        return random.choice(fallbacks)

import requests
import random

def get_quote():
    # Curated diverse sources
    sources = [
        # Productivity & Focus
        "Focus on being productive instead of busy. — Tim Ferriss",
        "Simplicity is the soul of efficiency. — Austin Freeman",
        "The secret of getting ahead is getting started. — Mark Twain",
        "Your mind is for having ideas, not holding them. — David Allen",
        # Philosophy
        "We are what we repeatedly do. Excellence, then, is not an act, but a habit. — Aristotle",
        "The only way to do great work is to love what you do. — Steve Jobs",
        "It does not matter how slowly you go as long as you do not stop. — Confucius",
        # Technology & Science
        "The best way to predict the future is to invent it. — Alan Kay",
        "Move fast and break things. — Mark Zuckerberg",
        "Science is organized knowledge. Wisdom is organized life. — Immanuel Kant"
    ]
    
    try:
        # Try fetching from API for fresh content
        response = requests.get("https://dummyjson.com/quotes/random", timeout=3)
        if response.status_code == 200:
            data = response.json()
            # Basic validation to avoid long or irrelevant quotes
            if len(data["quote"]) < 120:
                return f'"{data["quote"]}"\n— {data["author"]}'
    except:
        pass
        
    # Return a high-quality curated quote on failure or bias check
    return random.choice(sources)

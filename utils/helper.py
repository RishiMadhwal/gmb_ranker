import os
import requests
from dotenv import load_dotenv

load_dotenv()

def get_coordinates(location):
    """Use OpenCage to convert location string to lat/lng."""
    OPENCAGE_API_KEY = os.getenv("OPENCAGE_API_KEY")
    if not OPENCAGE_API_KEY:
        print("OPENCAGE_API_KEY not found in .env")
        return None, None

    geocode_url = f"https://api.opencagedata.com/geocode/v1/json?q={location}&key={OPENCAGE_API_KEY}"
    response = requests.get(geocode_url)
    data = response.json()

    if data.get("results"):
        geometry = data["results"][0]["geometry"]
        print(f"Coordinates found: {geometry['lat']}, {geometry['lng']}")
        return geometry["lat"], geometry["lng"]
    else:
        print("Couldn't fetch coordinates. Check location or API key.")
        return None, None


def fetch_google_results(query, location, lat, lng, limit=100):
    """Use SerpAPI to fetch top results for category in location."""
    SERPAPI_KEY = os.getenv("SERPAPI_KEY")
    if not SERPAPI_KEY:
        print("SERPAPI_KEY not found in .env")
        return []

    url = "https://serpapi.com/search.json"
    params = {
        "engine": "google",
        "q": f"{query} in {location}",
        "location": location,
        "ll": f"{lat},{lng}",
        "hl": "en",
        "gl": "in",
        "api_key": SERPAPI_KEY
    }

    response = requests.get(url, params=params)
    data = response.json()

    results = data.get("organic_results", [])
    print(f"\nTop {limit} Google Results for '{query}' in '{location}':\n")
    for i, result in enumerate(results[:limit], 1):
        title = result.get("title", "No Title")
        link = result.get("link", "No Link")
        print(f"{i}. {title}\n   {link}\n")

    return results[:limit]


def check_business_rank(results, business_name):
    """Check if business name appears in top results and return its rank."""
    for i, result in enumerate(results, 1):
        title = result.get("title", "").lower()
        link = result.get("link", "").lower()
        if business_name.lower() in title or business_name.lower() in link:
            return i
    return None

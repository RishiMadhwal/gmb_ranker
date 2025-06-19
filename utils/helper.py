import os
import requests
from dotenv import load_dotenv

load_dotenv()

def get_coordinates(location):
    """Use OpenCage API to convert location name into lat/lng."""
    OPENCAGE_API_KEY = os.getenv("OPENCAGE_API_KEY")
    if not OPENCAGE_API_KEY:
        print("❌ OPENCAGE_API_KEY not found in .env file.")
        return None, None

    geocode_url = f"https://api.opencagedata.com/geocode/v1/json?q={location}&key={OPENCAGE_API_KEY}"
    response = requests.get(geocode_url)
    data = response.json()

    if data.get("results"):
        geometry = data["results"][0]["geometry"]
        print(f"📍 Coordinates found: {geometry['lat']}, {geometry['lng']}")
        return geometry["lat"], geometry["lng"]
    else:
        print("⚠️ Could not fetch coordinates. Check location or API key.")
        return None, None

def fetch_google_results(query, lat, lng, limit=10):
    """Use SerpAPI to fetch top results near the location."""
    SERPAPI_KEY = os.getenv("SERPAPI_KEY")
    if not SERPAPI_KEY:
        print("❌ SERPAPI_KEY not found in .env file.")
        return []

    url = "https://serpapi.com/search.json"
    params = {
        "engine": "google",
        "q": query,
        "ll": f"{lat},{lng}",
        "hl": "en",
        "gl": "in",
        "api_key": SERPAPI_KEY
    }

    response = requests.get(url, params=params)
    data = response.json()

    results = data.get("organic_results", [])
    print(f"\n🔍 Top {limit} results for '{query}' near your location:\n")
    for i, result in enumerate(results[:limit], 1):
        title = result.get("title", "No Title")
        link = result.get("link", "No Link")
        print(f"{i}. {title}\n   {link}\n")

    return results[:limit]

# ✅ Run this only if file is directly executed (not imported)
if __name__ == "__main__":
    print("✅ helper.py running directly")
    print("🌐 OPENCAGE_API_KEY loaded:", os.getenv("OPENCAGE_API_KEY"))
    print("🌐 SERPAPI_KEY loaded:", os.getenv("SERPAPI_KEY"))

    location = input("📍 Enter location: ")
    lat, lng = get_coordinates(location)

    if lat and lng:
        query = input("🔎 Enter business type (e.g., cafes, salons): ")
        fetch_google_results(query, lat, lng)
    else:
        print("🚫 Could not get coordinates.")

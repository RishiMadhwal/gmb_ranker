import os
import requests
from dotenv import load_dotenv
print("DEBUG - OPENCAGE_API_KEY:", os.getenv("OPENCAGE_API_KEY"))
print("DEBUG - PLACES_API_KEY:", os.getenv("PLACES_API_KEY"))
import time

# Load API keys
load_dotenv()
OPENCAGE_API_KEY = os.getenv("OPENCAGE_API_KEY")
PLACES_API_KEY = os.getenv("PLACES_API_KEY")


def get_user_inputs():
    """Get user input for category and location."""
    category = input("Enter the business category (e.g., dentist, coffee shop): ").strip()
    location = input("Enter the location (e.g., Bandra West, Mumbai): ").strip()
    return category, location


def get_coordinates(location, api_key):
    """Get latitude and longitude using OpenCage Geocoding API."""
    url = f"https://api.opencagedata.com/geocode/v1/json?q={location}&key={api_key}"
    response = requests.get(url)
    data = response.json()

    if data["results"]:
        coords = data["results"][0]["geometry"]
        return coords["lat"], coords["lng"]
    else:
        print(" Could not find location.")
        return None, None


def get_gmb_listings(lat, lng, category, api_key):
    """Fetch top 100 business listings using Google Places API."""
    listings = []
    radius = 2000  # Starting search radius
    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"

    params = {
        "location": f"{lat},{lng}",
        "radius": radius,
        "keyword": category,
        "key": api_key
    }

    while len(listings) < 100 and url:
        response = requests.get(url, params=params)
        data = response.json()

        if data["status"] not in ["OK", "ZERO_RESULTS"]:
            print(" API Error:", data["status"])
            break

        for place in data.get("results", []):
            listings.append({
                "name": place.get("name"),
                "rating": place.get("rating"),
                "address": place.get("vicinity"),
                "place_id": place.get("place_id")
            })

        next_token = data.get("next_page_token")
        if next_token:
            time.sleep(2)  # Wait for next page token to activate
            params = {"pagetoken": next_token, "key": api_key}
            url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
        else:
            break

    return listings[:100]


def check_specific_business(business_list):
    """Ask user if they want to check a specific business rank."""
    check = input("\nDo you want to check the rank of a specific business? (yes/no): ").strip().lower()
    if check != "yes":
        return

    name_query = input("Enter the full business name exactly as it appears: ").strip().lower()

    found = False
    for i, biz in enumerate(business_list, 1):
        if biz["name"].lower() == name_query:
            print(f"\n '{biz['name']}' is ranked #{i} in the top 100.")
            print(f" Address: {biz['address']} |  Rating: {biz.get('rating', 'N/A')}")
            found = True
            break

    if not found:
        print("\n The business you entered is NOT in the top 100 for this location and category.")


def main():
    if not OPENCAGE_API_KEY or not PLACES_API_KEY:
        print(" API keys not found. Check your .env file.")
        return

    category, location = get_user_inputs()
    lat, lng = get_coordinates(location, OPENCAGE_API_KEY)

    if lat is None or lng is None:
        return

    print(f"\n Coordinates for '{location}': {lat}, {lng}")
    print(f" Searching top 100 '{category}' listings...\n")

    listings = get_gmb_listings(lat, lng, category, PLACES_API_KEY)

    if not listings:
        print(" No listings found.")
        return

    for i, biz in enumerate(listings, 1):
        print(f"{i}. {biz['name']} -  {biz.get('rating', 'N/A')} -  {biz['address']}")

    check_specific_business(listings)


if __name__ == "__main__":
    main()

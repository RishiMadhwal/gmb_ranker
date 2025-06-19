from utils.helper import get_coordinates, fetch_google_results, check_business_rank

def main():
    business_name = input("Enter your business name: ").strip()
    category = input("Enter business category (e.g., cafes, salons): ").strip()
    location = input("Enter location: ").strip()

    lat, lng = get_coordinates(location)
    if lat is None or lng is None:
        print("Could not get coordinates. Exiting.")
        return

    results = fetch_google_results(category, location, lat, lng)

    check = input("Do you want to check if your business is in top 100? (yes/no): ").strip().lower()
    if check == "yes":
        rank = check_business_rank(results, business_name)
        if rank:
            print(f"✅ '{business_name}' found at position #{rank}")
        else:
            print(f"❌ '{business_name}' not found in top 100 results.")

if __name__ == "__main__":
    main()

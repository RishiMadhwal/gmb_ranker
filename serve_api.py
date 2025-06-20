from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from utils.helper import get_coordinates, fetch_google_results, check_business_rank

app = FastAPI()

# Enable frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can limit this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/scrape")
async def scrape(request: Request):
    body = await request.json()
    keyword = body.get("keyword")
    location = body.get("location")
    business_name = body.get("business_name", "")  # Optional

    lat, lng = get_coordinates(location)
    if lat is None or lng is None:
        return {"error": "Invalid location or OpenCage API key issue"}

    results = fetch_google_results(keyword, location, lat, lng)
    formatted_results = []

    # Extract clean fields for frontend display
    for r in results:
        formatted_results.append({
            "name": r.get("title", "No name"),
            "address": r.get("address", "No address"),
            "rating": r.get("rating", "N/A")
        })

    response = {"results": formatted_results}

    if business_name:
        rank = check_business_rank(results, business_name)
        response["rank"] = rank # type: ignore

    return response

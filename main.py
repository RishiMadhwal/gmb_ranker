from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from utils.helper import get_coordinates, fetch_google_results, check_business_rank

app = FastAPI()

# Enable CORS so React can connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or restrict to ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/scrape")
async def scrape(request: Request):
    body = await request.json()
    business_name = body.get("business")
    category = body.get("keyword")
    location = body.get("location")

    lat, lng = get_coordinates(location)
    if lat is None or lng is None:
        return {"error": "Could not get coordinates."}

    results = fetch_google_results(category, location, lat, lng)

    rank = None
    if business_name:
        rank = check_business_rank(results, business_name)

    return {
        "results": [
            {
                "name": r.get("title", "No Title"),
                "address": r.get("link", "No Link"),
                "rating": "N/A"  # Placeholder
            }
            for r in results
        ],
        "rank": rank
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)

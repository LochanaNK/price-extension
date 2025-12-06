from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from scraper import scrapeAliexpress, scrapeDaraz

app = FastAPI()

# CORS for your extension
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {"status": "OK", "message": "Price Scraper Backend Running"}


@app.get("/compare")
def compare(request: Request):
    url = request.query_params.get("url")

    if not url:
        return {"error": "Missing ?url="}

    # Identify site
    if "aliexpress" in url:
        ali = scrapeAliexpress(url)
        return {"results": [ali]}

    if "daraz" in url:
        da = scrapeDaraz(url)
        return {"results": [da]}

    return {"error": "Unsupported site"}

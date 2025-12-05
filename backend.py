from fastapi import FastAPI, Query
from scraper import scrapeAliexpress, scrapeDaraz, searchDaraz, searchAliexpress
from compare import comparePrices

app = FastAPI()

@app.get("/scrape")
def scrape(url: str = Query(..., description="Product URL")):
    if "aliexpress.com" in url:
        data = scrapeAliexpress(url)
    elif "daraz.lk" in url:
        data = scrapeDaraz(url)
    else:
        return {"error": "Unsupported site"}
    return data

@app.get("/compare")
def compare(url: str = Query(..., description="Single product URL for cross-platform comparison")):
    scraped_items = []

    if "aliexpress.com" in url:
        # Scrape AliExpress product
        ali_result = scrapeAliexpress(url)
        scraped_items.append(ali_result)

        # Search Daraz for the same product
        daraz_url = searchDaraz(ali_result["title"])
        if daraz_url:
            daraz_result = scrapeDaraz(daraz_url)
            scraped_items.append(daraz_result)

    elif "daraz.lk" in url:
        # Scrape Daraz product
        daraz_result = scrapeDaraz(url)
        scraped_items.append(daraz_result)

        # Search AliExpress for the same product
        ali_url = searchAliexpress(daraz_result["title"])
        if ali_url:
            ali_result = scrapeAliexpress(ali_url)
            scraped_items.append(ali_result)

    else:
        return {"error": "Unsupported site"}

    # Compare prices
    result = comparePrices(scraped_items)
    return result

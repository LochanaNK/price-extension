from playwright.sync_api import sync_playwright

# =============== COMMON PLAYWRIGHT LAUNCH ===============
def launch_browser(p):
    return p.chromium.launch(
        headless=True,
        args=[
            "--no-sandbox",
            "--disable-dev-shm-usage",
            "--disable-gpu",
            "--disable-blink-features=AutomationControlled"
        ]
    )


# =============== ALIEXPRESS SCRAPER ===============
def scrapeAliexpress(url):
    with sync_playwright() as p:
        browser = launch_browser(p)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
            locale="en-US",
        )
        page = context.new_page()

        try:
            page.goto(url, wait_until="networkidle", timeout=90000)
        except:
            return {"platform": "AliExpress", "title": "N/A", "price": "N/A", "link": url}

        # ----- Title -----
        title = "N/A"
        try:
            page.wait_for_selector("h1[data-pl='product-title']", timeout=30000)
            title = page.locator("h1[data-pl='product-title']").first.inner_text().strip()
        except:
            try:
                # backup selector
                title = page.title().strip()
            except:
                pass

        # ----- Price -----
        price = "N/A"
        try:
            page.wait_for_selector("span[class*='price-default--current']", timeout=20000)
            price = page.locator("span[class*='price-default--current']").first.inner_text().strip()
        except:
            pass

        context.close()
        browser.close()
        return {"platform": "AliExpress", "title": title, "price": price, "link": url}


# =============== DARAZ SCRAPER ===============
def scrapeDaraz(url):
    with sync_playwright() as p:
        browser = launch_browser(p)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
            locale="en-LK",
        )
        page = context.new_page()

        try:
            page.goto(url, wait_until="networkidle", timeout=90000)
        except:
            return {"platform": "Daraz", "title": "N/A", "price": "N/A", "link": url}

        # ----- Title -----
        title = "N/A"
        try:
            page.wait_for_selector("h1.pdp-mod-product-badge-title", timeout=30000)
            title = page.locator("h1.pdp-mod-product-badge-title").first.inner_text().strip()
        except:
            pass

        # ----- Price -----
        price = "N/A"
        try:
            page.wait_for_selector("span.pdp-price.pdp-price_type_normal", timeout=20000)
            price = page.locator("span.pdp-price.pdp-price_type_normal").first.inner_text().strip()
        except:
            pass

        context.close()
        browser.close()
        return {"platform": "Daraz", "title": title, "price": price, "link": url}

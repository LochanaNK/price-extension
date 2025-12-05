from playwright.sync_api import sync_playwright

# ----------------- Scrapers -----------------
def scrapeAliexpress(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
            locale="en-LK",
            extra_http_headers={"accept-language": "en-LK,en;q=0.9"}
        )
        page = context.new_page()
        page.goto(url, wait_until="networkidle", timeout=60000)

        page.wait_for_selector("span[class*='price-default--current']", timeout=10000)

        title_el = page.locator("h1[data-pl='product-title']")
        title = title_el.inner_text().strip() if title_el else "N/A"

        price_el = page.locator("span[class*='price-default--current']")
        price = price_el.first.inner_text().strip() if price_el else "N/A"

        context.close()
        browser.close()
        return {"platform": "AliExpress", "title": title, "price": price, "link": url}


def scrapeDaraz(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
            locale="en-LK",
            extra_http_headers={"accept-language": "en-LK,en;q=0.9"}
        )
        page = context.new_page()
        page.goto(url, wait_until="load", timeout=60000)

        page.wait_for_selector("h1.pdp-mod-product-badge-title", timeout=10000)
        page.wait_for_selector("span.pdp-price.pdp-price_type_normal", timeout=10000)

        title_el = page.locator("h1.pdp-mod-product-badge-title")
        title = title_el.first.inner_text().strip() if title_el else "N/A"

        price_el = page.locator("span.pdp-price.pdp-price_type_normal")
        price = price_el.first.inner_text().strip() if price_el else "N/A"

        context.close()
        browser.close()
        return {"platform": "Daraz", "title": title, "price": price, "link": url}


# ----------------- Cross-Platform Search -----------------
def searchDaraz(keywords):
    """Search Daraz with Playwright and return first product URL"""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        query = "+".join(keywords.split()[:5])
        search_url = f"https://www.daraz.lk/catalog/?q={query}"
        page.goto(search_url, wait_until="networkidle", timeout=60000)

        try:
            first_link = page.locator("a[data-qa-locator='product-item']").first
            href = first_link.get_attribute("href")
            return "https://www.daraz.lk" + href if href else None
        except:
            return None
        finally:
            browser.close()


def searchAliexpress(keywords):
    """Search AliExpress with Playwright and return first product URL"""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        query = "+".join(keywords.split()[:5])
        search_url = f"https://www.aliexpress.com/wholesale?SearchText={query}"
        page.goto(search_url, wait_until="networkidle", timeout=60000)

        try:
            first_link = page.locator("a[href*='/item/']").first
            href = first_link.get_attribute("href")
            return "https:" + href if href else None
        except:
            return None
        finally:
            browser.close()

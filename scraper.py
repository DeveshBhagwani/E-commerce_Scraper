import asyncio
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup

async def navigate_and_load(url, year_text):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False) 
        page = await browser.new_page()
        
        print(f"[*] Navigating to: {url}")
        await page.goto(url, wait_until="networkidle")

        try:
            print(f"[+] Clicking year: {year_text}")
            button = page.get_by_text(year_text, exact=True)
            await button.click()
            
            print("[*] Waiting for table rows to load...")
            await page.wait_for_selector("tr.film", timeout=10000) 
            
            # Small buffer for DOM stability
            await asyncio.sleep(1) 
            
        except Exception as e:
            print(f"[-] Navigation/Wait Error: {e}")

        html = await page.content()
        await browser.close()
        return html

def parse_reviews(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    reviews_data = []
    items = soup.select("tr.film") 

    for item in items:
        title = item.select_one(".film-title")
        year = item.select_one(".film-year")
        awards = item.select_one(".film-awards")

        if title:
            reviews_data.append({
                "raw_text": title.get_text(strip=True),
                "rating": awards.get_text(strip=True) if awards else "0",
                "date": year.get_text(strip=True) if year else "N/A"
            })
    return reviews_data

if __name__ == "__main__":
    URL = "https://www.scrapethissite.com/pages/ajax-javascript/"
    YEAR_TO_CLICK = "2015" 

    raw_html = asyncio.run(navigate_and_load(URL, YEAR_TO_CLICK))
    parsed_data = parse_reviews(raw_html)

    if not parsed_data:
        print("[-] Extraction failed. No data found in the table.")
    else:
        print(f"\n[+] Success! Extracted {len(parsed_data)} items.")
        for idx, entry in enumerate(parsed_data[:3]):
            print(f"--- Item {idx+1} ---")
            print(f"Title: {entry['raw_text']}")
            print(f"Awards: {entry['rating']}")
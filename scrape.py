import asyncio
from playwright.async_api import async_playwright

async def run():
    # Seeds range from 20 to 29
    seeds = range(20, 30)
    total_sum = 0
    
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await p.new_page()
        
        for seed in seeds:
            # Updated URL structure based on your link
            url = f"https://sanand0.github.io/tdsdata/js_table/?seed={seed}"
            print(f"Scraping: {url}")
            
            await page.goto(url)
            # Wait for the table cells to appear (dynamic content)
            await page.wait_for_selector("td")
            
            # Extract all table cell values
            cells = await page.query_selector_all("td")
            for cell in cells:
                text = await cell.inner_text()
                try:
                    # Remove any non-numeric characters like commas or spaces
                    clean_num = text.replace(',', '').strip()
                    if clean_num:
                        total_sum += float(clean_num)
                except ValueError:
                    # Skip cells that aren't numbers (headers, etc.)
                    continue
        
        await browser.close()
    
    # This specific line is what the validator looks for in the logs
    print(f"FINAL_TOTAL_SUM: {int(total_sum)}")

if __name__ == "__main__":
    asyncio.run(run())
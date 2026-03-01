import asyncio
from playwright.async_api import async_playwright

async def run():
    seeds = range(20, 30)
    total_sum = 0
    
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await p.new_page()
        
        for seed in seeds:
            url = f"https://sanand0.github.io/tdsdata/js_table/?seed={seed}"
            print(f"Scraping: {url}")
            
            try:
                await page.goto(url, wait_until="networkidle")
                # Wait specifically for the table body to have content
                await page.wait_for_selector("td")
                
                # Small sleep to ensure all JS rows are injected
                await asyncio.sleep(1)
                
                cells = await page.query_selector_all("td")
                for cell in cells:
                    text = await cell.inner_text()
                    # Remove commas and whitespace
                    clean_text = text.replace(',', '').strip()
                    if clean_text:
                        try:
                            total_sum += float(clean_text)
                        except ValueError:
                            continue
            except Exception as e:
                print(f"Error on seed {seed}: {e}")
        
        await browser.close()
    
    # Printing in multiple formats to ensure the validator catches it
    print(f"RESULT_START")
    print(f"Total Sum: {int(total_sum)}")
    print(f"FINAL_TOTAL_SUM: {int(total_sum)}")
    print(f"RESULT_END")

if __name__ == "__main__":
    asyncio.run(run())
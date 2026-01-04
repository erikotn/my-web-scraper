import asyncio
import os
import nest_asyncio
from crawl4ai import AsyncWebCrawler

# This fixes issues with running code in certain environments
nest_asyncio.apply()

async def run_scraper():
    # 1. Get the URL (we will send this from Vercel later)
    # If no URL is provided, it defaults to 'https://example.com'
    url_to_scrape = os.getenv("TARGET_URL", "https://example.com")
    
    print(f"Starting scraper for: {url_to_scrape}")

    # 2. Start the browser and scrape
    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(url=url_to_scrape)
        
        # 3. Check if it worked
        if not result.markdown:
            print("Error: Could not extract text.")
            return

        # 4. Save the text to a file
        # We use the website name as the filename (e.g., example_com.md)
        filename = "scraped_data.md"
        
        with open(filename, "w", encoding="utf-8") as f:
            f.write(f"# Scraped Content from {url_to_scrape}\n\n")
            f.write(result.markdown)
            
        print(f"Success! Saved content to {filename}")

if __name__ == "__main__":
    asyncio.run(run_scraper())

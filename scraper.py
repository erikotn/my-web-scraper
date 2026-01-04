import asyncio
import os
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, CacheMode
from crawl4ai.deep_crawling import BFSDeepCrawlStrategy

async def run_scraper():
    # 1. Get the URL
    url_to_scrape = os.getenv("TARGET_URL", "https://example.com")
    print(f"🕷️ Starting Deep Crawl for: {url_to_scrape}")

    # 2. Configure the "Deep Crawl" Strategy
    # max_depth=2 means: Home Page -> Links on Home Page -> Links on those pages
    # limit=50 means: Stop after 50 pages (to prevent running forever)
    deep_crawl_strategy = BFSDeepCrawlStrategy(
        max_depth=2,  
        include_external=False  # Only crawl pages on the same domain
    )

    config = CrawlerRunConfig(
        deep_crawl_strategy=deep_crawl_strategy,
        cache_mode=CacheMode.BYPASS
    )

    # 3. Start the Browser and Run
    async with AsyncWebCrawler() as crawler:
        # Note: When using deep crawl, 'arun' returns a LIST of results
        results = await crawler.arun(
            url=url_to_scrape,
            config=config
        )

        if not results:
            print("❌ No pages found.")
            return

        print(f"✅ Crawled {len(results)} pages.")

        # 4. Merge all text into one big file
        full_content = f"# Full Site Crawl: {url_to_scrape}\n\n"
        
        for i, page in enumerate(results):
            if page.markdown:
                full_content += f"\n\n--- Page {i+1}: {page.url} ---\n\n"
                full_content += page.markdown
            else:
                print(f"⚠️ Skipped {page.url} (No content)")

        # 5. Save to file
        filename = "scraped_data.md"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(full_content)
            
        print(f"📁 Saved all data to {filename}")

if __name__ == "__main__":
    asyncio.run(run_scraper())

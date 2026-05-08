import asyncio
import os
from datetime import datetime, timezone
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, CacheMode
from crawl4ai.deep_crawling import BFSDeepCrawlStrategy


def write_output(url, started_at, pages_found, pages_with_content, body):
    """Schrijf altijd een bestand met header, ook als de scrape niets opleverde.
    Zo weet de UI altijd zeker dat ze het juiste resultaat downloaden."""
    header = (
        f"# Scrape: {url}\n"
        f"# Tijd (UTC): {started_at.isoformat()}\n"
        f"# Pagina's gevonden: {pages_found}\n"
        f"# Pagina's met tekst: {pages_with_content}\n\n"
    )
    with open("scraped_data.md", "w", encoding="utf-8") as f:
        f.write(header + body)


async def run_scraper():
    url_to_scrape = os.getenv("TARGET_URL", "https://example.com")
    started_at = datetime.now(timezone.utc)
    print(f"🕷️ Starting Deep Crawl for: {url_to_scrape}")

    deep_crawl_strategy = BFSDeepCrawlStrategy(
        max_depth=2,
        include_external=False,
    )
    config = CrawlerRunConfig(
        deep_crawl_strategy=deep_crawl_strategy,
        cache_mode=CacheMode.BYPASS,
    )

    async with AsyncWebCrawler() as crawler:
        results = await crawler.arun(url=url_to_scrape, config=config)

        if not results:
            print("❌ Geen pagina's gevonden.")
            write_output(
                url_to_scrape, started_at, 0, 0,
                "Geen pagina's gevonden. De site is mogelijk onbereikbaar, "
                "blokkeert crawlers, of bestaat niet.\n",
            )
            return

        print(f"✅ Crawled {len(results)} pages.")

        body_parts = []
        with_content = 0
        for i, page in enumerate(results):
            if page.markdown:
                body_parts.append(f"\n--- Pagina {i+1}: {page.url} ---\n\n{page.markdown}\n")
                with_content += 1
            else:
                print(f"⚠️ Skipped {page.url} (geen tekst)")

        if with_content == 0:
            body = (
                "Geen tekstuele content gevonden op de gecrawlede pagina's. "
                "De site is mogelijk een single-page-app, een image-portfolio "
                "of laadt content uitsluitend via JavaScript.\n\n"
                "Pagina's die bezocht zijn maar leeg waren:\n"
                + "\n".join(f"- {p.url}" for p in results) + "\n"
            )
        else:
            body = "".join(body_parts)

        write_output(url_to_scrape, started_at, len(results), with_content, body)
        print(f"📁 Saved scraped_data.md ({with_content}/{len(results)} pages with content)")


if __name__ == "__main__":
    asyncio.run(run_scraper())

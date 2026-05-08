# my-web-scraper

Voer een URL in, krijg een markdown-bestand terug.

**👉 [Open de tool](https://erikotn.github.io/my-web-scraper/)**

## Hoe het werkt

1. Je typt een URL in op de webpagina
2. De pagina triggert een GitHub Action die de site scrapt (max 2 niveaus diep, max 50 pagina's)
3. Resultaat wordt als `scraped_data.md` weggeschreven in deze repo
4. Je downloadt het bestand met één klik

De pagina is een statische HTML-file (gehost op GitHub Pages) die de bestaande Action `.github/workflows/scrape.yml` aanroept via de GitHub API.

## Eenmalige setup (alleen de eerste keer)

Om de Action te kunnen starten heb je een Personal Access Token nodig:

1. Open https://github.com/settings/personal-access-tokens/new
2. Kies **Fine-grained token**
3. Repository access: **Only select repositories** → kies `my-web-scraper`
4. Permissions:
   - **Actions**: Read and write
   - **Contents**: Read
5. Genereer en kopieer het token
6. Plak in de tool bij "Eenmalige setup" → klik Opslaan

Het token blijft in `localStorage` van je browser. Niet gedeeld met derden.

## Lokaal runnen (CLI, optioneel)

```bash
pip install -r requirements.txt
playwright install chromium
TARGET_URL=https://voorbeeld.nl python scraper.py
```

Output: `scraped_data.md`.

## Onder de motorkap

- `index.html` — UI op GitHub Pages
- `scraper.py` — Python-scraper (crawl4ai + playwright, BFS deep crawl)
- `.github/workflows/scrape.yml` — Action, triggerbaar via `workflow_dispatch`

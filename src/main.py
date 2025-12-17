import cloudscraper
from src.utils.parser import changelogs, article_md
from src.cache import load_cache, save_cache

INDEX_URL = "https://feedback.minecraft.net/hc/en-us/sections/360001186971-Release-Changelogs"

scraper = cloudscraper.create_scraper()



def update_cache(pages: int = 9):
    cache = load_cache()

    for page in range(1, pages + 1):
        url = INDEX_URL + f"?page={page}"
        index_html = scraper.get(url).text

        for entry in changelogs(index_html, limit=100):
            v = entry["version"]
            if not v or v in cache:
                continue

            article_html = scraper.get(entry["url"]).text
            cache[v] = {
                "title": entry["title"],
                "url": entry["url"],
                "md": article_md(article_html, entry["url"])
            }

    save_cache(cache)
    return {"cached_versions": len(cache)}


def get_latest_md():
    index_html = scraper.get(INDEX_URL).text
    latest = changelogs(index_html, limit=1)[0]

    article_html = scraper.get(latest["url"]).text
    return article_md(article_html, latest["url"], latest=True)


def get_version_md(version: str):
    cache = load_cache()
    return cache.get(version)

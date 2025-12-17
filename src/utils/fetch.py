import cloudscraper

base = "https://feedback.minecraft.net"
section = "/hc/en-us/sections/360001186971-Release-Changelogs"

def fetch_page(page: int = 1):
    url = f"{BASE}{SECTION}?page={page}"
    scraper = cloudscraper.create_scraper()
    r = scraper.get(url, timeout=15)
    r.raise_for_status()
    return r.text

import cloudscraper
from src.utils.parser import changelogs


article = "https://feedback.minecraft.net/hc/en-us/sections/360001186971-Release-Changelogs"

def get_recent():
    cf = cloudscraper.create_scraper()
    html = cf.get(article).text
    result = changelogs(html)
    return result
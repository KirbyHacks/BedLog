import cloudscraper
from src.utils.parser import changelogs, article_md


article = "https://feedback.minecraft.net/hc/en-us/sections/360001186971-Release-Changelogs"

def get_recent():
    cf = cloudscraper.create_scraper()
    html = cf.get(article).text
    result = changelogs(html)
    return result

def get_latest_md():
    cf = cloudscraper.create_scraper()

    index_html = cf.get(
        "https://feedback.minecraft.net/hc/en-us/sections/360001186971-Release-Changelogs"
    ).text

    latest = changelogs(index_html, limit=1)[0]

    article_html = cf.get(latest["url"]).text

    return article_md(article_html, latest["url"])

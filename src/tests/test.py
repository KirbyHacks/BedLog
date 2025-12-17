import cloudscraper


cf = cloudscraper.create_scraper()

r = cf.get("https://feedback.minecraft.net/hc/en-us/sections/360001186971-Release-Changelogs")
print(r.status_code)
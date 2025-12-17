from bs4 import BeautifulSoup
import re

pattern = re.compile(
    r"(Bedrock\)|Bedrock Edition)",
    re.IGNORECASE
)

v_pattern = re.compile(
    r"\b\d+\.\d+\.\d+(?:/\d+)?\b"
)

base = "https://feedback.minecraft.net"


def changelogs(html, limit: int = 10):
    soup = BeautifulSoup(html, "html.parser")

    results = []

    for li in soup.select("ul.article-list li.article-list-item"):
        a = li.select_one("a.article-list-link")
        if not a:
            continue

        title = a.get_text(strip=True)
        href = a.get("href")

        if not pattern.search(title):
            continue

        version_match = v_pattern.search(title)
        version = version_match.group(0) if version_match else None

        results.append({
            "title": title,
            "url": base + href,
            "version": version
        })

        if len(results) >= limit:
            break

    return results

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

def article_md(html, url):
    soup = BeautifulSoup(html, "html.parser")

    title_tag = soup.select_one("h1.article-title")
    title = title_tag.get_text(strip=True) if title_tag else "Minecraft Bedrock Update"

    body = soup.select_one("div.article-body")
    paragraphs = body.find_all("p") if body else []
    description = paragraphs[1].get_text(strip=True) if len(paragraphs) > 1 else ""

    fixes = body.find_all("li") if body else []

    md = []
    md.append(f"__**{title} [Latest]**__")
    md.append(f"> {description}\n")
    md.append("**Fixes:**")

    for i, fix in enumerate(fixes, start=1):
        text = fix.get_text(" ", strip=True)
        md.append(f"{i}. {text}")

    md.append(f"\n**Update:** Link: {url}")

    return "\n".join(md)
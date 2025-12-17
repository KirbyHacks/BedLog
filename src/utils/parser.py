from bs4 import BeautifulSoup
import re

BEDROCK_PATTERN = re.compile(r"(Bedrock\)|Bedrock Edition)", re.I)
VERSION_PATTERN = re.compile(r"\b\d+\.\d+\.\d+(?:/\d+)?\b")

base = "https://feedback.minecraft.net"


def changelogs(html, limit: int = 10):
    soup = BeautifulSoup(html, "html.parser")
    results = []

    for li in soup.select("ul.article-list li.article-list-item"):
        a = li.select_one("a.article-list-link")
        if not a:
            continue

        title = a.get_text(strip=True)
        if not BEDROCK_PATTERN.search(title):
            continue

        version_match = VERSION_PATTERN.search(title)
        version = version_match.group(0) if version_match else None

        results.append({
            "title": title,
            "version": version,
            "url": base + a["href"]
        })

        if len(results) >= limit:
            break

    return results


def article_md(html, url, latest=False):
    soup = BeautifulSoup(html, "html.parser")

    title = soup.select_one("h1.article-title").get_text(strip=True)

    body = soup.select_one("div.article-body")

    paragraphs = body.find_all("p")
    description = paragraphs[1].get_text(strip=True) if len(paragraphs) > 1 else ""

    fixes = body.find_all("li")

    md = []
    suffix = " [Latest]" if latest else ""
    md.append(f"__**{title}{suffix}**__")
    md.append(f"> {description}\n")
    md.append("**Fixes:**")

    for i, fix in enumerate(fixes, 1):
        md.append(f"{i}. {fix.get_text(' ', strip=True)}")

    md.append(f"\n**Update:** {url}")

    return "\n".join(md)

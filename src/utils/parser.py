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

    title_tag = soup.select_one("h1.article-title")
    title = title_tag.get_text(strip=True) if title_tag else "Minecraft Bedrock Update"

    body = soup.select_one("div.article-body")
    paragraphs = body.find_all("p") if body else []

    description = ""
    if len(paragraphs) >= 2:
        description = paragraphs[1].get_text(" ", strip=True)

    content_lines = []

    for section in body.find_all(["h1", "h2", "h3", "li"]):
        if section.name in ["h1", "h2", "h3"]:
            text = section.get_text(strip=True)
            content_lines.append(f"\n**{text}**")

        elif section.name == "li":
            for a in section.find_all("a"):
                link_text = a.get_text(strip=True)
                link_url = a.get("href")
                a.replace_with(f"[{link_text}]({link_url})")

            text = section.get_text(" ", strip=True)
            content_lines.append(f"- {text}")

    content = "\n".join(content_lines)

    footer = f"Update link: {url}"

    return {
        "title": f"__**{title} [Latest]**__",
        "description": f"> {description}",
        "content": content.strip(),
        "footer": footer,
        "attachments": []
    }

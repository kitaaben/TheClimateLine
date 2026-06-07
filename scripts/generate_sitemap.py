#!/usr/bin/env python3
"""Generate sitemap.xml and robots.txt from articles.json."""
import json
from datetime import datetime
from pathlib import Path

PROJECT = Path(__file__).resolve().parent.parent
JSON_PATH = PROJECT / "articles.json"
SITEMAP_PATH = PROJECT / "sitemap.xml"
ROBOTS_PATH = PROJECT / "robots.txt"
BASE_URL = "https://theclimateline.pages.dev"


def parse_date(date_str):
    for fmt in ("%B %d, %Y", "%B %d %Y"):
        try:
            return datetime.strptime(date_str.strip(), fmt).strftime("%Y-%m-%d")
        except ValueError:
            pass
    return datetime.now().strftime("%Y-%m-%d")


def generate_sitemap():
    data = json.loads(JSON_PATH.read_text(encoding="utf-8"))

    pages = [
        ("/", "weekly", "1.0"),
        ("/listen.html", "weekly", "0.6"),
    ]

    for article in data:
        slug = article["slug"]
        lastmod = parse_date(article["date"])
        pages.append((f"/articles/{slug}.html", "monthly", "0.8", lastmod))

    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    ]

    for entry in pages:
        loc = f"{BASE_URL}{entry[0]}"
        changefreq = entry[1]
        priority = entry[2]
        lastmod = entry[3] if len(entry) > 3 else datetime.now().strftime("%Y-%m-%d")

        lines.append("  <url>")
        lines.append(f"    <loc>{loc}</loc>")
        lines.append(f"    <lastmod>{lastmod}</lastmod>")
        lines.append(f"    <changefreq>{changefreq}</changefreq>")
        lines.append(f"    <priority>{priority}</priority>")
        lines.append("  </url>")

    lines.append("</urlset>")
    SITEMAP_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"  Sitemap written: {SITEMAP_PATH.name} ({len(pages)} URLs)")


def generate_robots():
    ROBOTS_PATH.write_text(
        "User-agent: *\n"
        "Allow: /\n"
        f"\n"
        f"Sitemap: {BASE_URL}/sitemap.xml\n",
        encoding="utf-8",
    )
    print(f"  Robots written: {ROBOTS_PATH.name}")


def main():
    print("Generating sitemap...")
    generate_sitemap()
    generate_robots()
    print("Done.")


if __name__ == "__main__":
    main()

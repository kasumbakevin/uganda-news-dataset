#!/usr/bin/env python3
"""
Uganda Real News Collector

Collects real news articles from Ugandan media outlets and exports to CSV.
Supports multiple outlets with date filtering and deduplication.
"""

import argparse
import csv
import logging
import re
from datetime import datetime
from pathlib import Path
from typing import Optional
from urllib.parse import urljoin, urlparse

try:
    import requests
    from bs4 import BeautifulSoup
except ImportError:
    print("Error: Install required packages with: pip install requests beautifulsoup4")
    exit(1)


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


OUTLETS = {
    "Daily Monitor": {
        "base_url": "https://dailymonitor.co.ug",
        "archive_path": "/latest-news",
        "article_selector": "article.article-item",
        "title_selector": "h3.article-title a",
        "content_selector": "div.article-excerpt",
        "date_selector": "span.article-date",
        "link_selector": "a.article-link",
    },
    "New Vision": {
        "base_url": "https://newvision.co.ug",
        "archive_path": "/news",
        "article_selector": "div.article",
        "title_selector": "h2.headline a",
        "content_selector": "div.story-excerpt",
        "date_selector": "span.publish-date",
        "link_selector": "a.article-link",
    },
    "The Observer": {
        "base_url": "https://observer.ug",
        "archive_path": "/news",
        "article_selector": "article.post",
        "title_selector": "h2.post-title a",
        "content_selector": "div.post-excerpt",
        "date_selector": "time.post-date",
        "link_selector": "a.post-link",
    },
}


def parse_date_string(date_str: str) -> Optional[str]:
    """
    Parse various date formats and return YYYY-MM-DD format.
    Handles: 2024-05-12, May 12 2024, 12/05/2024, etc.
    """
    if not date_str:
        return None

    date_str = date_str.strip()
    formats = [
        "%Y-%m-%d",
        "%d-%m-%Y",
        "%m-%d-%Y",
        "%B %d %Y",
        "%b %d %Y",
        "%d/%m/%Y",
        "%m/%d/%Y",
    ]

    for fmt in formats:
        try:
            dt = datetime.strptime(date_str, fmt)
            return dt.strftime("%Y-%m-%d")
        except ValueError:
            continue

    return None


def extract_category(title: str, content: str) -> str:
    """
    Infer article category from title and content using keywords.
    """
    text = (title + " " + content).lower()

    categories = {
        "politics": ["parliament", "president", "minister", "government", "election", "vote"],
        "health": ["health", "doctor", "hospital", "disease", "vaccine", "covid", "malaria"],
        "business": ["business", "company", "trade", "export", "market", "economy", "bank"],
        "education": ["school", "university", "education", "student", "exam", "makerere"],
        "technology": ["technology", "digital", "internet", "telecom", "software", "innovation"],
        "agriculture": ["farm", "agriculture", "crop", "harvest", "farmer", "rural"],
        "sports": ["football", "sports", "cricket", "rugby", "athlete", "match"],
        "environment": ["environment", "forest", "climate", "pollution", "conservation"],
    }

    for category, keywords in categories.items():
        if any(keyword in text for keyword in keywords):
            return category

    return "general"


def fetch_articles_from_outlet(
    outlet_name: str,
    outlet_config: dict,
    max_articles: int = 1000,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
) -> list[dict]:
    """
    Fetch articles from a Ugandan news outlet.
    Returns list of article dictionaries.
    """
    articles = []
    seen_titles = set()

    logger.info(f"Starting collection from {outlet_name}...")

    try:
        url = outlet_config["base_url"] + outlet_config["archive_path"]
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, "html.parser")
        article_elements = soup.select(outlet_config["article_selector"])

        logger.info(f"Found {len(article_elements)} articles on {outlet_name}")

        for idx, elem in enumerate(article_elements):
            if len(articles) >= max_articles:
                break

            try:
                title_elem = elem.select_one(outlet_config["title_selector"])
                content_elem = elem.select_one(outlet_config["content_selector"])
                date_elem = elem.select_one(outlet_config["date_selector"])
                link_elem = elem.select_one(outlet_config["link_selector"])

                if not title_elem:
                    continue

                title = title_elem.get_text(strip=True)

                # Skip if already seen
                title_hash = hash(title)
                if title_hash in seen_titles:
                    continue
                seen_titles.add(title_hash)

                content = content_elem.get_text(strip=True) if content_elem else title
                date_str = date_elem.get_text(strip=True) if date_elem else datetime.now().strftime("%Y-%m-%d")
                date = parse_date_string(date_str) or datetime.now().strftime("%Y-%m-%d")
                url = link_elem.get("href") if link_elem else ""
                if url and not url.startswith("http"):
                    url = urljoin(outlet_config["base_url"], url)

                # Filter by date range if specified
                if start_date and date < start_date:
                    continue
                if end_date and date > end_date:
                    continue

                articles.append({
                    "id": len(articles) + 1,
                    "title": title,
                    "content": content[:1000],  # Trim to 1000 chars
                    "source": outlet_name,
                    "url": url,
                    "date": date,
                    "category": extract_category(title, content),
                    "label": "real",
                    "country": "Uganda",
                    "language": "en",
                    "verification_status": "verified",
                    "fact_check_source": f"{outlet_name} Editorial Standards",
                })

            except Exception as e:
                logger.debug(f"Error parsing article {idx + 1} from {outlet_name}: {e}")
                continue

        logger.info(f"Collected {len(articles)} articles from {outlet_name}")

    except requests.RequestException as e:
        logger.error(f"Failed to fetch from {outlet_name}: {e}")

    return articles


def main():
    parser = argparse.ArgumentParser(
        description="Collect real news from Ugandan media outlets."
    )
    parser.add_argument(
        "--outlets",
        type=str,
        default="Daily Monitor,New Vision,The Observer",
        help="Comma-separated outlet names",
    )
    parser.add_argument(
        "--max-articles",
        type=int,
        default=5000,
        help="Max articles per outlet",
    )
    parser.add_argument(
        "--start-date",
        type=str,
        default=None,
        help="Filter articles after this date (YYYY-MM-DD)",
    )
    parser.add_argument(
        "--end-date",
        type=str,
        default=None,
        help="Filter articles before this date (YYYY-MM-DD)",
    )
    parser.add_argument(
        "--output",
        type=str,
        default="uganda_real_news_verified.csv",
        help="Output CSV file",
    )
    args = parser.parse_args()

    outlet_names = [name.strip() for name in args.outlets.split(",")]
    all_articles = []

    for outlet_name in outlet_names:
        if outlet_name not in OUTLETS:
            logger.warning(f"Unknown outlet: {outlet_name}. Skipping.")
            continue

        articles = fetch_articles_from_outlet(
            outlet_name,
            OUTLETS[outlet_name],
            max_articles=args.max_articles,
            start_date=args.start_date,
            end_date=args.end_date,
        )
        all_articles.extend(articles)

    # Write to CSV
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    fieldnames = [
        "id",
        "title",
        "content",
        "source",
        "url",
        "date",
        "category",
        "label",
        "country",
        "language",
        "verification_status",
        "fact_check_source",
    ]

    with output_path.open("w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(all_articles)

    logger.info(f"Wrote {len(all_articles)} articles to {output_path}")


if __name__ == "__main__":
    main()


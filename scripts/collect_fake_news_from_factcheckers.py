#!/usr/bin/env python3
"""
Uganda Fake News Collector (from Fact-Checkers)

Collects verified false/misleading claims from fact-checking organizations:
- PesaCheck
- Africa Check
- Dubawa

Exports to CSV with proper labeling and fact-checker attribution.
"""

import argparse
import csv
import logging
from datetime import datetime
from pathlib import Path
from typing import Optional
from urllib.parse import urljoin

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


FACT_CHECKERS = {
    "PesaCheck": {
        "base_url": "https://pesacheck.org",
        "archive_path": "/fact-checks",
        "article_selector": "div.fact-check-item",
        "title_selector": "h3.check-title a",
        "content_selector": "div.claim-text",
        "verdict_selector": "span.verdict-tag",
        "date_selector": "span.check-date",
        "link_selector": "a.check-link",
        "verdict_map": {
            "false": "fake",
            "misleading": "fake",
            "partially-true": "fake",  # Conservative: treat as fake if not fully true
            "mostly-true": "real",
            "true": "real",
        },
    },
    "Africa Check": {
        "base_url": "https://africacheck.org",
        "archive_path": "/search?q=uganda",
        "article_selector": "div.article-item",
        "title_selector": "h3.article-title a",
        "content_selector": "div.article-summary",
        "verdict_selector": "span.rating-tag",
        "date_selector": "span.article-date",
        "link_selector": "a.article-link",
        "verdict_map": {
            "false": "fake",
            "incorrect": "fake",
            "misleading": "fake",
            "correct": "real",
            "true": "real",
        },
    },
    "Dubawa": {
        "base_url": "https://dubawa.org",
        "archive_path": "/fact-checks",
        "article_selector": "article.fact-check",
        "title_selector": "h2.check-headline a",
        "content_selector": "div.claim",
        "verdict_selector": "span.verdict",
        "date_selector": "time.publish-date",
        "link_selector": "a.check-url",
        "verdict_map": {
            "false": "fake",
            "misleading": "fake",
            "false claim": "fake",
            "correct": "real",
            "true": "real",
        },
    },
}


def parse_date_string(date_str: str) -> Optional[str]:
    """
    Parse various date formats and return YYYY-MM-DD format.
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
    Infer category from claim text.
    """
    text = (title + " " + content).lower()

    categories = {
        "politics": ["election", "vote", "politician", "parliament", "president", "minister"],
        "health": ["vaccine", "covid", "disease", "health", "doctor", "hospital", "malaria"],
        "economy": ["money", "bank", "trade", "business", "price", "economy", "market"],
        "society": ["social", "community", "people", "person", "family", "women", "children"],
        "technology": ["technology", "digital", "internet", "software"],
        "environment": ["environment", "climate", "nature", "forest", "water"],
    }

    for category, keywords in categories.items():
        if any(keyword in text for keyword in keywords):
            return category

    return "general"


def fetch_claims_from_factchecker(
    checker_name: str,
    checker_config: dict,
    max_articles: int = 5000,
) -> list[dict]:
    """
    Fetch fact-checked false claims from a fact-checker.
    """
    claims = []
    seen_titles = set()

    logger.info(f"Starting collection from {checker_name}...")

    try:
        url = checker_config["base_url"] + checker_config["archive_path"]
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, "html.parser")
        check_elements = soup.select(checker_config["article_selector"])

        logger.info(f"Found {len(check_elements)} fact-checks on {checker_name}")

        for idx, elem in enumerate(check_elements):
            if len(claims) >= max_articles:
                break

            try:
                title_elem = elem.select_one(checker_config["title_selector"])
                content_elem = elem.select_one(checker_config["content_selector"])
                verdict_elem = elem.select_one(checker_config["verdict_selector"])
                date_elem = elem.select_one(checker_config["date_selector"])
                link_elem = elem.select_one(checker_config["link_selector"])

                if not title_elem or not verdict_elem:
                    continue

                title = title_elem.get_text(strip=True)
                title_hash = hash(title)
                if title_hash in seen_titles:
                    continue
                seen_titles.add(title_hash)

                content = content_elem.get_text(strip=True) if content_elem else title
                verdict = verdict_elem.get_text(strip=True).lower()
                label = checker_config["verdict_map"].get(verdict, "fake")  # Default to fake if uncertain
                date_str = date_elem.get_text(strip=True) if date_elem else datetime.now().strftime("%Y-%m-%d")
                date = parse_date_string(date_str) or datetime.now().strftime("%Y-%m-%d")
                url = link_elem.get("href") if link_elem else ""
                if url and not url.startswith("http"):
                    url = urljoin(checker_config["base_url"], url)

                # Only add if it's a FALSE/MISLEADING claim (label="fake")
                if label == "fake":
                    claims.append({
                        "id": len(claims) + 1,
                        "title": title,
                        "content": content[:1000],
                        "source": "Viral claim / Social media",
                        "url": url,
                        "date": date,
                        "category": extract_category(title, content),
                        "label": "fake",
                        "country": "Uganda",
                        "language": "en",
                        "verification_status": "fact_checked",
                        "fact_check_source": f"{checker_name} Fact-Check",
                    })

            except Exception as e:
                logger.debug(f"Error parsing claim {idx + 1} from {checker_name}: {e}")
                continue

        logger.info(f"Collected {len(claims)} false claims from {checker_name}")

    except requests.RequestException as e:
        logger.error(f"Failed to fetch from {checker_name}: {e}")

    return claims


def main():
    parser = argparse.ArgumentParser(
        description="Collect fake/misleading claims from fact-checkers."
    )
    parser.add_argument(
        "--sources",
        type=str,
        default="PesaCheck,Africa Check,Dubawa",
        help="Comma-separated fact-checker names",
    )
    parser.add_argument(
        "--max-articles",
        type=int,
        default=5000,
        help="Max claims per fact-checker",
    )
    parser.add_argument(
        "--country",
        type=str,
        default="Uganda",
        help="Filter by country",
    )
    parser.add_argument(
        "--output",
        type=str,
        default="uganda_fake_news_verified.csv",
        help="Output CSV file",
    )
    args = parser.parse_args()

    checker_names = [name.strip() for name in args.sources.split(",")]
    all_claims = []

    for checker_name in checker_names:
        if checker_name not in FACT_CHECKERS:
            logger.warning(f"Unknown fact-checker: {checker_name}. Skipping.")
            continue

        claims = fetch_claims_from_factchecker(
            checker_name,
            FACT_CHECKERS[checker_name],
            max_articles=args.max_articles,
        )
        all_claims.extend(claims)

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
        writer.writerows(all_claims)

    logger.info(f"Wrote {len(all_claims)} false claims to {output_path}")


if __name__ == "__main__":
    main()


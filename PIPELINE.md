# Uganda News Dataset Collection Pipeline

This pipeline collects **real Uganda news articles** from verified outlets and **fake/misleading reports** from fact-checking organizations, then exports them as labeled CSV files for misinformation research.

## Data Sources

### Real News Sources (Ugandan Media Outlets)
- **Daily Monitor** (dailymonitor.co.ug) – Major Ugandan daily newspaper
- **New Vision** (newvision.co.ug) – Government-aligned major daily
- **The Observer** (observer.ug) – Independent weekly newspaper
- **NTV Uganda** (ntvuganda.co.ug) – Television news network
- **Nile Post** (nilepost.co.ug) – Online news portal
- **Urban TV** (urbantv.co.ug) – Urban-focused media
- **UBC** (ubcmedia.ug) – Radio and digital news
- **ChimpReports** (chimpreports.com) – Digital news outlet

### Fact-Checking & Misinformation Sources
- **PesaCheck** (pesacheck.org) – East African fact-checking platform covering Uganda
- **Africa Check** (africacheck.org) – Pan-African fact-checking organization
- **Dubawa** (dubawa.org) – African fact-checking network (covers Uganda)
- **Social Media Archives** – Archived claims from Facebook, WhatsApp, Twitter

## Dataset Structure

The final CSVs contain these fields:

```
id,title,content,source,url,date,category,label,country,language,verification_status,fact_check_source
```

### Fields Explained
- `id` – Unique identifier
- `title` – Article headline
- `content` – Article body or summary (first 500–1000 characters)
- `source` – Original publication or origin
- `url` – Link to original article (when available)
- `date` – Publication date (YYYY-MM-DD format)
- `category` – Topic (politics, health, business, technology, agriculture, etc.)
- `label` – "real" or "fake"
- `country` – Uganda
- `language` – en (English)
- `verification_status` – "verified", "fact_checked", "unverified_claim", "retracted"
- `fact_check_source` – Which organization verified it (if applicable)

## Collection Methods

### Method 1: Web Scraping Real News

Scrape articles from Ugandan news outlets using `requests` + `BeautifulSoup`:

```python
python scripts/collect_real_news.py --outlet "Daily Monitor" --max-articles 5000
```

### Method 2: Fact-Checking Organization API/Archives

Collect verified fake claims and fact-checks from PesaCheck, Africa Check, Dubawa:

```python
python scripts/collect_fake_news_from_factcheckers.py --organization "PesaCheck" --max-articles 5000
```

### Method 3: Social Media Misinformation Archives

Collect documented false claims from WhatsApp, Facebook, Twitter (archived):

```python
python scripts/collect_social_media_claims.py --platform "WhatsApp" --max-articles 5000
```

### Method 4: Manual Verification & Labeling

For high-quality datasets, manually review and label scraped articles:

```python
python scripts/manual_verification_tool.py --input raw_articles.csv --output verified_articles.csv
```

## Complete Pipeline (All-in-One)

Run the full collection and export workflow:

```bash
python scripts/full_pipeline.py \
  --real-sources "Daily Monitor,New Vision,The Observer" \
  --fake-sources "PesaCheck,Africa Check" \
  --output-dir data/ \
  --real-count 20000 \
  --fake-count 20000
```

This will:
1. Scrape real news from specified Ugandan outlets
2. Collect fact-checked false claims from PesaCheck/Africa Check
3. Parse and clean the articles
4. Label and verify each entry
5. Export two CSVs:
   - `uganda_real_news_verified.csv`
   - `uganda_fake_news_verified.csv`

## Output Files

After running the pipeline, you will have:

```
data/
├���─ uganda_real_news_verified.csv       (20,000+ real articles)
├── uganda_fake_news_verified.csv       (20,000+ fake/misleading articles)
├── collection_log.txt                  (dates, sources, count)
└── verification_report.json            (quality metrics and source breakdown)
```

## CSV Format Example

```csv
id,title,content,source,url,date,category,label,country,language,verification_status,fact_check_source
1,"Government launches digital ID drive","Officials said the programme would improve service delivery...",Daily Monitor,https://dailymonitor.co.ug/article/123,2024-05-12,politics,real,Uganda,en,verified,Daily Monitor Editorial Standards
2,"President plans floating capital city","A viral WhatsApp message claimed the president secretly...",WhatsApp viral claim,https://archive.example.com/claim/456,2024-05-13,politics,fake,Uganda,en,fact_checked,PesaCheck Verification #UG-2024-0456
```

## Installation & Requirements

```bash
pip install -r requirements.txt
```

See `requirements.txt` for all dependencies.

## Legal & Ethical Guidelines

- **Respect robots.txt** – Follow website scraping policies
- **Attribution** – Always cite the original source
- **Fair Use** – Use snippets/summaries, not full articles without permission
- **Fact-Check Accuracy** – Only label as "fake" if independently verified by established fact-checkers
- **Privacy** – Do not include personal identifiable information (PII)
- **Licensing** – Check individual outlet licenses before republishing data

## Running the Collection

1. Clone or fork this repository
2. Install dependencies: `pip install -r requirements.txt`
3. Run the desired collection script (see examples above)
4. Check `data/` directory for output CSVs
5. Review `verification_report.json` for quality metrics

## Notes

- Real news collection depends on outlet availability and scraping permissions
- Fact-check data is more reliable but may be smaller in volume
- Some articles may require manual labeling for accuracy
- The pipeline retries failed requests and logs errors for debugging
- Estimated collection time: 2–6 hours depending on network speed and source availability

## Support

For issues, missing sources, or data quality questions, open an issue or contact the maintainer.


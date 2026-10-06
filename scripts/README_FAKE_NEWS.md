# Uganda News Dataset - Fake News Collector (from Fact-Checkers)

Collects verified false claims and fact-checks from PesaCheck, Africa Check, and Dubawa,
then exports them to CSV with proper labeling and verification sources.

## Usage

```bash
python collect_fake_news_from_factcheckers.py \
  --sources "PesaCheck,Africa Check,Dubawa" \
  --max-articles 5000 \
  --country Uganda \
  --output uganda_fake_news_verified.csv
```

Parameters:
- `--sources` – Comma-separated fact-checker names (default: all)
- `--max-articles` – Maximum claims to collect per source (default: 5000)
- `--country` – Filter by country (default: Uganda)
- `--output` – Output CSV file path

## Supported Fact-Checkers

### 1. PesaCheck (pesacheck.org)
- East African fact-checking platform
- Covers Uganda extensively
- Provides verdict tags: FALSE, MISLEADING, PARTIALLY TRUE, TRUE
- Focus: Elections, COVID-19, politics, economics, health

### 2. Africa Check (africacheck.org)
- Pan-African fact-checking organization
- Large archive of verified false claims
- Detailed fact-check reports with evidence
- Focus: Politics, economics, health, governance

### 3. Dubawa (dubawa.org)
- African fact-checking network
- Covers misinformation in African languages
- Covers Uganda election misinformation
- Focus: Elections, social media claims, COVID-19

## Collection Method

1. **Scrape fact-check archives** – Query each organization's published fact-checks
2. **Extract verdict** – Parse fact-checker's conclusion (FALSE, MISLEADING, etc.)
3. **Get original claim** – Extract the false statement being checked
4. **Label as "fake"** – Mark as false/misleading based on fact-checker verdict
5. **Cite fact-checker** – Record which organization verified it
6. **Export to CSV** – Save with proper attribution

## Output CSV Columns

```
id, title, content, source, url, date, category, label, country, language, verification_status, fact_check_source
```

## Example Output

```
1,"President announces ban on cryptocurrency","A viral claim stated that President Museveni banned all cryptocurrency trading in Uganda...",Social Media,https://pesacheck.org/fact-checks/123,2024-03-15,economy,fake,Uganda,en,fact_checked,PesaCheck Fact-Check #UG-2024-0123
2,"Vaccine causes infertility in women","A widely shared WhatsApp message falsely claimed that COVID-19 vaccines make women infertile...",WhatsApp rumor,https://africacheck.org/fact-checks/456,2024-02-20,health,fake,Uganda,en,fact_checked,Africa Check Verification
```

## Features

- **Automated scraping** – Fetches latest fact-checks from organization websites
- **Verdict parsing** – Correctly identifies FALSE/MISLEADING claims
- **Claim extraction** – Isolates the original false statement
- **Source attribution** – Links back to original fact-check report
- **Date filtering** – Collects recent and historical claims
- **Deduplication** – Avoids duplicate claims across organizations
- **Error handling** – Retries failed requests and logs issues

## Notes

- Fact-checks provide **high-confidence labeling** (verified by experts)
- Each claim is **independently verified** by established organizations
- **Source attribution** is critical for legal and ethical compliance
- Some fact-checks may have regional scope (East Africa, Pan-Africa)
- The pipeline respects each organization's terms of service

## CSV Format

Each row represents a verified false/misleading claim from a fact-checker:

| Field | Example |
|-------|----------|
| `id` | 1 |
| `title` | "President announces ban on cryptocurrency" |
| `content` | "A viral claim stated that..." |
| `source` | "Social Media" or "WhatsApp rumor" |
| `url` | https://pesacheck.org/fact-checks/123 |
| `date` | 2024-03-15 |
| `category` | economy |
| `label` | fake |
| `country` | Uganda |
| `language` | en |
| `verification_status` | fact_checked |
| `fact_check_source` | PesaCheck Fact-Check #UG-2024-0123 |

## Legal & Ethical Compliance

- ✅ All fact-checks are **public, published work**
- ✅ We **cite and link** to original fact-checks
- ✅ We use **summaries, not full reports** (fair use)
- ✅ We attribute to fact-checking organizations
- ✅ No personal data or private information is included
- ✅ Respects each organization's licensing (typically CC-BY or open)

## Troubleshooting

- **Connection timeout**: Check internet connection; script will retry
- **No results from a source**: Outlet may have changed structure; file an issue
- **Duplicate entries**: Deduplication runs automatically; check CSV for duplicates


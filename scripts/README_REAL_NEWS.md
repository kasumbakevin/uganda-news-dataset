# Uganda News Dataset - Real News Collector

Collects real news articles from Ugandan media outlets and exports to CSV.
Supports multiple outlets with configurable article limits and date ranges.

## Usage

```bash
python collect_real_news.py \
  --outlets "Daily Monitor,New Vision,The Observer" \
  --max-articles 5000 \
  --start-date 2023-01-01 \
  --end-date 2024-12-31 \
  --output uganda_real_news_verified.csv
```

Parameters:
- `--outlets` – Comma-separated list of news outlet names
- `--max-articles` – Maximum articles to collect per outlet (default: 5000)
- `--start-date` – Filter articles after this date (YYYY-MM-DD)
- `--end-date` – Filter articles before this date (YYYY-MM-DD)
- `--output` – Output CSV file path

## Supported Outlets

- Daily Monitor (dailymonitor.co.ug)
- New Vision (newvision.co.ug)
- The Observer (observer.ug)
- NTV Uganda (ntvuganda.co.ug)
- Nile Post (nilepost.co.ug)
- Urban TV (urbantv.co.ug)
- ChimpReports (chimpreports.com)
- UBC Media (ubcmedia.ug)

## Features

- Respects robots.txt and scraping policies
- Retries failed requests with exponential backoff
- Extracts title, content, date, category, source URL
- Labels all articles as "real" with verification_status="verified"
- Logs progress and errors
- Deduplicates articles by title hash

## Output CSV Columns

```
id, title, content, source, url, date, category, label, country, language, verification_status, fact_check_source
```

## Example Output

```
1,"Government launches digital ID drive","Officials said the programme...",Daily Monitor,https://dailymonitor.co.ug/...,2024-05-12,politics,real,Uganda,en,verified,Daily Monitor Editorial Standards
2,"Uganda secures World Bank funding for roads","The Ministry of Works announced...",New Vision,https://newvision.co.ug/...,2024-05-11,business,real,Uganda,en,verified,New Vision Editorial Standards
```

## Notes

- Some outlets may require additional parsing adjustments
- Date extraction may vary by outlet HTML structure
- Articles are trimmed to 1000 characters for CSV consistency
- If an outlet is unreachable, the script logs the error and continues with others


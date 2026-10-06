# Uganda News Dataset Generator

This repository contains a generator for a synthetic Uganda news dataset designed for experimentation in fake news detection and misinformation classification.

Important:
- This is a synthetic benchmark dataset, not a verified real-world archive of Uganda news.
- It is intended for testing pipelines, training prototypes, and research experiments.
- Do not treat it as factual reporting or a source of verified news.

## Dataset structure

The script creates two CSV files in the `data/` directory:
- `uganda_real_news.csv` — 20,000+ records labeled as real
- `uganda_fake_news.csv` — 20,000+ records labeled as fake

Each record contains:
- `id`
- `title`
- `content`
- `source`
- `date`
- `category`
- `label`
- `country`
- `language`
- `url`
- `article_type`

## Generate the files

Run:

```bash
python scripts/generate_uganda_news_dataset.py --real-count 20000 --fake-count 20000
```

This creates the CSVs under `data/`.

## Notes

For a real research project, replace this synthetic material with data from verified sources such as:
- PesaCheck
- Africa Check
- Dubawa
- Ugandan national media archives
- licensed news APIs


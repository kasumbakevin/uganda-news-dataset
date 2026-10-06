#!/bin/bash

# Complete Uganda News Dataset Collection Pipeline
# Collects real news and fake news from verified sources

echo "=== Uganda News Dataset Collection Pipeline ==="
echo ""

# Create directories
mkdir -p data logs

echo "Step 1: Collecting real news from Ugandan outlets..."
python scripts/collect_real_news.py \
  --outlets "Daily Monitor,New Vision,The Observer" \
  --max-articles 6667 \
  --output data/uganda_real_news_verified.csv \
  2>&1 | tee logs/real_news_collection.log

echo ""
echo "Step 2: Collecting fake news from fact-checkers..."
python scripts/collect_fake_news_from_factcheckers.py \
  --sources "PesaCheck,Africa Check,Dubawa" \
  --max-articles 6667 \
  --output data/uganda_fake_news_verified.csv \
  2>&1 | tee logs/fake_news_collection.log

echo ""
echo "Step 3: Combining and verifying datasets..."
python scripts/combine_and_verify.py \
  --real data/uganda_real_news_verified.csv \
  --fake data/uganda_fake_news_verified.csv \
  --output data/uganda_news_dataset_combined.csv \
  2>&1 | tee logs/combine_verify.log

echo ""
echo "=== Collection Complete ==="
echo "Output files:"
ls -lh data/*.csv
echo ""
echo "Logs:"
ls -lh logs/*.log


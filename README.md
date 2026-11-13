# Basic-Webscraping

Three small, independent scraping/NLP scripts.

## How to run

```bash
pip install -r requirements.txt
```

- `Real-Time Price Tracker & Alert System.py` — fetches a product page with
  requests/BeautifulSoup and prints an alert if the price is below a target.
  Edit the placeholder URL in the `__main__` block to a real product page
  first (the page must contain a `<span class="price">` element). The alert
  function is a print-only placeholder — see the TODO in the file.
- `Social Media Sentiment Miner.py` — averages TextBlob sentiment over Reddit
  search results. Needs real Reddit API credentials in the environment
  variables `REDDIT_CLIENT_ID`, `REDDIT_CLIENT_SECRET`, `REDDIT_USER_AGENT`.
- `AI-Powered News Trend Analyzer.py` — downloads a news article with
  newspaper3k and summarizes it with a transformers pipeline. The summarizer
  downloads a large model on first use.

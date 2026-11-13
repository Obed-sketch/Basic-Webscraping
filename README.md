# Basic-Webscraping

Three small, independent scraping/NLP scripts. All three were verified
running end-to-end in Nov 2026 (details per script below).

## How to run

```bash
pip install -r requirements.txt
```

### `Real-Time Price Tracker & Alert System.py` — VERIFIED

Fetches a product page with requests/BeautifulSoup, extracts the price,
and prints an alert if it is below target. The `__main__` block points
at a stable public demo target: **books.toscrape.com** (a sandbox shop
built for scraping practice), the book "A Light in the Attic". The
price finder tolerates common markup variants (`span.price`, any
element whose class contains "price" — the demo page uses
`<p class="price_color">` — then a currency pattern in the text), so it
also works on other product pages via `track_price(url, target)`. The
alert function remains a print-only placeholder (see the TODO in the
file). Verified output:

```
Current price: £51.77 (target: £55.00)
[PRICE ALERT] Price dropped to £51.77!
```

### `Social Media Sentiment Miner.py` — VERIFIED (demo mode)

Averages TextBlob sentiment polarity over Reddit search results for
('stocks', 'AMD'). The live path needs your own Reddit API credentials
in `REDDIT_CLIENT_ID`, `REDDIT_CLIENT_SECRET`, `REDDIT_USER_AGENT`.

Without credentials (or with `--demo`) it runs in **demo mode** over
the bundled **synthetic** sample posts in `sample_reddit_posts.csv`
(30 made-up posts; the 19 matching r/stocks + AMD are scored). The
computation is identical to the live path; only the data source
differs, and the output says so. Verified output:

```
DEMO MODE: scoring bundled synthetic sample posts (sample_reddit_posts.csv) -- not live Reddit data.
AMD Sentiment (demo, 19 sample posts): 0.0570602642971064
```

### `AI-Powered News Trend Analyzer.py` — VERIFIED

Downloads a news article with newspaper3k and summarizes it with a
transformers summarization pipeline. Needs no API key; the default
target is a public BBC News article (override with the `NEWS_URL`
environment variable). Verified output (Nov 2026, against the default
BBC article "Only one female scientist named in GCSEs, research
finds"; the publish date came back `None` — newspaper3k did not find
one in this page's metadata):

```
URL: https://www.bbc.com/news/articles/c69wzv5pg447o
Publish date: None
Keywords: ['scientist', 'marie', 'inge', 'geology', 'lehmann', 'seismologist', 'gcses', 'map', 'inner', 'tharp', 'ocrs', 'female', 'research', 'ocean', 'finds', 'named']
Summary:  Marie Tharp and Inge Lehmann feature in Cambridge OCR's A-level Geology . Tharp created the first map of the floor of the Atlantic ocean in the 1950s . Lehmann discovered the existence of the Earth's inner core in the 1930s .
```

Fixes and requirements (Nov 2026):

- `article.nlp()` is now called — without it, `article.keywords` was
  always empty.
- A `__main__` block was added (the file previously defined a function
  and did nothing when run).
- `transformers` is pinned `<5` in requirements.txt: v5 removed the
  `summarization` pipeline entirely.
- The summarizer model (~350 MB, distilbart) downloads on first use,
  and `article.nlp()` needs NLTK's `punkt`/`punkt_tab` data — the
  script fetches it if missing (with a direct-download fallback for
  proxied environments where NLTK's own downloader refuses the fetch).

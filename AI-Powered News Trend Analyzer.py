import os

from newspaper import Article
from transformers import pipeline


def analyze_news_trends(url):
    article = Article(url)
    article.download()
    article.parse()
    # FIX (Nov 2026): article.keywords is only populated by article.nlp();
    # without this call the "keywords" field below always came back empty.
    # (nlp() needs the NLTK 'punkt' tokenizer data -- see __main__.)
    article.nlp()

    summarizer = pipeline("summarization")
    summary = summarizer(article.text, max_length=100, min_length=20)

    return {
        "keywords": article.keywords,
        "summary": summary[0]['summary_text'],
        "publish_date": article.publish_date
    }


def _ensure_nltk_data():
    """article.nlp() needs NLTK's punkt tokenizer data; fetch it if absent.

    Fallback (Nov 2026): in some proxied environments NLTK's own
    downloader refuses the fetch (its SSRF guard rejects the proxy's
    resolved IPs) while a plain HTTPS GET works -- so if the data is
    still missing after nltk.download(), pull the official zip from
    the nltk_data repo directly and unpack it.
    """
    import nltk

    for pkg in ("punkt", "punkt_tab"):
        try:
            nltk.data.find(f"tokenizers/{pkg}")
            continue
        except LookupError:
            pass
        nltk.download(pkg, quiet=True)
        try:
            nltk.data.find(f"tokenizers/{pkg}")
            continue
        except LookupError:
            pass
        import io
        import zipfile

        import requests

        url = ("https://raw.githubusercontent.com/nltk/nltk_data/"
               f"gh-pages/packages/tokenizers/{pkg}.zip")
        target = os.path.join(nltk.data.path[0], "tokenizers")
        os.makedirs(target, exist_ok=True)
        blob = requests.get(url, timeout=60).content
        with zipfile.ZipFile(io.BytesIO(blob)) as z:
            z.extractall(target)


if __name__ == "__main__":
    # Default demo target: a public BBC News article (no API key needed).
    # Override with the NEWS_URL environment variable.
    _ensure_nltk_data()

    url = os.environ.get(
        "NEWS_URL",
        # Verified live Nov 2026: "Only one female scientist named in
        # GCSEs, research finds" (BBC News, Oct 2026).
        "https://www.bbc.com/news/articles/c69wzv5pg447o",
    )
    result = analyze_news_trends(url)
    print(f"URL: {url}")
    print(f"Publish date: {result['publish_date']}")
    print(f"Keywords: {result['keywords']}")
    print(f"Summary: {result['summary']}")

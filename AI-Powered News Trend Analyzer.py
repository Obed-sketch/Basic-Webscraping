from newspaper import Article
from transformers import pipeline

def analyze_news_trends(url):
    article = Article(url)
    article.download()
    article.parse()
    
    summarizer = pipeline("summarization")
    summary = summarizer(article.text, max_length=100)
    
    return {
        "keywords": article.keywords,
        "summary": summary[0]['summary_text'],
        "publish_date": article.publish_date
    }

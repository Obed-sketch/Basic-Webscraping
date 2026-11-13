import csv
import os
import sys

import praw
from textblob import TextBlob

# Credentials are read from the environment. The placeholder defaults keep the
# file importable but cannot authenticate -- set REDDIT_CLIENT_ID,
# REDDIT_CLIENT_SECRET and REDDIT_USER_AGENT to real values to run it.
# (A credential-like value was previously hard-coded on this line; it has been
# removed. If it was a real Reddit secret, rotate it in the Reddit app prefs.)
reddit = praw.Reddit(
    client_id=os.environ.get('REDDIT_CLIENT_ID', 'YOUR_ID'),
    client_secret=os.environ.get('REDDIT_CLIENT_SECRET', 'YOUR_SECRET'),
    user_agent=os.environ.get('REDDIT_USER_AGENT', 'YOUR_USER_AGENT'),
)

def get_sentiment(subreddit, keyword):
    submissions = reddit.subreddit(subreddit).search(keyword, limit=100)
    sentiments = []

    for submission in submissions:
        analysis = TextBlob(submission.title)
        sentiments.append(analysis.sentiment.polarity)

    if not sentiments:
        # REPAIR: previously this divided by len(sentiments) unconditionally
        # and crashed with ZeroDivisionError when a search returned nothing.
        return 0.0
    return sum(sentiments)/len(sentiments)


def get_sentiment_demo(subreddit, keyword, path=None):
    """DEMO MODE (added Nov 2026): the same average-polarity computation
    as get_sentiment(), but over the bundled SYNTHETIC sample posts in
    sample_reddit_posts.csv instead of live Reddit. The sample posts
    are made up -- the result demonstrates the pipeline only and is not
    real Reddit sentiment."""
    if path is None:
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                            'sample_reddit_posts.csv')
    with open(path, newline='', encoding='utf-8') as f:
        rows = [r for r in csv.DictReader(f)
                if r['subreddit'] == subreddit and r['keyword'] == keyword]
    if not rows:
        return 0.0, 0
    sentiments = [TextBlob(r['title']).sentiment.polarity for r in rows]
    return sum(sentiments) / len(sentiments), len(rows)


def _credentials_configured():
    return all([
        os.environ.get('REDDIT_CLIENT_ID', 'YOUR_ID') != 'YOUR_ID',
        os.environ.get('REDDIT_CLIENT_SECRET', 'YOUR_SECRET') != 'YOUR_SECRET',
        os.environ.get('REDDIT_USER_AGENT', 'YOUR_USER_AGENT') != 'YOUR_USER_AGENT',
    ])


if __name__ == '__main__':
    if '--demo' in sys.argv or not _credentials_configured():
        # Demo mode: no Reddit credentials needed (or explicitly asked
        # for). Live mode requires real credentials in the environment
        # variables named at the top of this file.
        print("DEMO MODE: scoring bundled synthetic sample posts "
              "(sample_reddit_posts.csv) -- not live Reddit data.")
        avg, n = get_sentiment_demo('stocks', 'AMD')
        print(f"AMD Sentiment (demo, {n} sample posts): {avg}")
    else:
        print(f"AMD Sentiment: {get_sentiment('stocks', 'AMD')}")

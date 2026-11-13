import os

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

if __name__ == '__main__':
    print(f"AMD Sentiment: {get_sentiment('stocks', 'AMD')}")

import praw
from textblob import TextBlob

reddit = praw.Reddit(client_id='YOUR_ID', client_secret='YOUR_SECRET')

def get_sentiment(subreddit, keyword):
    submissions = reddit.subreddit(subreddit).search(keyword, limit=100)
    sentiments = []
    
    for submission in submissions:
        analysis = TextBlob(submission.title)
        sentiments.append(analysis.sentiment.polarity)
    
    return sum(sentiments)/len(sentiments)

print(f"AMD Sentiment: {get_sentiment('stocks', 'AMD')}")

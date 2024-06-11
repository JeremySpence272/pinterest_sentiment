import praw
from textblob import TextBlob
import csv

import os

load_dotenv()  # take environment variables from .env.

client_secret = os.getenv('REDDIT_SECRET')

# Set up Reddit connection using your credentials
reddit = praw.Reddit(
    client_id='sa9ehcf5cgYVzCb-DumhOA',
    client_secret=client_secret,
    user_agent='python:pinterest_sentiment:v1.0 (by u/Js27212509)'
)

# Access the subreddit
subreddit = reddit.subreddit('pinterest')

# Open a CSV file to write the negative comments
with open('negative_comments.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    # Include a header for the number of upvotes
    writer.writerow(['Sentiment Polarity', 'Upvotes', 'Comment', 'Post URL'])

    # Fetch top posts from the last year
    for post in subreddit.top(time_filter='year', limit=500):  # You can adjust the limit as needed
        submission = reddit.submission(id=post.id)
        submission.comments.replace_more(limit=0)  # Fetch all comments
        for comment in submission.comments.list():
            blob = TextBlob(comment.body)
            if blob.sentiment.polarity < 0:
                # Write the negative sentiment comments to the CSV file, including upvotes
                writer.writerow([blob.sentiment.polarity, comment.score, comment.body, post.url])

print("CSV file has been created with negative comments and their upvote counts.")

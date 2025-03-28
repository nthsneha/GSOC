import praw
import csv

CID="udJjQk-xYDt5srtizFMS0w"
CS="WQeTGncFU0tKdXK563WcNKDzhBD53w"
UA="MyRedditBot/1.0"

reddit=praw.Reddit(
    client_id=CID,
    client_secret=CS,
    user_agent=UA,
)

#print("Reddit API authenticated successfully!")

subreddits=["depression", "mentalhealth", "SuicideWatch", "addiction", "SuicidalThots", "loneliness"]
keywords=["suicidal", "depressed", "overwhelmed", "addiction help", "loneliness", "suicide", "want to kill myself"]

OP_FILE= "reddit_posts.csv"

with open(OP_FILE, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)

    writer.writerow(["subreddit", "title", "content", "upvotes", "comments", "url"])

    # Fetch Posts
    for subreddit in subreddits:
        print(f"\n Searching in r/{subreddit}")
        sub = reddit.subreddit(subreddit)

        for keyword in keywords:
            print(f" Searching for '{keyword}'")
            for post in sub.search(keyword, limit=10):
                writer.writerow([
                    subreddit,
                    post.title.replace(",", " "), 
                    post.selftext.replace(",", " "),
                    post.score,
                    post.num_comments,
                    post.url
                ])

print(f"\n Data saved to {OP_FILE}")


import praw
import csv
from dotenv import load_dotenv
import os


load_dotenv()


CID = os.getenv("CID")
CS = os.getenv("CS")
UA = os.getenv("UA")

reddit=praw.Reddit(
    client_id=CID,
    client_secret=CS,
    user_agent=UA,
)


subreddits = [
    "depression", "mentalhealth", "SuicideWatch", "addiction", "SuicidalThots", "loneliness",
    "Anxiety", "BPD", "OCD", "bipolar"]

keywords = [
    "suicidal",
    "depressed",
    "overwhelmed",
    "addiction help",
    "loneliness",
    "suicide",
    "want to kill myself",
    "can't go on",
    "life is meaningless",
    "I'm tired of everything",
    "nobody cares",
    "I feel so alone",
    "self-harm",
    "cutting myself",
    "I want to disappear",
    "everything hurts",
    "I give up",
    "I'm broken",
    "need help",
    "crying every night",
    "I hate my life",
    "anxiety attack",
    "panic attack",
    "I feel empty",
    "I want the pain to end",
    "nobody understands me",
    "I feel like a burden",
    "feeling worthless"
    ]

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


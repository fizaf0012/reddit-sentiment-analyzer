import praw

# Initialize Reddit client
reddit = praw.Reddit(
    client_id="OeCiJClHhS41I8TFYKfyUA",
    client_secret="39mjKuAQ12ctvaPPq9jg45VN0TBEyg",
    user_agent="sentiment-analysis-app"
)

def fetch_posts(subreddit: str, limit: int = 5):
    """Fetch top posts from a subreddit"""
    try:
        posts = []
        for submission in reddit.subreddit(subreddit).hot(limit=limit):
            posts.append({
                "title": submission.title,
                "text": submission.selftext,
                "score": submission.score,
                "url": submission.url
            })
        return posts
    except Exception as e:
        raise RuntimeError(f"Error fetching subreddit data: {e}")

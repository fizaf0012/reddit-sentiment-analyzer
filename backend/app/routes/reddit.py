from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.reddit_client import fetch_posts
from app.sentiment import analyze_sentiment
from app.database import get_db
from app import models

router = APIRouter(
    prefix="/reddit",
    tags=["Reddit"]
)

# ------------------------------------------------
# FETCH AND ANALYZE POSTS FROM REDDIT
# ------------------------------------------------
@router.get("/fetch/{subreddit}")
def fetch_and_analyze(subreddit: str, limit: int = 5, db: Session = Depends(get_db)):
    try:
        posts = fetch_posts(subreddit, limit=limit)
        analyzed = []

        for post in posts:
            # Run sentiment analysis
            sentiment = analyze_sentiment(
                post.get("title", "") + " " + post.get("text", "")
            )

            # Save post to DB
            db_post = models.RedditPost(
                subreddit=subreddit,
                title=post.get("title", ""),
                text=post.get("text", ""),
                score=post.get("score", 0),
                url=post.get("url", ""),
                sentiment=sentiment.get("sentiment", "neutral"),
                emotion=sentiment.get("emotion", "none"),
                confidence=sentiment.get("confidence", 0.0)
            )

            db.add(db_post)
            db.commit()
            db.refresh(db_post)

            analyzed.append({
                "id": db_post.id,
                "title": db_post.title,
                "text": db_post.text,
                "score": db_post.score,
                "sentiment": db_post.sentiment,
                "emotion": db_post.emotion,
                "confidence": db_post.confidence,
                "url": db_post.url
            })

        return {"subreddit": subreddit, "results": analyzed}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


# ------------------------------------------------
# FETCH SAVED POSTS HISTORY FROM DATABASE
# ------------------------------------------------
@router.get("/history/{subreddit}")
def get_history(subreddit: str, limit: int = 10, db: Session = Depends(get_db)):
    try:
        posts = (
            db.query(models.RedditPost)
            .filter(models.RedditPost.subreddit == subreddit)
            .order_by(models.RedditPost.created_at.desc())
            .limit(limit)
            .all()
        )

        # Convert ORM objects to dicts for JSON response
        results = [
            {
                "id": p.id,
                "subreddit": p.subreddit,
                "title": p.title,
                "text": p.text,
                "score": p.score,
                "sentiment": p.sentiment,
                "emotion": p.emotion,
                "confidence": p.confidence,
                "url": p.url,
                "created_at": p.created_at
            }
            for p in posts
        ]

        return {"subreddit": subreddit, "results": results}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

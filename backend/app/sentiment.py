from fastapi import APIRouter, HTTPException
from transformers import pipeline
from app import schemas

router = APIRouter(
    prefix="/sentiment",
    tags=["Sentiment Analysis"]
)

# ⚙️ Load HuggingFace emotion model once
# (loads DistilRoBERTa fine-tuned for emotion classification)
emotion_model = pipeline(
    "text-classification",
    model="j-hartmann/emotion-english-distilroberta-base",
    top_k=1
)

# ✅ Map detailed emotions to general sentiment
def map_to_polarity(emotion: str) -> str:
    if emotion.lower() in ["joy", "love"]:
        return "positive"
    elif emotion.lower() in ["anger", "sadness", "fear", "disgust"]:
        return "negative"
    else:
        return "neutral"


# ✅ Utility function for internal or API use
def analyze_sentiment(text: str) -> dict:
    if not text.strip():
        raise ValueError("Text cannot be empty")

    try:
        # Limit text length to prevent model overflow
        text = text[:500]

        # Run model
        result = emotion_model(text)[0][0]  # top result
        emotion = result["label"]
        confidence = float(result["score"])
        sentiment = map_to_polarity(emotion)

        return {
            "text": text,
            "emotion": emotion,
            "sentiment": sentiment,
            "confidence": confidence
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Sentiment analysis error: {e}")


# ✅ Endpoint for analyzing single text
@router.post("/analyze", response_model=schemas.SentimentResponse)
def analyze_text(text: str):
    try:
        return analyze_sentiment(text)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


# ✅ Endpoint for analyzing multiple texts
@router.post("/analyze_batch", response_model=schemas.BatchSentimentResponse)
def analyze_batch(texts: list[str]):
    if not texts:
        raise HTTPException(status_code=400, detail="Text list cannot be empty")

    try:
        results = [analyze_sentiment(text) for text in texts if text.strip()]
        return schemas.BatchSentimentResponse(results=results)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Batch analysis error: {e}")

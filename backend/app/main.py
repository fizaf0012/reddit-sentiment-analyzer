# backend/app/main.py
from fastapi import FastAPI
app = FastAPI(title="Reddit Sentiment Analyzer")

@app.get("/")
def root():
    return {"status": "ok"}

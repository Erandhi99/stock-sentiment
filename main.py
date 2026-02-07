from fastapi import FastAPI
from pymongo import MongoClient
from datetime import datetime

app = FastAPI()

# Database Connection
client = MongoClient("mongodb://localhost:27017/")
db = client.stock_sentiment_db
collection = db.posts

@app.get("/")
def home():
    return {"message": "Stock Sentiment API is running!"}

@app.get("/analysis/{symbol}")
def analyze_stock(symbol: str):
    # 1. Find last 50 posts for this stock
    posts_cursor = collection.find({"symbol": symbol.upper()}).sort("timestamp", -1).limit(50)
    posts = list(posts_cursor)

    if not posts:
        return {"error": "No data found for this stock"}

    # 2. Calculate Average Sentiment
    total_score = sum(p['sentiment'] for p in posts)
    avg_score = total_score / len(posts)

    # 3. Determine Human-Readable Verdict
    if avg_score > 0.05:
        verdict = "BULLISH (Optimistic) 🚀"
    elif avg_score < -0.05:
        verdict = "BEARISH (Pessimistic) 📉"
    else:
        verdict = "NEUTRAL 😐"

    return {
        "symbol": symbol.upper(),
        "sample_size": len(posts),
        "average_sentiment": round(avg_score, 4),
        "verdict": verdict,
        "latest_posts": [p['text'] for p in posts[:3]] # Show top 3 recent posts
    }
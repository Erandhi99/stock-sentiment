import time
import random
import datetime
import os
from pymongo import MongoClient
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# --- CONFIGURATION ---
# Set to TRUE to use fake data (Instant start). 
# Set to FALSE later when you have Reddit keys.
SIMULATION_MODE = True 

# Database Setup
client = MongoClient("mongodb://localhost:27017/")
db = client.stock_sentiment_db
collection = db.posts

# AI Setup
analyzer = SentimentIntensityAnalyzer()

# Simulation Tools (Fake tweets for testing)
fake_templates = [
    "I love {stock}, it's going to the moon! 🚀", 
    "{stock} is a disaster, selling everything.", 
    "Just bought more {stock}, holding forever.",
    "Why is {stock} dropping? Panic!",
    "{stock} earnings looking strong."
]
target_stocks = ["AAPL", "TSLA", "BTC", "NVDA"]

def get_real_reddit_data():
    # We will fill this in Phase 4!
    pass

def generate_fake_data():
    stock = random.choice(target_stocks)
    text = random.choice(fake_templates).format(stock=stock)
    return stock, text

print("--- Scraper Started ---")
print(f"Mode: {'SIMULATION' if SIMULATION_MODE else 'REAL REDDIT'}")

while True:
    try:
        if SIMULATION_MODE:
            symbol, text = generate_fake_data()
        else:
            # Placeholder for real logic later
            symbol, text = generate_fake_data()

        # 1. Analyze Sentiment (-1.0 to +1.0)
        scores = analyzer.polarity_scores(text)
        compound_score = scores['compound']

        # 2. Create the Document
        post_doc = {
            "symbol": symbol,
            "text": text,
            "sentiment": compound_score,
            "timestamp": datetime.datetime.utcnow()
        }

        # 3. Save to MongoDB
        collection.insert_one(post_doc)
        print(f"[{symbol}] Score: {compound_score} | Saved: {text}")

        # Sleep to simulate real-time traffic (2 seconds)
        time.sleep(2)

    except Exception as e:
        print(f"Error: {e}")
        time.sleep(5)
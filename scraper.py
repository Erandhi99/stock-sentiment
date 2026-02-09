import requests
import time
import datetime
import sys
from pymongo import MongoClient
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# --- CONFIGURATION ---
FINNHUB_KEY = "d64ui9pr01qqbln57gt0d64ui9pr01qqbln57gtg"

# The stocks you want to monitor
STOCKS = ["AAPL", "TSLA", "NVDA", "BTC", "AMZN", "MSFT"]

# 1. MongoDB Connection
try:
    client = MongoClient("mongodb://localhost:27017/")
    db = client.stock_sentiment_db
    collection = db.posts
    # Test connection
    client.admin.command('ping')
    print("✅ Successfully connected to MongoDB")
except Exception as e:
    print(f"❌ Could not connect to MongoDB: {e}")
    sys.exit(1)

# 2. AI Sentiment Engine Setup
analyzer = SentimentIntensityAnalyzer()

def fetch_and_analyze():
    """Fetches general market news and filters for our target stocks."""
    print(f"\n--- 📡 Fetching News: {datetime.datetime.now().strftime('%H:%M:%S')} ---")
    
    # Finnhub 'general' news category provides the latest market headlines
    url = f"https://finnhub.io/api/v1/news?category=general&token={FINNHUB_KEY}"
    
    try:
        response = requests.get(url)
        response.raise_for_status() # Check for HTTP errors
        news_list = response.json()
        
        saved_count = 0

        # We look through the latest news items
        for item in news_list:
            headline = item.get('headline', '')
            
            # Identify which of our target stocks are mentioned in the headline
            for symbol in STOCKS:
                if symbol in headline.upper():
                    
                    # A. AI Sentiment Analysis
                    # VADER returns a 'compound' score from -1 (Negative) to +1 (Positive)
                    scores = analyzer.polarity_scores(headline)
                    compound_score = scores['compound']
                    
                    # B. Prepare the MongoDB Document
                    doc = {
                        "symbol": symbol,
                        "text": headline,
                        "sentiment": compound_score,
                        "timestamp": datetime.datetime.utcnow(),
                        "source": item.get('source', 'Finnhub'),
                        "url": item.get('url', '')
                    }
                    
                    # C. Save to MongoDB (Preventing duplicates by checking headline)
                    if not collection.find_one({"text": headline}):
                        collection.insert_one(doc)
                        saved_count += 1
                        print(f"   ✨ Saved [{symbol}]: {headline[:60]}... (Score: {compound_score})")

        if saved_count == 0:
            print("   💤 No new relevant headlines found in this batch.")
        else:
            print(f"   💾 Added {saved_count} new analysis records to MongoDB.")

    except Exception as e:
        print(f"❌ Error during fetch: {e}")

# --- MAIN LOOP ---
if __name__ == "__main__":
    print(f"🚀 Scraper started! Monitoring: {', '.join(STOCKS)}")
    print("Press Ctrl+C to stop.")
    
    while True:
        fetch_and_analyze()
        # Finnhub free tier update frequency is good at 2-5 minutes
        print("\n😴 Sleeping for 2 minutes...")
        time.sleep(120)
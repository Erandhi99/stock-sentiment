The Concept: A system that scrapes Twitter/X or Reddit (r/wallstreetbets) for mentions of specific stocks, analyzes the sentiment (Positive/Negative) using Python AI libraries, and correlates it with live stock prices.

Key Features:
  Ingestion Engine: A Python script running in the background listening to live tweets.
  NLP Processor: Uses a library like VADER to score sentiment (-1 to +1).
  TimeSeries Collections: MongoDB has dedicated Time Series collections optimized for storing financial data efficiently.

Tech Stack: FastAPI, Motor (Async Mongo driver), TextBlob (NLP), yfinance.
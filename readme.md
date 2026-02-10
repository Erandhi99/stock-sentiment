# AI-Powered Stock Sentiment Analyzer

A real-time data pipeline that monitors financial news, performs NLP-based sentiment analysis, and serves market "verdicts" via a REST API.

## 🛠️ Tech Stack
- **Python**: Core logic and data processing.
- **FastAPI**: High-performance API framework.
- **MongoDB**: Document store for high-velocity news data.
- **VADER Sentiment**: Lexicon and rule-based sentiment analysis tool.
- **Finnhub API**: Real-time financial news source.

## 🚀 How it Works
1. **Ingestion**: The `scraper.py` script polls the Finnhub API for the latest market headlines.
2. **Analysis**: Each headline is processed by the VADER engine to calculate a sentiment score from -1.0 (Bearish) to +1.0 (Bullish).
3. **Storage**: Processed data is stored in MongoDB with timestamps to prevent duplication.
4. **Delivery**: The FastAPI server (`main.py`) aggregates the last 50 headlines for a specific stock to provide a real-time "Market Verdict."
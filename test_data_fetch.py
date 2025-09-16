#!/usr/bin/env python3
"""
Simple test to check if data fetching works
"""

import yfinance as yf
import pandas as pd
from datetime import datetime

print("=== Testing Data Fetch ===")

# Test basic yfinance functionality
try:
    print("Testing yfinance...")
    ticker = yf.Ticker("AAPL")
    data = ticker.history(period="5d")
    print(f"SUCCESS: Got {len(data)} days of AAPL data")
    print(f"Latest close: ${data['Close'].iloc[-1]:.2f}")
    
    # Test info
    info = ticker.info
    print(f"Company: {info.get('longName', 'N/A')}")
    print(f"Market Cap: ${info.get('marketCap', 0):,}")
    
except Exception as e:
    print(f"ERROR with yfinance: {e}")

def calculate_rsi(prices, window=14):
    """Simple RSI calculation"""
    delta = prices.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

# Test technical indicators
try:
    print("\nTesting technical indicators...")
    if len(data) > 5:
        data['SMA_5'] = data['Close'].rolling(window=5).mean()
        data['RSI'] = calculate_rsi(data['Close'])
        print(f"SUCCESS: Added technical indicators")
        print(f"Latest SMA(5): ${data['SMA_5'].iloc[-1]:.2f}")
    else:
        print("WARNING: Not enough data for indicators")
        
except Exception as e:
    print(f"ERROR with indicators: {e}")

print("=== Test Complete ===")
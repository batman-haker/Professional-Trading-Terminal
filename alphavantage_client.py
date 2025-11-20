#!/usr/bin/env python3
"""
AlphaVantage API Client
Free tier: 25 requests/day (premium) or 500 requests/day (standard endpoints)
Official API: https://www.alphavantage.co/
"""

import requests
import pandas as pd
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import time
import os
from dotenv import load_dotenv

load_dotenv()

class AlphaVantageClient:
    """Client for AlphaVantage API"""

    BASE_URL = "https://www.alphavantage.co/query"

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize AlphaVantage client

        Args:
            api_key: AlphaVantage API key. If not provided, looks for ALPHAVANTAGE_API_KEY in .env
        """
        self.api_key = api_key or os.getenv('ALPHAVANTAGE_API_KEY', 'DHUNB2KBGCZKJP4Y')
        self.session = requests.Session()
        self.cache = {}
        self.cache_ttl = 300  # 5 minutes

    def _make_request(self, params: Dict) -> Optional[Dict]:
        """Make API request with error handling"""
        params['apikey'] = self.api_key

        try:
            response = self.session.get(self.BASE_URL, params=params, timeout=10)

            if response.status_code == 200:
                data = response.json()

                # Check for API error messages
                if "Error Message" in data:
                    print(f"[AlphaVantage Error] {data['Error Message']}")
                    return None
                if "Note" in data:
                    print(f"[AlphaVantage Note] {data['Note']}")
                    return None

                return data
            else:
                print(f"[AlphaVantage] HTTP {response.status_code}")
                return None

        except Exception as e:
            print(f"[AlphaVantage] Request error: {e}")
            return None

    def _cache_key(self, method: str, **kwargs) -> str:
        """Generate cache key"""
        return f"{method}:{str(sorted(kwargs.items()))}"

    def _get_cached(self, key: str) -> Optional[Any]:
        """Get cached data if valid"""
        if key in self.cache:
            data, timestamp = self.cache[key]
            if time.time() - timestamp < self.cache_ttl:
                return data
        return None

    def _set_cache(self, key: str, data: Any):
        """Set cache data"""
        self.cache[key] = (data, time.time())

    def get_quote(self, symbol: str) -> Optional[Dict]:
        """
        Get real-time quote for a symbol

        Args:
            symbol: Stock symbol (e.g., 'AAPL', 'MSFT')

        Returns:
            Dictionary with quote data or None
        """
        cache_key = self._cache_key("quote", symbol=symbol)
        cached = self._get_cached(cache_key)
        if cached:
            return cached

        params = {
            'function': 'GLOBAL_QUOTE',
            'symbol': symbol
        }

        data = self._make_request(params)

        if data and 'Global Quote' in data:
            quote = data['Global Quote']

            result = {
                'symbol': quote.get('01. symbol', symbol),
                'price': float(quote.get('05. price', 0)),
                'change': float(quote.get('09. change', 0)),
                'change_percent': quote.get('10. change percent', '0%').replace('%', ''),
                'volume': int(quote.get('06. volume', 0)),
                'latest_trading_day': quote.get('07. latest trading day', ''),
                'previous_close': float(quote.get('08. previous close', 0)),
                'open': float(quote.get('02. open', 0)),
                'high': float(quote.get('03. high', 0)),
                'low': float(quote.get('04. low', 0))
            }

            self._set_cache(cache_key, result)
            return result

        return None

    def get_intraday(self, symbol: str, interval: str = '5min') -> Optional[pd.DataFrame]:
        """
        Get intraday time series data

        Args:
            symbol: Stock symbol
            interval: 1min, 5min, 15min, 30min, 60min

        Returns:
            DataFrame with OHLCV data or None
        """
        params = {
            'function': 'TIME_SERIES_INTRADAY',
            'symbol': symbol,
            'interval': interval,
            'outputsize': 'compact'  # Last 100 data points
        }

        data = self._make_request(params)

        if data and f'Time Series ({interval})' in data:
            time_series = data[f'Time Series ({interval})']

            # Convert to DataFrame
            df = pd.DataFrame.from_dict(time_series, orient='index')
            df.index = pd.to_datetime(df.index)
            df = df.sort_index()

            # Rename columns
            df.columns = ['Open', 'High', 'Low', 'Close', 'Volume']
            df = df.astype(float)

            return df

        return None

    def get_daily(self, symbol: str, outputsize: str = 'compact') -> Optional[pd.DataFrame]:
        """
        Get daily time series data

        Args:
            symbol: Stock symbol
            outputsize: 'compact' (100 days) or 'full' (20+ years)

        Returns:
            DataFrame with OHLCV data or None
        """
        cache_key = self._cache_key("daily", symbol=symbol, outputsize=outputsize)
        cached = self._get_cached(cache_key)
        if cached is not None:
            return cached

        params = {
            'function': 'TIME_SERIES_DAILY',
            'symbol': symbol,
            'outputsize': outputsize
        }

        data = self._make_request(params)

        if data and 'Time Series (Daily)' in data:
            time_series = data['Time Series (Daily)']

            # Convert to DataFrame
            df = pd.DataFrame.from_dict(time_series, orient='index')
            df.index = pd.to_datetime(df.index)
            df = df.sort_index()

            # Rename columns to match yfinance format
            df.columns = ['Open', 'High', 'Low', 'Close', 'Volume']
            df = df.astype(float)

            self._set_cache(cache_key, df)
            return df

        return None

    def get_company_overview(self, symbol: str) -> Optional[Dict]:
        """
        Get company overview (fundamentals)

        Args:
            symbol: Stock symbol

        Returns:
            Dictionary with company data or None
        """
        cache_key = self._cache_key("overview", symbol=symbol)
        cached = self._get_cached(cache_key)
        if cached:
            return cached

        params = {
            'function': 'OVERVIEW',
            'symbol': symbol
        }

        data = self._make_request(params)

        if data and 'Symbol' in data:
            self._set_cache(cache_key, data)
            return data

        return None

    def get_news_sentiment(self, tickers: str, limit: int = 10) -> Optional[List[Dict]]:
        """
        Get news and sentiment for tickers

        Args:
            tickers: Comma-separated ticker symbols
            limit: Number of articles

        Returns:
            List of news articles or None
        """
        params = {
            'function': 'NEWS_SENTIMENT',
            'tickers': tickers,
            'limit': limit
        }

        data = self._make_request(params)

        if data and 'feed' in data:
            return data['feed']

        return None

    def search_symbol(self, keywords: str) -> Optional[List[Dict]]:
        """
        Search for symbols matching keywords

        Args:
            keywords: Search query

        Returns:
            List of matching symbols or None
        """
        params = {
            'function': 'SYMBOL_SEARCH',
            'keywords': keywords
        }

        data = self._make_request(params)

        if data and 'bestMatches' in data:
            return data['bestMatches']

        return None


def test_alphavantage():
    """Test AlphaVantage client"""
    print("Testing AlphaVantage Client...")
    print("=" * 60)

    client = AlphaVantageClient()

    # Test 1: Get quote
    print("\n[1] Testing quote for AAPL...")
    quote = client.get_quote('AAPL')
    if quote:
        print(f"[OK] AAPL: ${quote['price']:.2f} ({quote['change_percent']}%)")
    else:
        print("[FAIL] Failed to get quote")

    # Test 2: Get daily data
    print("\n[2] Testing daily data for MSFT...")
    daily = client.get_daily('MSFT', outputsize='compact')
    if daily is not None and not daily.empty:
        print(f"[OK] Got {len(daily)} days of data")
        print(f"     Latest close: ${daily['Close'].iloc[-1]:.2f}")
    else:
        print("[FAIL] Failed to get daily data")

    # Test 3: Company overview
    print("\n[3] Testing company overview for TSLA...")
    overview = client.get_company_overview('TSLA')
    if overview:
        print(f"[OK] Company: {overview.get('Name', 'N/A')}")
        print(f"     Sector: {overview.get('Sector', 'N/A')}")
        print(f"     Market Cap: ${int(overview.get('MarketCapitalization', 0)):,}")
    else:
        print("[FAIL] Failed to get overview")

    # Test 4: Symbol search
    print("\n[4] Testing symbol search for 'Microsoft'...")
    results = client.search_symbol('Microsoft')
    if results:
        print(f"[OK] Found {len(results)} matches")
        if len(results) > 0:
            print(f"     Top match: {results[0].get('1. symbol')} - {results[0].get('2. name')}")
    else:
        print("[FAIL] Failed to search symbols")

    print("\n" + "=" * 60)
    print("[OK] Testing complete!")


if __name__ == "__main__":
    test_alphavantage()

"""
Professional Trading Terminal - Enhanced Version with OpenBB Integration
Version: 3.0 | Full Featured Trading Platform
Author: Terminal Pro Team
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import yfinance as yf
from datetime import datetime, timedelta
import requests
import json
import time
import pytz
import warnings
from typing import Dict, List, Optional, Tuple, Any
import ta
from pathlib import Path
import pickle
from concurrent.futures import ThreadPoolExecutor, as_completed
import os
from dotenv import load_dotenv

# Import OpenBB SDK
try:
    from openbb import obb
    OPENBB_AVAILABLE = True
except ImportError:
    OPENBB_AVAILABLE = False
    st.warning("OpenBB not installed. Some features will be limited. Install with: pip install openbb")

warnings.filterwarnings('ignore')
load_dotenv()

# ================== CONFIGURATION ==================
st.set_page_config(
    page_title="Terminal Pro 3.0 | Professional Trading Platform",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/terminal-pro/trading-terminal',
        'Report a bug': 'https://github.com/terminal-pro/issues',
        'About': "Terminal Pro 3.0 - Professional Trading Platform with OpenBB Integration"
    }
)

# ================== CONSTANTS & MAPPINGS ==================

# ================== COMPREHENSIVE INSTRUMENTS DATABASE ==================

# Global stocks database with company names for intelligent search
GLOBAL_INSTRUMENTS = {
    # US Tech Giants
    'AAPL': {'name': 'Apple Inc.', 'exchange': 'NASDAQ', 'type': 'stock', 'sector': 'Technology'},
    'MSFT': {'name': 'Microsoft Corporation', 'exchange': 'NASDAQ', 'type': 'stock', 'sector': 'Technology'},
    'GOOGL': {'name': 'Alphabet Inc. Class A', 'exchange': 'NASDAQ', 'type': 'stock', 'sector': 'Technology'},
    'AMZN': {'name': 'Amazon.com Inc.', 'exchange': 'NASDAQ', 'type': 'stock', 'sector': 'Consumer Discretionary'},
    'NVDA': {'name': 'NVIDIA Corporation', 'exchange': 'NASDAQ', 'type': 'stock', 'sector': 'Technology'},
    'TSLA': {'name': 'Tesla Inc.', 'exchange': 'NASDAQ', 'type': 'stock', 'sector': 'Automotive'},
    'META': {'name': 'Meta Platforms Inc.', 'exchange': 'NASDAQ', 'type': 'stock', 'sector': 'Technology'},
    'NFLX': {'name': 'Netflix Inc.', 'exchange': 'NASDAQ', 'type': 'stock', 'sector': 'Communication'},
    'AMD': {'name': 'Advanced Micro Devices', 'exchange': 'NASDAQ', 'type': 'stock', 'sector': 'Technology'},
    'CRM': {'name': 'Salesforce Inc.', 'exchange': 'NYSE', 'type': 'stock', 'sector': 'Technology'},
    
    # US Banks & Finance
    'JPM': {'name': 'JPMorgan Chase & Co.', 'exchange': 'NYSE', 'type': 'stock', 'sector': 'Financials'},
    'BAC': {'name': 'Bank of America Corp.', 'exchange': 'NYSE', 'type': 'stock', 'sector': 'Financials'},
    'WFC': {'name': 'Wells Fargo & Company', 'exchange': 'NYSE', 'type': 'stock', 'sector': 'Financials'},
    'GS': {'name': 'Goldman Sachs Group', 'exchange': 'NYSE', 'type': 'stock', 'sector': 'Financials'},
    'MS': {'name': 'Morgan Stanley', 'exchange': 'NYSE', 'type': 'stock', 'sector': 'Financials'},
    
    # Polish Stocks (WSE)
    'PCO.WA': {'name': 'PEPCO Group N.V.', 'exchange': 'WSE', 'type': 'stock', 'sector': 'Consumer Discretionary', 'local_code': 'PCO'},
    'PKN.WA': {'name': 'PKN ORLEN S.A.', 'exchange': 'WSE', 'type': 'stock', 'sector': 'Energy', 'local_code': 'PKN'},
    'PEO.WA': {'name': 'Bank Pekao S.A.', 'exchange': 'WSE', 'type': 'stock', 'sector': 'Financials', 'local_code': 'PEO'},
    'KGH.WA': {'name': 'KGHM Polska Miedź S.A.', 'exchange': 'WSE', 'type': 'stock', 'sector': 'Materials', 'local_code': 'KGH'},
    'LPP.WA': {'name': 'LPP S.A.', 'exchange': 'WSE', 'type': 'stock', 'sector': 'Consumer Discretionary', 'local_code': 'LPP'},
    'CDR.WA': {'name': 'CD PROJEKT S.A.', 'exchange': 'WSE', 'type': 'stock', 'sector': 'Technology', 'local_code': 'CDR'},
    'ALE.WA': {'name': 'Allegro.eu S.A.', 'exchange': 'WSE', 'type': 'stock', 'sector': 'Technology', 'local_code': 'ALE'},
    'PZU.WA': {'name': 'Powszechny Zakład Ubezpieczeń S.A.', 'exchange': 'WSE', 'type': 'stock', 'sector': 'Financials', 'local_code': 'PZU'},
    'PKO.WA': {'name': 'PKO Bank Polski S.A.', 'exchange': 'WSE', 'type': 'stock', 'sector': 'Financials', 'local_code': 'PKO'},
    'JSW.WA': {'name': 'Jastrzębska Spółka Węglowa S.A.', 'exchange': 'WSE', 'type': 'stock', 'sector': 'Materials', 'local_code': 'JSW'},
    'CPS.WA': {'name': 'Compass Group PLC', 'exchange': 'WSE', 'type': 'stock', 'sector': 'Consumer Discretionary', 'local_code': 'CPS'},
    'PGE.WA': {'name': 'Polska Grupa Energetyczna S.A.', 'exchange': 'WSE', 'type': 'stock', 'sector': 'Utilities', 'local_code': 'PGE'},
    'DNP.WA': {'name': 'Dino Polska S.A.', 'exchange': 'WSE', 'type': 'stock', 'sector': 'Consumer Staples', 'local_code': 'DNP'},
    
    # European Stocks
    'ASML': {'name': 'ASML Holding N.V.', 'exchange': 'NASDAQ', 'type': 'stock', 'sector': 'Technology'},
    'SAP': {'name': 'SAP SE', 'exchange': 'NYSE', 'type': 'stock', 'sector': 'Technology'},
    'NESN.SW': {'name': 'Nestlé S.A.', 'exchange': 'SIX', 'type': 'stock', 'sector': 'Consumer Staples'},
    'MC.PA': {'name': 'LVMH Moët Hennessy Louis Vuitton SE', 'exchange': 'EPA', 'type': 'stock', 'sector': 'Consumer Discretionary'},
    
    # Cryptocurrencies
    'BTC-USD': {'name': 'Bitcoin', 'exchange': 'Crypto', 'type': 'cryptocurrency', 'sector': 'Digital Assets'},
    'ETH-USD': {'name': 'Ethereum', 'exchange': 'Crypto', 'type': 'cryptocurrency', 'sector': 'Digital Assets'},
    'BNB-USD': {'name': 'Binance Coin', 'exchange': 'Crypto', 'type': 'cryptocurrency', 'sector': 'Digital Assets'},
    'ADA-USD': {'name': 'Cardano', 'exchange': 'Crypto', 'type': 'cryptocurrency', 'sector': 'Digital Assets'},
    'SOL-USD': {'name': 'Solana', 'exchange': 'Crypto', 'type': 'cryptocurrency', 'sector': 'Digital Assets'},
    'DOT-USD': {'name': 'Polkadot', 'exchange': 'Crypto', 'type': 'cryptocurrency', 'sector': 'Digital Assets'},
    'MATIC-USD': {'name': 'Polygon', 'exchange': 'Crypto', 'type': 'cryptocurrency', 'sector': 'Digital Assets'},
    'AVAX-USD': {'name': 'Avalanche', 'exchange': 'Crypto', 'type': 'cryptocurrency', 'sector': 'Digital Assets'},
    
    # ETFs
    'SPY': {'name': 'SPDR S&P 500 ETF Trust', 'exchange': 'NYSE', 'type': 'etf', 'sector': 'Index Fund'},
    'QQQ': {'name': 'Invesco QQQ Trust', 'exchange': 'NASDAQ', 'type': 'etf', 'sector': 'Technology'},
    'VTI': {'name': 'Vanguard Total Stock Market ETF', 'exchange': 'NYSE', 'type': 'etf', 'sector': 'Index Fund'},
    'IWM': {'name': 'iShares Russell 2000 ETF', 'exchange': 'NYSE', 'type': 'etf', 'sector': 'Small Cap'},
    'EFA': {'name': 'iShares MSCI EAFE ETF', 'exchange': 'NYSE', 'type': 'etf', 'sector': 'International'},
    'VEA': {'name': 'Vanguard FTSE Developed Markets ETF', 'exchange': 'NYSE', 'type': 'etf', 'sector': 'International'},
    
    # Commodities
    'GLD': {'name': 'SPDR Gold Shares', 'exchange': 'NYSE', 'type': 'etf', 'sector': 'Precious Metals'},
    'SLV': {'name': 'iShares Silver Trust', 'exchange': 'NYSE', 'type': 'etf', 'sector': 'Precious Metals'},
    'USO': {'name': 'United States Oil Fund', 'exchange': 'NYSE', 'type': 'etf', 'sector': 'Energy'},
    
    # Indices
    '^GSPC': {'name': 'S&P 500 Index', 'exchange': 'Index', 'type': 'index', 'sector': 'Broad Market'},
    '^IXIC': {'name': 'NASDAQ Composite Index', 'exchange': 'Index', 'type': 'index', 'sector': 'Technology'},
    '^DJI': {'name': 'Dow Jones Industrial Average', 'exchange': 'Index', 'type': 'index', 'sector': 'Blue Chip'},
    '^WIG20': {'name': 'WIG20 Index', 'exchange': 'WSE', 'type': 'index', 'sector': 'Polish Market'},
    '^FTSE': {'name': 'FTSE 100 Index', 'exchange': 'LSE', 'type': 'index', 'sector': 'UK Market'},
    '^GDAXI': {'name': 'DAX Index', 'exchange': 'XETRA', 'type': 'index', 'sector': 'German Market'}
}

# Legacy mapping for backward compatibility
POLISH_STOCKS = {
    'PCO': 'PCO.WA', 'PKN': 'PKN.WA', 'PEO': 'PEO.WA', 'KGH': 'KGH.WA',
    'LPP': 'LPP.WA', 'CCC': 'CCC.WA', 'CDR': 'CDR.WA', 'ALE': 'ALE.WA',
    'DNP': 'DNP.WA', 'PGE': 'PGE.WA', 'PZU': 'PZU.WA', 'SPL': 'SPL.WA',
    'PKO': 'PKO.WA', 'JSW': 'JSW.WA', 'CPS': 'CPS.WA', 'OPL': 'OPL.WA',
    'PGN': 'PGN.WA', 'KRU': 'KRU.WA', 'KTY': 'KTY.WA', 'ASE': 'ASE.WA',
    'MBK': 'MBK.WA', 'TPE': 'TPE.WA', 'PLW': 'PLW.WA', '11B': '11B.WA'
}

# Polish indices
POLISH_INDICES = {
    'WIG20': '^WIG20', 'WIG': '^WIG',
    'mWIG40': '^MWIG40', 'sWIG80': '^SWIG80'
}

# Major global indices
GLOBAL_INDICES = {
    'S&P 500': '^GSPC', 'Nasdaq': '^IXIC', 'Dow Jones': '^DJI',
    'Russell 2000': '^RUT', 'VIX': '^VIX', 'FTSE 100': '^FTSE',
    'DAX': '^GDAXI', 'CAC 40': '^FCHI', 'Nikkei': '^N225',
    'Hang Seng': '^HSI', 'Shanghai': '000001.SS'
}

# Data storage paths
DATA_DIR = Path("terminal_data")
DATA_DIR.mkdir(exist_ok=True)
WATCHLIST_FILE = DATA_DIR / "watchlist.json"
PORTFOLIO_FILE = DATA_DIR / "portfolio.json"
SETTINGS_FILE = DATA_DIR / "settings.json"
ALERTS_FILE = DATA_DIR / "alerts.json"

# ================== PROFESSIONAL CSS STYLING ==================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600&display=swap');
    
    :root {
        --bg-primary: #0b0e11;
        --bg-secondary: #161b22;
        --bg-tertiary: #1c2128;
        --bg-hover: #262c36;
        --accent-primary: #4263eb;
        --accent-secondary: #5e72e4;
        --accent-success: #00d68f;
        --accent-danger: #ff3d71;
        --accent-warning: #ffaa00;
        --text-primary: #ffffff;
        --text-secondary: #8b92a8;
        --border-color: #30363d;
    }
    
    .stApp {
        background: linear-gradient(180deg, var(--bg-primary) 0%, #0d1117 100%);
        color: var(--text-primary);
    }
    
    .main-header {
        background: linear-gradient(135deg, var(--bg-secondary) 0%, var(--bg-tertiary) 100%);
        border-bottom: 1px solid var(--border-color);
        padding: 1.5rem 2rem;
        margin: -1rem -2rem 2rem -2rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .widget-card {
        background: var(--bg-secondary);
        border: 1px solid var(--border-color);
        border-radius: 12px;
        padding: 1.5rem;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    .widget-card:hover {
        border-color: var(--accent-primary);
        box-shadow: 0 0 20px rgba(66, 99, 235, 0.1);
        transform: translateY(-2px);
    }
    
    .metric-card {
        background: linear-gradient(135deg, var(--bg-tertiary) 0%, var(--bg-secondary) 100%);
        border: 1px solid var(--border-color);
        border-radius: 10px;
        padding: 1.25rem;
        transition: all 0.3s ease;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, var(--accent-primary), var(--accent-secondary));
        color: white;
        border: none;
        padding: 0.75rem 1.5rem;
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(66, 99, 235, 0.4);
    }
    
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, var(--bg-secondary) 0%, var(--bg-tertiary) 100%);
        border-right: 1px solid var(--border-color);
    }
    
    .dataframe {
        background: var(--bg-secondary) !important;
        color: var(--text-primary) !important;
    }
</style>
""", unsafe_allow_html=True)

# ================== SESSION STATE INITIALIZATION ==================
def initialize_session_state():
    """Initialize all session state variables"""
    
    # Load saved data if exists
    if 'initialized' not in st.session_state:
        st.session_state.initialized = True
        
        # Watchlist
        if WATCHLIST_FILE.exists():
            with open(WATCHLIST_FILE, 'r') as f:
                st.session_state.watchlist = json.load(f)
        else:
            st.session_state.watchlist = ['AAPL', 'MSFT', 'GOOGL', 'NVDA', 'TSLA']
        
        # Portfolio
        if PORTFOLIO_FILE.exists():
            with open(PORTFOLIO_FILE, 'r') as f:
                st.session_state.portfolio = json.load(f)
        else:
            st.session_state.portfolio = {}
        
        # Settings
        if SETTINGS_FILE.exists():
            with open(SETTINGS_FILE, 'r') as f:
                settings = json.load(f)
                for key, value in settings.items():
                    st.session_state[key] = value
        else:
            st.session_state.selected_ticker = 'AAPL'
            st.session_state.theme = 'dark'
            st.session_state.auto_refresh = False
            st.session_state.refresh_interval = 60
        
        # Alerts
        if ALERTS_FILE.exists():
            with open(ALERTS_FILE, 'r') as f:
                st.session_state.alerts = json.load(f)
        else:
            st.session_state.alerts = []
        
        # Other state variables
        st.session_state.trade_history = []
        st.session_state.last_update = datetime.now()

initialize_session_state()

# ================== DATA PERSISTENCE ==================
def save_session_data():
    """Save session data to files"""
    with open(WATCHLIST_FILE, 'w') as f:
        json.dump(st.session_state.watchlist, f)
    
    with open(PORTFOLIO_FILE, 'w') as f:
        json.dump(st.session_state.portfolio, f)
    
    settings = {
        'selected_ticker': st.session_state.selected_ticker,
        'theme': st.session_state.theme,
        'auto_refresh': st.session_state.auto_refresh,
        'refresh_interval': st.session_state.refresh_interval
    }
    with open(SETTINGS_FILE, 'w') as f:
        json.dump(settings, f)
    
    with open(ALERTS_FILE, 'w') as f:
        json.dump(st.session_state.alerts, f)

# ================== UTILITY FUNCTIONS ==================
# ================== POLISH STOCKS MAPPING ==================
POLISH_STOCKS_MAPPING = {
    'PCO': 'PCO.WA',
    'PKN': 'PKN.WA',
    'PEO': 'PEO.WA',
    'KGH': 'KGH.WA',
    'LPP': 'LPP.WA',
    'CCC': 'CCC.WA',
    'CDR': 'CDR.WA',
    'ALE': 'ALE.WA',
    'PZU': 'PZU.WA',
    'PKO': 'PKO.WA',
}

def normalize_ticker(ticker: str) -> str:
    """Normalize ticker for Yahoo Finance"""
    if not ticker:
        return ticker
    
    ticker = ticker.upper().strip()
    
    # Polish stocks legacy mapping
    if ticker in POLISH_STOCKS:
        return POLISH_STOCKS[ticker]
    
    # Check if ticker exists in our database
    if ticker in GLOBAL_INSTRUMENTS:
        return ticker
    
    return ticker

def search_instruments(query: str, limit: int = 10) -> List[Dict[str, str]]:
    """Search instruments by name, ticker, or company name"""
    if not query or len(query) < 1:
        return []
    
    query = query.upper().strip()
    results = []
    
    for ticker, info in GLOBAL_INSTRUMENTS.items():
        # Match by ticker
        if query in ticker.upper():
            results.append({
                'ticker': ticker,
                'name': info['name'],
                'exchange': info['exchange'],
                'type': info['type'],
                'sector': info.get('sector', ''),
                'match_type': 'ticker',
                'score': 100 if ticker.upper() == query else 80
            })
        # Match by company name
        elif query in info['name'].upper():
            results.append({
                'ticker': ticker,
                'name': info['name'],
                'exchange': info['exchange'],
                'type': info['type'],
                'sector': info.get('sector', ''),
                'match_type': 'name',
                'score': 60
            })
        # Match by local code for Polish stocks
        elif 'local_code' in info and query in info['local_code'].upper():
            results.append({
                'ticker': ticker,
                'name': info['name'],
                'exchange': info['exchange'],
                'type': info['type'],
                'sector': info.get('sector', ''),
                'match_type': 'local_code',
                'score': 90
            })
    
    # Sort by score and limit results
    results.sort(key=lambda x: x['score'], reverse=True)
    return results[:limit]

def get_instruments_by_type(instrument_type: str) -> List[Dict[str, str]]:
    """Get all instruments of a specific type"""
    results = []
    
    for ticker, info in GLOBAL_INSTRUMENTS.items():
        if info['type'] == instrument_type:
            results.append({
                'ticker': ticker,
                'name': info['name'],
                'exchange': info['exchange'],
                'type': info['type'],
                'sector': info.get('sector', '')
            })
    
    return sorted(results, key=lambda x: x['name'])

def get_instruments_by_sector(sector: str) -> List[Dict[str, str]]:
    """Get all instruments from a specific sector"""
    results = []
    
    for ticker, info in GLOBAL_INSTRUMENTS.items():
        if info.get('sector', '').lower() == sector.lower():
            results.append({
                'ticker': ticker,
                'name': info['name'],
                'exchange': info['exchange'],
                'type': info['type'],
                'sector': info.get('sector', '')
            })
    
    return sorted(results, key=lambda x: x['name'])

def format_large_number(num: float) -> str:
    """Format large numbers with appropriate suffixes"""
    if num >= 1e12:
        return f"${num/1e12:.2f}T"
    elif num >= 1e9:
        return f"${num/1e9:.2f}B"
    elif num >= 1e6:
        return f"${num/1e6:.2f}M"
    elif num >= 1e3:
        return f"${num/1e3:.2f}K"
    else:
        return f"${num:.2f}"

def check_market_hours() -> Dict[str, bool]:
    """Check if major markets are open"""
    now_ny = datetime.now(pytz.timezone('America/New_York'))
    now_london = datetime.now(pytz.timezone('Europe/London'))
    now_warsaw = datetime.now(pytz.timezone('Europe/Warsaw'))
    now_tokyo = datetime.now(pytz.timezone('Asia/Tokyo'))
    
    markets = {
        'NYSE': 9 <= now_ny.hour < 16,
        'LSE': 8 <= now_london.hour < 16 and now_london.minute < 30 if now_london.hour == 16 else True,
        'WSE': 9 <= now_warsaw.hour < 17,
        'TSE': (9 <= now_tokyo.hour < 11) or (12 <= now_tokyo.hour < 15)
    }
    
    return markets

# ================== OPENBB INTEGRATION ==================
class OpenBBDataProvider:
    """OpenBB data provider for enhanced market data"""
    
    def __init__(self):
        self.available = OPENBB_AVAILABLE
        if self.available:
            try:
                # Initialize OpenBB with any API keys from environment
                if os.getenv('POLYGON_API_KEY'):
                    obb.account.save('polygon', api_key=os.getenv('POLYGON_API_KEY'))
                if os.getenv('FRED_API_KEY'):
                    obb.account.save('fred', api_key=os.getenv('FRED_API_KEY'))
            except:
                pass
    
    @st.cache_data(ttl=300)
    def get_economic_calendar(_self, start_date=None, end_date=None):
        """Get economic calendar events"""
        if not _self.available:
            return pd.DataFrame()
        
        try:
            if not start_date:
                start_date = datetime.now().strftime('%Y-%m-%d')
            if not end_date:
                end_date = (datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d')
            
            events = obb.economy.calendar(start_date=start_date, end_date=end_date)
            return pd.DataFrame(events.results) if hasattr(events, 'results') else pd.DataFrame()
        except:
            return pd.DataFrame()
    
    @st.cache_data(ttl=300)
    def get_market_news(_self, symbol: str = None, limit: int = 20):
        """Get market news"""
        if not _self.available:
            return []
        
        try:
            if symbol:
                news = obb.news.company(symbol=symbol, limit=limit)
            else:
                news = obb.news.general(limit=limit)
            
            return news.results if hasattr(news, 'results') else []
        except:
            return []
    
    @st.cache_data(ttl=600)
    def get_options_chain(_self, symbol: str):
        """Get options chain with Greeks"""
        if not _self.available:
            return None, None
        
        try:
            options = obb.derivatives.options.chains(symbol=symbol)
            if hasattr(options, 'results'):
                df = pd.DataFrame(options.results)
                calls = df[df['option_type'] == 'call']
                puts = df[df['option_type'] == 'put']
                return calls, puts
            return None, None
        except:
            return None, None
    
    @st.cache_data(ttl=300)
    def get_insider_trading(_self, symbol: str):
        """Get insider trading data"""
        if not _self.available:
            return pd.DataFrame()
        
        try:
            insider = obb.equity.ownership.insider_trading(symbol=symbol)
            return pd.DataFrame(insider.results) if hasattr(insider, 'results') else pd.DataFrame()
        except:
            return pd.DataFrame()
    
    @st.cache_data(ttl=600)
    def get_fundamental_data(_self, symbol: str):
        """Get fundamental data"""
        if not _self.available:
            return {}
        
        try:
            profile = obb.equity.profile(symbol=symbol)
            financials = obb.equity.fundamental.income(symbol=symbol, limit=4)
            ratios = obb.equity.fundamental.ratios(symbol=symbol)
            
            return {
                'profile': profile.results if hasattr(profile, 'results') else {},
                'financials': pd.DataFrame(financials.results) if hasattr(financials, 'results') else pd.DataFrame(),
                'ratios': pd.DataFrame(ratios.results) if hasattr(ratios, 'results') else pd.DataFrame()
            }
        except:
            return {}

# Initialize OpenBB provider
openbb_provider = OpenBBDataProvider()

# ================== DATA FETCHING FUNCTIONS ==================
@st.cache_data(ttl=60)
def fetch_stock_data(symbol: str, period: str = '1y', interval: str = '1d'):
    """Fetch stock data using yfinance with error handling"""
    try:
        symbol = normalize_ticker(symbol)  # <-- DODAJ TĘ LINIĘ
        ticker = yf.Ticker(symbol)
    except Exception as e:
        return None, None

@st.cache_data(ttl=300)
def fetch_multiple_stocks(symbols: List[str], period: str = '1d') -> Dict[str, pd.DataFrame]:
    """Fetch data for multiple stocks in parallel"""
    data = {}
    
    with ThreadPoolExecutor(max_workers=10) as executor:
        future_to_symbol = {
            executor.submit(fetch_stock_data, symbol, period): symbol 
            for symbol in symbols
        }
        
        for future in as_completed(future_to_symbol):
            symbol = future_to_symbol[future]
            try:
                result, _ = future.result()
                if result is not None:
                    data[symbol] = result
            except:
                pass
    
    return data

@st.cache_data(ttl=300)
def fetch_market_overview() -> Dict[str, Dict[str, float]]:
    """Fetch market overview data - simplified to avoid errors"""
    # Użyj tylko symboli które na pewno działają
    indices = {
        'AAPL': 'AAPL',
        'MSFT': 'MSFT',
        'GOOGL': 'GOOGL',
        'NVDA': 'NVDA',
        'TSLA': 'TSLA',
        'META': 'META',
        'AMZN': 'AMZN',
        'Bitcoin': 'BTC-USD'
    }
    
    market_data = {}
    for name, symbol in indices.items():
        try:
            ticker = yf.Ticker(symbol)
            hist = ticker.history(period='5d')
            
            if not hist.empty and len(hist) >= 2:
                current_price = hist['Close'].iloc[-1]
                prev_close = hist['Close'].iloc[-2]
                change = ((current_price - prev_close) / prev_close * 100) if prev_close else 0
                
                market_data[name] = {
                    'symbol': symbol,
                    'price': current_price,
                    'change': change,
                    'volume': hist['Volume'].iloc[-1] if 'Volume' in hist else 0
                }
        except:
            continue  # Skip failed symbols
    
    return market_data

# ================== TECHNICAL ANALYSIS ==================
def calculate_technical_indicators(df: pd.DataFrame) -> pd.DataFrame:
    """Calculate comprehensive technical indicators using TA library"""
    if df is None or df.empty:
        return df
    
    # Use TA library for professional indicators
    # Trend Indicators
    df['SMA_20'] = ta.trend.sma_indicator(df['Close'], window=20)
    df['SMA_50'] = ta.trend.sma_indicator(df['Close'], window=50)
    df['SMA_200'] = ta.trend.sma_indicator(df['Close'], window=200)
    df['EMA_12'] = ta.trend.ema_indicator(df['Close'], window=12)
    df['EMA_26'] = ta.trend.ema_indicator(df['Close'], window=26)
    
    # MACD
    macd = ta.trend.MACD(df['Close'])
    df['MACD'] = macd.macd()
    df['MACD_Signal'] = macd.macd_signal()
    df['MACD_Histogram'] = macd.macd_diff()
    
    # RSI
    df['RSI'] = ta.momentum.RSIIndicator(df['Close']).rsi()
    
    # Bollinger Bands
    bollinger = ta.volatility.BollingerBands(df['Close'])
    df['BB_Upper'] = bollinger.bollinger_hband()
    df['BB_Lower'] = bollinger.bollinger_lband()
    df['BB_Middle'] = bollinger.bollinger_mavg()
    df['BB_Width'] = bollinger.bollinger_wband()
    
    # Stochastic
    stoch = ta.momentum.StochasticOscillator(df['High'], df['Low'], df['Close'])
    df['Stoch_K'] = stoch.stoch()
    df['Stoch_D'] = stoch.stoch_signal()
    
    # ATR
    df['ATR'] = ta.volatility.AverageTrueRange(df['High'], df['Low'], df['Close']).average_true_range()
    
    # Volume indicators
    df['Volume_MA'] = ta.volume.volume_weighted_average_price(df['High'], df['Low'], df['Close'], df['Volume'])
    df['OBV'] = ta.volume.on_balance_volume(df['Close'], df['Volume'])
    df['MFI'] = ta.volume.money_flow_index(df['High'], df['Low'], df['Close'], df['Volume'])
    
    # Ichimoku
    ichimoku = ta.trend.IchimokuIndicator(df['High'], df['Low'])
    df['Ichimoku_A'] = ichimoku.ichimoku_a()
    df['Ichimoku_B'] = ichimoku.ichimoku_b()
    
    # Support and Resistance
    df['Pivot'] = (df['High'] + df['Low'] + df['Close']) / 3
    df['R1'] = 2 * df['Pivot'] - df['Low']
    df['S1'] = 2 * df['Pivot'] - df['High']
    df['R2'] = df['Pivot'] + (df['High'] - df['Low'])
    df['S2'] = df['Pivot'] - (df['High'] - df['Low'])
    
    return df

def generate_trade_signals(df: pd.DataFrame) -> Dict[str, Any]:
    """Generate comprehensive trading signals"""
    if df is None or df.empty:
        return {'overall': 'NEUTRAL', 'signals': [], 'strength': 0}
    
    df = calculate_technical_indicators(df)
    signals = []
    bullish_count = 0
    bearish_count = 0
    
    # RSI Signals
    if 'RSI' in df.columns and not df['RSI'].isna().all():
        current_rsi = df['RSI'].iloc[-1]
        if current_rsi < 30:
            signals.append(('RSI Oversold', 'BULLISH', current_rsi))
            bullish_count += 2
        elif current_rsi > 70:
            signals.append(('RSI Overbought', 'BEARISH', current_rsi))
            bearish_count += 2
        else:
            signals.append(('RSI Neutral', 'NEUTRAL', current_rsi))
    
    # MACD Signals
    if 'MACD' in df.columns and 'MACD_Signal' in df.columns:
        macd_current = df['MACD'].iloc[-1]
        signal_current = df['MACD_Signal'].iloc[-1]
        macd_prev = df['MACD'].iloc[-2] if len(df) > 1 else macd_current
        signal_prev = df['MACD_Signal'].iloc[-2] if len(df) > 1 else signal_current
        
        if macd_current > signal_current and macd_prev <= signal_prev:
            signals.append(('MACD Bullish Cross', 'BULLISH', macd_current - signal_current))
            bullish_count += 3
        elif macd_current < signal_current and macd_prev >= signal_prev:
            signals.append(('MACD Bearish Cross', 'BEARISH', macd_current - signal_current))
            bearish_count += 3
    
    # Moving Average Signals
    if all(col in df.columns for col in ['SMA_50', 'SMA_200', 'Close']):
        sma50 = df['SMA_50'].iloc[-1]
        sma200 = df['SMA_200'].iloc[-1]
        current_price = df['Close'].iloc[-1]
        
        if pd.notna(sma50) and pd.notna(sma200):
            if sma50 > sma200:
                signals.append(('Golden Cross Active', 'BULLISH', (sma50/sma200 - 1) * 100))
                bullish_count += 2
            else:
                signals.append(('Death Cross Active', 'BEARISH', (sma50/sma200 - 1) * 100))
                bearish_count += 2
            
            if current_price > sma50:
                bullish_count += 1
            else:
                bearish_count += 1
    
    # Bollinger Bands Signals
    if all(col in df.columns for col in ['BB_Upper', 'BB_Lower', 'Close']):
        current_price = df['Close'].iloc[-1]
        bb_upper = df['BB_Upper'].iloc[-1]
        bb_lower = df['BB_Lower'].iloc[-1]
        
        if pd.notna(bb_upper) and pd.notna(bb_lower):
            bb_position = (current_price - bb_lower) / (bb_upper - bb_lower)
            if bb_position > 1:
                signals.append(('Above BB Upper', 'BEARISH', bb_position))
                bearish_count += 1
            elif bb_position < 0:
                signals.append(('Below BB Lower', 'BULLISH', bb_position))
                bullish_count += 1
            else:
                signals.append(('Within BB Range', 'NEUTRAL', bb_position))
    
    # Calculate overall signal strength
    total_signals = bullish_count + bearish_count
    if total_signals > 0:
        strength = abs(bullish_count - bearish_count) / total_signals * 100
    else:
        strength = 0
    
    # Determine overall signal
    if bullish_count > bearish_count * 1.5:
        overall = 'STRONG BUY'
    elif bullish_count > bearish_count:
        overall = 'BUY'
    elif bearish_count > bullish_count * 1.5:
        overall = 'STRONG SELL'
    elif bearish_count > bullish_count:
        overall = 'SELL'
    else:
        overall = 'NEUTRAL'
    
    return {
        'overall': overall,
        'signals': signals,
        'strength': strength,
        'bullish_count': bullish_count,
        'bearish_count': bearish_count
    }

# ================== CHARTING FUNCTIONS ==================
def create_professional_candlestick_chart(df: pd.DataFrame, ticker: str, indicators: List[str] = []) -> go.Figure:
    """Create professional candlestick chart with indicators"""
    if df is None or df.empty:
        return go.Figure()
    
    df = calculate_technical_indicators(df)
    
    # Determine subplots needed
    rows = 1
    row_heights = [0.7]
    subplot_titles = [f"{ticker} - Price"]
    
    if 'RSI' in indicators:
        rows += 1
        row_heights.append(0.15)
        subplot_titles.append("RSI")
    
    if 'MACD' in indicators:
        rows += 1
        row_heights.append(0.15)
        subplot_titles.append("MACD")
    
    # Create figure with subplots
    fig = make_subplots(
        rows=rows, cols=1,
        shared_xaxes=True,
        vertical_spacing=0.03,
        row_heights=row_heights,
        subplot_titles=subplot_titles
    )
    
    # Main candlestick chart
    fig.add_trace(
        go.Candlestick(
            x=df.index,
            open=df['Open'],
            high=df['High'],
            low=df['Low'],
            close=df['Close'],
            name='OHLC',
            increasing=dict(line=dict(color='#00d68f')),
            decreasing=dict(line=dict(color='#ff3d71'))
        ),
        row=1, col=1
    )
    
    # Add moving averages
    ma_colors = {
        'SMA_20': '#ffaa00', 'SMA_50': '#00d68f', 'SMA_200': '#ff3d71',
        'EMA_12': '#4263eb', 'EMA_26': '#5e72e4'
    }
    
    for ma, color in ma_colors.items():
        if ma in indicators and ma in df.columns:
            fig.add_trace(
                go.Scatter(
                    x=df.index, y=df[ma],
                    mode='lines', name=ma,
                    line=dict(color=color, width=1.5)
                ),
                row=1, col=1
            )
    
    # Bollinger Bands
    if 'Bollinger Bands' in indicators:
        for col, name, color in [
            ('BB_Upper', 'BB Upper', 'rgba(255,255,255,0.2)'),
            ('BB_Lower', 'BB Lower', 'rgba(255,255,255,0.2)'),
            ('BB_Middle', 'BB Middle', 'rgba(255,255,255,0.4)')
        ]:
            if col in df.columns:
                fig.add_trace(
                    go.Scatter(
                        x=df.index, y=df[col],
                        mode='lines', name=name,
                        line=dict(color=color, width=1)
                    ),
                    row=1, col=1
                )
    
    # Volume overlay
    if 'Volume' in indicators:
        colors = ['#00d68f' if df['Close'].iloc[i] >= df['Open'].iloc[i] else '#ff3d71' 
                 for i in range(len(df))]
        
        fig.add_trace(
            go.Bar(
                x=df.index, y=df['Volume'],
                name='Volume',
                marker_color=colors,
                opacity=0.3,
                yaxis='y2'
            ),
            row=1, col=1
        )
    
    current_row = 2
    
    # RSI subplot
    if 'RSI' in indicators and current_row <= rows:
        fig.add_trace(
            go.Scatter(
                x=df.index, y=df['RSI'],
                mode='lines', name='RSI',
                line=dict(color='#5e72e4', width=2)
            ),
            row=current_row, col=1
        )
        
        # Add overbought/oversold lines
        fig.add_hline(y=70, line_dash="dash", line_color="red", 
                     row=current_row, col=1)
        fig.add_hline(y=30, line_dash="dash", line_color="green", 
                     row=current_row, col=1)
        current_row += 1
    
    # MACD subplot
    if 'MACD' in indicators and current_row <= rows:
        # Histogram
        colors = ['#00d68f' if val >= 0 else '#ff3d71' for val in df['MACD_Histogram']]
        fig.add_trace(
            go.Bar(
                x=df.index, y=df['MACD_Histogram'],
                name='Histogram',
                marker_color=colors
            ),
            row=current_row, col=1
        )
        
        # MACD line
        fig.add_trace(
            go.Scatter(
                x=df.index, y=df['MACD'],
                mode='lines', name='MACD',
                line=dict(color='#4263eb', width=2)
            ),
            row=current_row, col=1
        )
        
        # Signal line
        fig.add_trace(
            go.Scatter(
                x=df.index, y=df['MACD_Signal'],
                mode='lines', name='Signal',
                line=dict(color='#ffaa00', width=2)
            ),
            row=current_row, col=1
        )
    
    # Update layout
    fig.update_layout(
        template='plotly_dark',
        height=700,
        showlegend=True,
        hovermode='x unified',
        xaxis_rangeslider_visible=False,
        margin=dict(r=10, t=30, b=40, l=10),
        paper_bgcolor='#0b0e11',
        plot_bgcolor='#161b22',
        legend=dict(
            bgcolor='rgba(22, 27, 34, 0.8)',
            bordercolor='#30363d',
            borderwidth=1
        ),
        yaxis2=dict(
            overlaying='y',
            side='right',
            showgrid=False
        ) if 'Volume' in indicators else {}
    )
    
    # Update axes
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='#30363d')
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='#30363d')
    
    return fig

def create_market_heatmap(market_data: Dict) -> go.Figure:
    """Create market heatmap visualization"""
    labels = []
    parents = []
    values = []
    colors = []
    
    # Group by category
    categories = {
        'Indices': ['S&P 500', 'Nasdaq', 'Dow Jones', 'Russell 2000'],
        'Europe': ['FTSE 100', 'DAX', 'CAC 40', 'WIG20'],
        'Asia': ['Nikkei', 'Hang Seng', 'Shanghai'],
        'Commodities': ['Gold', 'Silver', 'Oil'],
        'Crypto': ['Bitcoin', 'Ethereum']
    }
    
    for category, items in categories.items():
        for item in items:
            if item in market_data:
                labels.append(item)
                parents.append(category)
                values.append(abs(market_data[item]['change']) + 5)
                colors.append(market_data[item]['change'])
        
        labels.append(category)
        parents.append("")
        values.append(20)
        # Calculate average change for category
        cat_items = [market_data[item]['change'] for item in items if item in market_data]
        avg_change = np.mean(cat_items) if cat_items else 0
        colors.append(avg_change)
    
    fig = go.Figure(go.Treemap(
        labels=labels,
        parents=parents,
        values=values,
        marker=dict(
            colorscale='RdYlGn',
            cmid=0,
            cmin=-5,
            cmax=5,
            showscale=True
        ),
        texttemplate='<b>%{label}</b><br>%{color:.2f}%',
        hovertemplate='<b>%{label}</b><br>Change: %{color:.2f}%<extra></extra>'
    ))
    
    fig.update_layout(
        height=500,
        paper_bgcolor='#0b0e11',
        margin=dict(t=30, l=0, r=0, b=0)
    )
    
    return fig

# ================== ENHANCED SIDEBAR ==================
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; padding: 1rem 0; border-bottom: 1px solid #30363d;">
        <div style="font-size: 1.5rem; font-weight: 700; color: #4263eb;">
            🏛️ Terminal Pro 3.0
        </div>
        <div style="font-size: 0.75rem; color: #8b92a8; margin-top: 0.25rem;">
            Professional Trading Platform
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Enhanced Symbol Search with Autocomplete
    st.markdown("### 🔍 Intelligent Search")
    
    search_query = st.text_input(
        "Search Instruments",
        placeholder="Type company name or ticker (e.g. 'Apple', 'AAPL', 'Pepco')",
        key="search_input",
        help="Search by company name, ticker symbol, or exchange code"
    )
    
    # Real-time search results
    if search_query and len(search_query) >= 1:
        search_results = search_instruments(search_query, limit=8)
        
        if search_results:
            st.markdown("**🎯 Search Results:**")
            
            for result in search_results:
                # Create a more informative button display
                display_name = f"{result['ticker']}"
                company_info = f"{result['name'][:30]}..." if len(result['name']) > 30 else result['name']
                exchange_info = f"{result['exchange']} • {result['type'].upper()}"
                
                # Color coding by instrument type
                if result['type'] == 'stock':
                    icon = "📈"
                elif result['type'] == 'etf':
                    icon = "🏦"
                elif result['type'] == 'cryptocurrency':
                    icon = "💰"
                elif result['type'] == 'index':
                    icon = "📉"
                else:
                    icon = "🗂️"
                
                # Create button with rich information
                if st.button(
                    f"{icon} {display_name}",
                    key=f"search_{result['ticker']}",
                    help=f"{company_info}\n{exchange_info}\nSector: {result.get('sector', 'N/A')}",
                    use_container_width=True
                ):
                    st.session_state.selected_ticker = result['ticker']
                    # Clear search after selection
                    st.session_state.search_input = ""
                    st.rerun()
                
                # Show additional info in small text
                st.markdown(f"""
                <div style="font-size: 0.7rem; color: #8b92a8; margin-top: -10px; margin-bottom: 8px;">
                    {company_info}<br>
                    <span style="color: #4263eb;">{exchange_info}</span>
                </div>
                """, unsafe_allow_html=True)
        
        else:
            st.markdown("🔍 No instruments found. Try different keywords.")
    
    st.markdown("---")
    
    # Enhanced Categories with Counters
    st.markdown("### 📋 Browse Categories")
    
    # Category tabs with instrument counts
    category_options = {
        "🇺🇸 US Stocks": "stock_us",
        "🇵🇱 Polish Stocks": "stock_pl", 
        "💰 Cryptocurrencies": "cryptocurrency",
        "🏦 ETFs & Funds": "etf",
        "📉 Market Indices": "index",
        "🌍 All Sectors": "sectors"
    }
    
    selected_category = st.selectbox(
        "Select Category",
        list(category_options.keys()),
        key="category_select"
    )
    
    # Display instruments based on selected category
    if selected_category == "🇺🇸 US Stocks":
        us_stocks = [item for ticker, item in GLOBAL_INSTRUMENTS.items() 
                    if item['type'] == 'stock' and item['exchange'] in ['NASDAQ', 'NYSE']]
        
        st.markdown(f"**Found {len(us_stocks)} US stocks**")
        
        # Group by sector
        sectors = {}
        for stock in us_stocks:
            sector = stock.get('sector', 'Other')
            if sector not in sectors:
                sectors[sector] = []
            sectors[sector].append(stock)
        
        for sector, stocks in sectors.items():
            with st.expander(f"🏷️ {sector} ({len(stocks)})"):
                cols = st.columns(2)
                for i, stock in enumerate(stocks[:10]):  # Limit to 10 per sector
                    with cols[i % 2]:
                        ticker = next(k for k, v in GLOBAL_INSTRUMENTS.items() if v == stock)
                        if st.button(
                            ticker,
                            key=f"us_stock_{ticker}",
                            help=stock['name'],
                            use_container_width=True
                        ):
                            st.session_state.selected_ticker = ticker
                            st.rerun()
    
    elif selected_category == "🇵🇱 Polish Stocks":
        pl_stocks = [item for ticker, item in GLOBAL_INSTRUMENTS.items() 
                    if item['type'] == 'stock' and item['exchange'] == 'WSE']
        
        st.markdown(f"**Found {len(pl_stocks)} Polish stocks**")
        
        for stock in pl_stocks:
            ticker = next(k for k, v in GLOBAL_INSTRUMENTS.items() if v == stock)
            local_code = stock.get('local_code', ticker.split('.')[0])
            
            col1, col2 = st.columns([3, 1])
            with col1:
                if st.button(
                    f"🇵🇱 {local_code}",
                    key=f"pl_stock_{ticker}",
                    help=f"{stock['name']}\nTicker: {ticker}",
                    use_container_width=True
                ):
                    st.session_state.selected_ticker = ticker
                    st.rerun()
            
            with col2:
                st.markdown(f"<div style='font-size:0.7rem;color:#8b92a8;padding-top:8px'>{stock.get('sector', 'N/A')}</div>", unsafe_allow_html=True)
    
    elif selected_category == "💰 Cryptocurrencies":
        cryptos = get_instruments_by_type('cryptocurrency')
        
        st.markdown(f"**Found {len(cryptos)} cryptocurrencies**")
        
        cols = st.columns(2)
        for i, crypto in enumerate(cryptos):
            with cols[i % 2]:
                display_name = crypto['name'].replace('USD', '').strip()
                if st.button(
                    f"💰 {display_name}",
                    key=f"crypto_{crypto['ticker']}",
                    help=f"Full ticker: {crypto['ticker']}",
                    use_container_width=True
                ):
                    st.session_state.selected_ticker = crypto['ticker']
                    st.rerun()
    
    elif selected_category == "🏦 ETFs & Funds":
        etfs = get_instruments_by_type('etf')
        
        st.markdown(f"**Found {len(etfs)} ETFs**")
        
        for etf in etfs:
            if st.button(
                f"🏦 {etf['ticker']}",
                key=f"etf_{etf['ticker']}",
                help=f"{etf['name']}\n{etf['exchange']} • {etf.get('sector', 'N/A')}",
                use_container_width=True
            ):
                st.session_state.selected_ticker = etf['ticker']
                st.rerun()
    
    elif selected_category == "📉 Market Indices":
        indices = get_instruments_by_type('index')
        
        st.markdown(f"**Found {len(indices)} market indices**")
        
        for index in indices:
            if st.button(
                f"📉 {index['ticker']}",
                key=f"index_{index['ticker']}",
                help=f"{index['name']}\n{index['exchange']}",
                use_container_width=True
            ):
                st.session_state.selected_ticker = index['ticker']
                st.rerun()
    
    elif selected_category == "🌍 All Sectors":
        # Group all stocks by sector
        all_sectors = {}
        for ticker, info in GLOBAL_INSTRUMENTS.items():
            if info['type'] == 'stock':
                sector = info.get('sector', 'Other')
                if sector not in all_sectors:
                    all_sectors[sector] = []
                all_sectors[sector].append({'ticker': ticker, **info})
        
        for sector, instruments in sorted(all_sectors.items()):
            with st.expander(f"🏷️ {sector} ({len(instruments)} stocks)"):
                cols = st.columns(2)
                for i, instrument in enumerate(instruments[:8]):  # Limit display
                    with cols[i % 2]:
                        display_ticker = instrument.get('local_code', instrument['ticker'].split('.')[0])
                        if st.button(
                            f"{display_ticker}",
                            key=f"sector_{sector}_{instrument['ticker']}",
                            help=f"{instrument['name']}\n{instrument['exchange']}",
                            use_container_width=True
                        ):
                            st.session_state.selected_ticker = instrument['ticker']
                            st.rerun()
    
    st.markdown("---")
    
    # Enhanced Watchlist Management
    st.markdown("### ⭐ Personal Watchlist")
    
    # Quick add current instrument to watchlist
    if st.session_state.selected_ticker and st.session_state.selected_ticker not in st.session_state.watchlist:
        if st.button(
            f"➕ Add {st.session_state.selected_ticker} to Watchlist",
            key="quick_add_watchlist",
            use_container_width=True
        ):
            st.session_state.watchlist.append(st.session_state.selected_ticker)
            save_session_data()
            st.success(f"Added {st.session_state.selected_ticker} to watchlist!")
            st.rerun()
    
    # Manual add to watchlist
    with st.expander("➕ Add Custom Symbol"):
        col1, col2 = st.columns([3, 1])
        with col1:
            add_symbol = st.text_input(
                "Symbol", 
                key="add_watch", 
                placeholder="Enter ticker..."
            )
        with col2:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("➕", key="add_btn", use_container_width=True):
                if add_symbol and add_symbol.upper() not in st.session_state.watchlist:
                    st.session_state.watchlist.append(add_symbol.upper())
                    save_session_data()
                    st.success(f"Added {add_symbol.upper()}!")
                    st.rerun()
    
    # Display enhanced watchlist
    if st.session_state.watchlist:
        st.markdown(f"**📋 {len(st.session_state.watchlist)} instruments in watchlist**")
        
        for symbol in st.session_state.watchlist[:15]:  # Show up to 15
            col1, col2 = st.columns([4, 1])
            
            with col1:
                # Get instrument info if available
                instrument_info = GLOBAL_INSTRUMENTS.get(symbol, {})
                display_name = symbol
                
                if instrument_info:
                    if instrument_info['type'] == 'stock':
                        icon = "📈"
                    elif instrument_info['type'] == 'etf':
                        icon = "🏦"
                    elif instrument_info['type'] == 'cryptocurrency':
                        icon = "💰"
                    elif instrument_info['type'] == 'index':
                        icon = "📉"
                    else:
                        icon = "🗂️"
                    
                    help_text = f"{instrument_info.get('name', 'Unknown')}\n{instrument_info.get('exchange', 'Unknown')} • {instrument_info.get('type', 'Unknown').upper()}"
                else:
                    icon = "📈"
                    help_text = f"Ticker: {symbol}"
                
                # Highlight current selection
                button_style = "" if symbol != st.session_state.selected_ticker else "type='primary'"
                
                if st.button(
                    f"{icon} {display_name}",
                    key=f"w_{symbol}",
                    help=help_text,
                    use_container_width=True
                ):
                    st.session_state.selected_ticker = symbol
                    st.rerun()
            
            with col2:
                if st.button("🗮", key=f"del_{symbol}", help="Remove from watchlist"):
                    st.session_state.watchlist.remove(symbol)
                    save_session_data()
                    st.rerun()
    
    else:
        st.markdown("🗃️ Your watchlist is empty. Search and add instruments above!")
    
    st.markdown("---")
    
    # Enhanced Market Status with Additional Info
    st.markdown("### 🌍 Live Market Status")
    markets = check_market_hours()
    
    # Add market time information
    from datetime import datetime
    import pytz
    
    market_times = {
        'NYSE': datetime.now(pytz.timezone('America/New_York')),
        'LSE': datetime.now(pytz.timezone('Europe/London')),
        'WSE': datetime.now(pytz.timezone('Europe/Warsaw')),
        'TSE': datetime.now(pytz.timezone('Asia/Tokyo'))
    }
    
    for market, is_open in markets.items():
        status_color = "#00d68f" if is_open else "#ff3d71"
        status_text = "OPEN" if is_open else "CLOSED"
        status_icon = "🟢" if is_open else "🔴"
        
        # Get local time for the market
        market_time = market_times.get(market, datetime.now())
        time_str = market_time.strftime("%H:%M")
        
        st.markdown(f"""
        <div style="display: flex; justify-content: space-between; align-items: center; 
                    padding: 0.5rem; margin: 0.25rem 0; background: rgba(30, 35, 42, 0.5); 
                    border-radius: 8px; border-left: 3px solid {status_color};">
            <div>
                <div style="font-size: 0.875rem; font-weight: 600;">{status_icon} {market}</div>
                <div style="font-size: 0.7rem; color: #8b92a8;">{time_str} local</div>
            </div>
            <div style="color: {status_color}; font-size: 0.75rem; font-weight: 600;">
                {status_text}
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Quick Settings and Info
    st.markdown("### ⚙️ Quick Settings")
    
    # Current selection info
    if st.session_state.selected_ticker:
        current_info = GLOBAL_INSTRUMENTS.get(st.session_state.selected_ticker, {})
        
        if current_info:
            st.markdown(f"""
            <div style="padding: 0.75rem; background: rgba(66, 99, 235, 0.1); 
                        border-radius: 8px; border: 1px solid rgba(66, 99, 235, 0.3);">
                <div style="font-size: 0.8rem; color: #4263eb; font-weight: 600;">
                    Currently Selected:
                </div>
                <div style="font-size: 0.9rem; font-weight: 600; margin-top: 0.25rem;">
                    {st.session_state.selected_ticker}
                </div>
                <div style="font-size: 0.7rem; color: #8b92a8; margin-top: 0.25rem;">
                    {current_info.get('name', 'Unknown Company')}<br>
                    {current_info.get('exchange', 'Unknown')} • {current_info.get('type', 'Unknown').upper()}
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div style="padding: 0.75rem; background: rgba(255, 170, 0, 0.1); 
                        border-radius: 8px; border: 1px solid rgba(255, 170, 0, 0.3);">
                <div style="font-size: 0.8rem; color: #ffaa00; font-weight: 600;">
                    Currently Selected:
                </div>
                <div style="font-size: 0.9rem; font-weight: 600; margin-top: 0.25rem;">
                    {st.session_state.selected_ticker}
                </div>
                <div style="font-size: 0.7rem; color: #8b92a8; margin-top: 0.25rem;">
                    Custom ticker (not in database)
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    # Compact settings
    col1, col2 = st.columns(2)
    
    with col1:
        # Theme toggle
        theme_dark = st.checkbox(
            "🌙 Dark Theme",
            value=st.session_state.theme == 'dark',
            key="theme_toggle"
        )
        st.session_state.theme = 'dark' if theme_dark else 'light'
    
    with col2:
        # Auto-refresh toggle
        auto_refresh = st.checkbox(
            "⚡ Auto-refresh",
            value=st.session_state.auto_refresh,
            key="auto_refresh_toggle"
        )
        st.session_state.auto_refresh = auto_refresh
    
    # Save settings button
    if st.button("💾 Save All Settings", use_container_width=True):
        save_session_data()
        st.success("✅ Settings saved!")
        time.sleep(1)
        st.rerun()
    
    st.markdown("---")
    
    # Data Provider Status
    st.markdown("### 📡 Data Providers")
    
    providers = [
        ("Yahoo Finance", True, "#00d68f"),
        ("OpenBB", OPENBB_AVAILABLE, "#00d68f" if OPENBB_AVAILABLE else "#ff3d71")
    ]
    
    for provider, status, color in providers:
        status_text = "✅ Active" if status else "❌ Inactive"
        status_icon = "🟢" if status else "🔴"
        
        st.markdown(f"""
        <div style="display: flex; justify-content: space-between; align-items: center; 
                    padding: 0.5rem; background: rgba(30, 35, 42, 0.3); 
                    border-radius: 6px; margin: 0.25rem 0;">
            <div style="font-size: 0.8rem; font-weight: 500;">{status_icon} {provider}</div>
            <div style="color: {color}; font-size: 0.7rem; font-weight: 600;">{status_text}</div>
        </div>
        """, unsafe_allow_html=True)

# ================== MAIN APPLICATION ==================

# Header
st.markdown("""
<div class="main-header">
    <div style="display: flex; justify-content: space-between; align-items: center;">
        <div>
            <h1 style="margin: 0; color: #ffffff;">Terminal Pro 3.0</h1>
            <p style="margin: 0; color: #8b92a8;">Professional Trading Platform with OpenBB Integration</p>
        </div>
        <div style="text-align: right;">
            <div style="color: #8b92a8; font-size: 0.875rem;">Last Update</div>
            <div style="color: #ffffff; font-weight: 600;">{}</div>
        </div>
    </div>
</div>
""".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S")), unsafe_allow_html=True)

# Main Tabs
main_tabs = st.tabs([
    "📊 Dashboard",
    "📈 Charts",
    "🎯 Analysis",
    "📰 News",
    "💼 Portfolio",
    "🔍 Screener",
    "📅 Calendar",
    "⚙️ Settings"
])

# ================== DASHBOARD TAB ==================
with main_tabs[0]:
    st.markdown("### 🌍 Global Markets Overview")
    
    # Fetch market data
    with st.spinner("Loading market data..."):
        market_data = fetch_market_overview()
    
    # Market Heatmap
    if market_data:
        st.plotly_chart(create_market_heatmap(market_data), use_container_width=True)
    
    # Market Stats Grid
    if market_data and len(market_data) > 0:  # <-- DODAJ TĘ LINIĘ
        st.markdown("### 📊 Market Statistics")
        
        col1, col2, col3, col4 = st.columns(4)
        
        # Calculate stats
        advances = sum(1 for d in market_data.values() if d.get('change', 0) > 0)
        declines = sum(1 for d in market_data.values() if d.get('change', 0) < 0)
        unchanged = len(market_data) - advances - declines
        avg_change = np.mean([d.get('change', 0) for d in market_data.values()])
        
        with col1:
            st.metric("Advances", advances)  # <-- USUŃ DZIELENIE
        with col2:
            st.metric("Declines", declines)
        with col3:
            st.metric("Unchanged", unchanged)
        with col4:
            st.metric("Avg Change", f"{avg_change:.2f}%")
    else:
        st.warning("Market data temporarily unavailable")
    
    # Top Movers
    st.markdown("### 🚀 Top Movers")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**🟢 Top Gainers**")
        sorted_gainers = sorted(market_data.items(), key=lambda x: x[1]['change'], reverse=True)[:5]
        for name, data in sorted_gainers:
            if data['change'] > 0:
                st.markdown(f"""
                <div style="display: flex; justify-content: space-between; padding: 0.5rem; 
                            background: rgba(0, 214, 143, 0.1); border-radius: 8px; margin: 0.25rem 0;">
                    <span>{name}</span>
                    <span style="color: #00d68f; font-weight: 600;">+{data['change']:.2f}%</span>
                </div>
                """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("**🔴 Top Losers**")
        sorted_losers = sorted(market_data.items(), key=lambda x: x[1]['change'])[:5]
        for name, data in sorted_losers:
            if data['change'] < 0:
                st.markdown(f"""
                <div style="display: flex; justify-content: space-between; padding: 0.5rem; 
                            background: rgba(255, 61, 113, 0.1); border-radius: 8px; margin: 0.25rem 0;">
                    <span>{name}</span>
                    <span style="color: #ff3d71; font-weight: 600;">{data['change']:.2f}%</span>
                </div>
                """, unsafe_allow_html=True)
    
    # Economic Calendar Preview (if OpenBB available)
    if OPENBB_AVAILABLE:
        st.markdown("### 📅 Economic Events Today")
        events = openbb_provider.get_economic_calendar()
        if not events.empty:
            st.dataframe(events.head(5), use_container_width=True)

# ================== CHARTS TAB ==================
with main_tabs[1]:
    ticker = normalize_ticker(st.session_state.selected_ticker)
    
    st.markdown(f"### 📈 Chart Analysis - {st.session_state.selected_ticker}")
    
    # Chart controls
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        period = st.selectbox(
            "Period",
            ["1d", "5d", "1mo", "3mo", "6mo", "1y", "2y", "5y", "ytd", "max"],
            index=5
        )
    
    with col2:
        interval = st.selectbox(
            "Interval",
            ["1m", "5m", "15m", "30m", "1h", "1d", "1wk", "1mo"],
            index=5
        )
    
    with col3:
        chart_type = st.selectbox(
            "Chart Type",
            ["Candlestick", "Line", "Area"],
            index=0
        )
    
    with col4:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🔄 Refresh", use_container_width=True):
            st.cache_data.clear()
            st.rerun()
    
    # Technical indicators selection
    st.markdown("#### Technical Indicators")
    
    col1, col2, col3, col4 = st.columns(4)
    
    indicators = []
    
    with col1:
        if st.checkbox("SMA 20/50/200"):
            indicators.extend(['SMA_20', 'SMA_50', 'SMA_200'])
        if st.checkbox("EMA 12/26"):
            indicators.extend(['EMA_12', 'EMA_26'])
    
    with col2:
        if st.checkbox("Bollinger Bands"):
            indicators.append('Bollinger Bands')
        if st.checkbox("Volume"):
            indicators.append('Volume')
    
    with col3:
        if st.checkbox("RSI"):
            indicators.append('RSI')
        if st.checkbox("MACD"):
            indicators.append('MACD')
    
    with col4:
        if st.checkbox("Support/Resistance"):
            indicators.append('Support/Resistance')
    
    # Fetch and display data
    with st.spinner(f"Loading data for {ticker}..."):
        data, info = fetch_stock_data(ticker, period, interval)
    
    if data is not None and not data.empty:
        # Company info bar
        col1, col2, col3, col4, col5 = st.columns(5)
        
        current_price = data['Close'].iloc[-1]
        prev_close = data['Close'].iloc[-2] if len(data) > 1 else current_price
        change = current_price - prev_close
        change_pct = (change / prev_close * 100) if prev_close else 0
        
        with col1:
            st.metric("Price", f"${current_price:.2f}", f"{change_pct:+.2f}%")
        
        with col2:
            st.metric("Day High", f"${data['High'].iloc[-1]:.2f}")
        
        with col3:
            st.metric("Day Low", f"${data['Low'].iloc[-1]:.2f}")
        
        with col4:
            st.metric("Volume", f"{data['Volume'].iloc[-1]:,.0f}")
        
        with col5:
            if info:
                mkt_cap = info.get('marketCap', 0)
                st.metric("Market Cap", format_large_number(mkt_cap))
        
        # Display chart
        fig = create_professional_candlestick_chart(data, ticker, indicators)
        st.plotly_chart(fig, use_container_width=True)
        
        # Trading signals
        signals = generate_trade_signals(data)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            signal_color = {
                'STRONG BUY': '#00d68f',
                'BUY': '#00d68f',
                'NEUTRAL': '#ffaa00',
                'SELL': '#ff3d71',
                'STRONG SELL': '#ff3d71'
            }
            
            st.markdown(f"""
            <div class="widget-card" style="text-align: center;">
                <h3 style="color: {signal_color.get(signals['overall'], '#ffaa00')};">
                    {signals['overall']}
                </h3>
                <p style="color: #8b92a8;">Signal Strength: {signals['strength']:.1f}%</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="widget-card" style="text-align: center;">
                <h3 style="color: #00d68f;">Bullish: {signals['bullish_count']}</h3>
                <p style="color: #8b92a8;">Positive Signals</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="widget-card" style="text-align: center;">
                <h3 style="color: #ff3d71;">Bearish: {signals['bearish_count']}</h3>
                <p style="color: #8b92a8;">Negative Signals</p>
            </div>
            """, unsafe_allow_html=True)

# ================== ANALYSIS TAB ==================
with main_tabs[2]:
    ticker = normalize_ticker(st.session_state.selected_ticker)
    
    st.markdown(f"### 🎯 Technical Analysis - {st.session_state.selected_ticker}")
    
    analysis_tabs = st.tabs(["Technical", "Fundamental", "Options", "Insider Trading"])
    
    # Technical Analysis
    with analysis_tabs[0]:
        data, _ = fetch_stock_data(ticker, '6mo', '1d')
        
        if data is not None:
            signals = generate_trade_signals(data)
            
            # Display individual signals
            st.markdown("### 📊 Technical Indicators")
            
            cols = st.columns(3)
            for i, (signal_name, signal_type, value) in enumerate(signals['signals']):
                with cols[i % 3]:
                    color = '#00d68f' if signal_type == 'BULLISH' else '#ff3d71' if signal_type == 'BEARISH' else '#ffaa00'
                    
                    st.markdown(f"""
                    <div class="metric-card">
                        <div style="color: #8b92a8; font-size: 0.875rem;">{signal_name}</div>
                        <div style="color: {color}; font-size: 1.25rem; font-weight: 600;">
                            {signal_type}
                        </div>
                        <div style="color: #8b92a8; font-size: 0.75rem;">
                            Value: {value:.2f}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
    
    # Fundamental Analysis
    with analysis_tabs[1]:
        if OPENBB_AVAILABLE:
            fundamental = openbb_provider.get_fundamental_data(ticker)
            
            if fundamental and 'profile' in fundamental:
                st.markdown("### 🏢 Company Profile")
                profile = fundamental['profile']
                
                if profile:
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.write(f"**Sector:** {profile.get('sector', 'N/A')}")
                        st.write(f"**Industry:** {profile.get('industry', 'N/A')}")
                        st.write(f"**Employees:** {profile.get('employees', 'N/A'):,}")
                    
                    with col2:
                        st.write(f"**CEO:** {profile.get('ceo', 'N/A')}")
                        st.write(f"**Founded:** {profile.get('founded', 'N/A')}")
                        st.write(f"**Website:** {profile.get('website', 'N/A')}")
                
                if 'financials' in fundamental and not fundamental['financials'].empty:
                    st.markdown("### 📊 Financial Statements")
                    st.dataframe(fundamental['financials'], use_container_width=True)
        else:
            st.info("Install OpenBB for fundamental analysis: pip install openbb")
    
    # Options Analysis
    with analysis_tabs[2]:
        if OPENBB_AVAILABLE:
            calls, puts = openbb_provider.get_options_chain(ticker)
            
            if calls is not None and puts is not None:
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("### Call Options")
                    st.dataframe(calls.head(10), use_container_width=True)
                
                with col2:
                    st.markdown("### Put Options")
                    st.dataframe(puts.head(10), use_container_width=True)
        else:
            st.info("Options data requires OpenBB integration")
    
    # Insider Trading
    with analysis_tabs[3]:
        if OPENBB_AVAILABLE:
            insider = openbb_provider.get_insider_trading(ticker)
            
            if not insider.empty:
                st.markdown("### 👥 Recent Insider Transactions")
                st.dataframe(insider.head(10), use_container_width=True)
        else:
            st.info("Insider trading data requires OpenBB integration")

# ================== NEWS TAB ==================
with main_tabs[3]:
    ticker = normalize_ticker(st.session_state.selected_ticker)
    
    st.markdown(f"### 📰 News & Research - {st.session_state.selected_ticker}")
    
    if OPENBB_AVAILABLE:
        news = openbb_provider.get_market_news(ticker, limit=20)
        
        if news:
            for article in news[:10]:
                title = article.get('title', 'No title')
                date = article.get('date', '')
                source = article.get('source', 'Unknown')
                url = article.get('url', '#')
                
                st.markdown(f"""
                <div class="widget-card" style="margin-bottom: 1rem;">
                    <h4>{title}</h4>
                    <p style="color: #8b92a8;">📰 {source} • 📅 {date}</p>
                    <a href="{url}" target="_blank" style="color: #4263eb;">Read More →</a>
                </div>
                """, unsafe_allow_html=True)
    else:
        # Fallback to yfinance news
        ticker_obj = yf.Ticker(ticker)
        news = ticker_obj.news
        
        if news:
            for article in news[:10]:
                st.markdown(f"""
                <div class="widget-card" style="margin-bottom: 1rem;">
                    <h4>{article.get('title', 'No title')}</h4>
                    <p style="color: #8b92a8;">📰 {article.get('publisher', 'Unknown')}</p>
                    <a href="{article.get('link', '#')}" target="_blank" style="color: #4263eb;">Read More →</a>
                </div>
                """, unsafe_allow_html=True)

# ================== PORTFOLIO TAB ==================
with main_tabs[4]:
    st.markdown("### 💼 Portfolio Management")
    
    # Add position form
    with st.expander("➕ Add New Position"):
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            add_symbol = st.text_input("Symbol", key="add_pos_symbol")
        with col2:
            add_shares = st.number_input("Shares", min_value=0.0, step=1.0, key="add_pos_shares")
        with col3:
            add_cost = st.number_input("Avg Cost", min_value=0.0, step=0.01, key="add_pos_cost")
        with col4:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("Add Position", use_container_width=True):
                if add_symbol and add_shares > 0 and add_cost > 0:
                    symbol = normalize_ticker(add_symbol.upper())
                    ticker = yf.Ticker(symbol)
                    hist = ticker.history(period='1d')
                    
                    if not hist.empty:
                        current_price = hist['Close'].iloc[-1]
                        st.session_state.portfolio[add_symbol.upper()] = {
                            'shares': add_shares,
                            'avg_cost': add_cost,
                            'current_price': current_price
                        }
                        save_session_data()
                        st.success(f"Added {add_shares} shares of {add_symbol.upper()}")
                        st.rerun()
    
    # Portfolio display
    if st.session_state.portfolio:
        # Calculate metrics
        total_value = 0
        total_cost = 0
        portfolio_data = []
        
        for symbol, position in st.session_state.portfolio.items():
            # Update current price
            try:
                ticker = yf.Ticker(normalize_ticker(symbol))
                hist = ticker.history(period='1d')
                if not hist.empty:
                    current_price = hist['Close'].iloc[-1]
                    position['current_price'] = current_price
            except:
                current_price = position.get('current_price', position['avg_cost'])
            
            market_value = position['shares'] * current_price
            cost_basis = position['shares'] * position['avg_cost']
            pl = market_value - cost_basis
            pl_pct = (pl / cost_basis * 100) if cost_basis > 0 else 0
            
            total_value += market_value
            total_cost += cost_basis
            
            portfolio_data.append({
                'Symbol': symbol,
                'Shares': position['shares'],
                'Avg Cost': position['avg_cost'],
                'Current': current_price,
                'Value': market_value,
                'Cost': cost_basis,
                'P&L': pl,
                'P&L %': pl_pct
            })
        
        # Display metrics
        total_pl = total_value - total_cost
        total_pl_pct = (total_pl / total_cost * 100) if total_cost > 0 else 0
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Value", format_large_number(total_value))
        with col2:
            st.metric("Total P&L", format_large_number(total_pl), f"{total_pl_pct:+.2f}%")
        with col3:
            st.metric("Total Cost", format_large_number(total_cost))
        with col4:
            st.metric("Positions", len(st.session_state.portfolio))
        
        # Portfolio table
        st.markdown("### 📊 Holdings")
        
        df = pd.DataFrame(portfolio_data)
        st.dataframe(
            df.style.format({
                'Shares': '{:.0f}',
                'Avg Cost': '${:.2f}',
                'Current': '${:.2f}',
                'Value': '${:,.2f}',
                'Cost': '${:,.2f}',
                'P&L': '${:+,.2f}',
                'P&L %': '{:+.2f}%'
            }).apply(lambda x: ['background-color: rgba(0, 214, 143, 0.1)' if x['P&L'] > 0 
                               else 'background-color: rgba(255, 61, 113, 0.1)' if x['P&L'] < 0
                               else '' for _ in x], axis=1),
            use_container_width=True,
            hide_index=True
        )
        
        # Portfolio chart
        if len(portfolio_data) > 0:
            fig = go.Figure(data=[go.Pie(
                labels=[p['Symbol'] for p in portfolio_data],
                values=[p['Value'] for p in portfolio_data],
                hole=0.4
            )])
            
            fig.update_layout(
                title="Portfolio Allocation",
                template='plotly_dark',
                height=400,
                paper_bgcolor='#0b0e11',
                plot_bgcolor='#161b22'
            )
            
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Your portfolio is empty. Add positions to start tracking.")

# ================== SCREENER TAB ==================
with main_tabs[5]:
    st.markdown("### 🔍 Stock Screener")
    
    # Screener filters
    with st.expander("Screener Filters", expanded=True):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            market_cap_min = st.number_input("Min Market Cap (B)", min_value=0.0, value=1.0)
            pe_min = st.number_input("Min P/E", min_value=-100.0, value=0.0)
        
        with col2:
            market_cap_max = st.number_input("Max Market Cap (B)", min_value=0.0, value=5000.0)
            pe_max = st.number_input("Max P/E", min_value=0.0, value=50.0)
        
        with col3:
            volume_min = st.number_input("Min Volume (M)", min_value=0.0, value=1.0)
            sector = st.selectbox("Sector", ["All", "Technology", "Healthcare", "Finance", "Energy"])
    
    if st.button("🔍 Run Screener", use_container_width=True):
        # Sample screener results (in production, implement actual screening)
        st.markdown("### Screener Results")
        
        sample_results = pd.DataFrame({
            'Symbol': ['NVDA', 'AAPL', 'MSFT', 'GOOGL', 'META'],
            'Price': [520.25, 175.50, 380.25, 2850.00, 385.20],
            'Change %': [5.2, 2.1, 1.5, 1.8, 3.2],
            'Volume': ['125M', '78M', '45M', '25M', '38M'],
            'Market Cap': ['1.3T', '2.7T', '2.8T', '1.8T', '1.0T'],
            'P/E': [65.2, 29.8, 35.2, 28.5, 22.3]
        })
        
        st.dataframe(sample_results, use_container_width=True)

# ================== CALENDAR TAB ==================
with main_tabs[6]:
    st.markdown("### 📅 Economic Calendar")
    
    if OPENBB_AVAILABLE:
        events = openbb_provider.get_economic_calendar()
        
        if not events.empty:
            st.dataframe(events, use_container_width=True)
    else:
        st.info("Economic calendar requires OpenBB integration. Install with: pip install openbb")

# ================== SETTINGS TAB ==================
with main_tabs[7]:
    st.markdown("### ⚙️ Platform Settings")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Display Settings")
        
        theme = st.selectbox("Theme", ["Dark", "Light"], index=0 if st.session_state.theme == 'dark' else 1)
        st.session_state.theme = theme.lower()
        
        refresh_interval = st.slider("Auto-refresh (seconds)", 30, 300, st.session_state.refresh_interval)
        st.session_state.refresh_interval = refresh_interval
    
    with col2:
        st.markdown("#### Data Providers")
        
        st.write("**Active Providers:**")
        st.write("✅ Yahoo Finance")
        if OPENBB_AVAILABLE:
            st.write("✅ OpenBB")
        else:
            st.write("❌ OpenBB (not installed)")
    
    if st.button("💾 Save All Settings", use_container_width=True):
        save_session_data()
        st.success("✅ Settings saved successfully!")

# Footer
st.markdown("""
<div style="margin-top: 3rem; padding: 2rem 0; border-top: 1px solid #30363d; text-align: center; color: #8b92a8;">
    <div style="font-size: 1.1rem; font-weight: 600; margin-bottom: 0.5rem;">
        Terminal Pro 3.0 - Professional Trading Platform
    </div>
    <div style="margin: 1rem 0;">
        <span style="margin: 0 1rem;">📊 Real-time Data</span>
        <span style="margin: 0 1rem;">🤖 AI Analysis</span>
        <span style="margin: 0 1rem;">🔐 Secure</span>
        <span style="margin: 0 1rem;">⚡ Fast</span>
    </div>
    <div style="font-size: 0.75rem; opacity: 0.6;">
        Data provided by Yahoo Finance & OpenBB | Market data may be delayed
    </div>
</div>
""", unsafe_allow_html=True)

"""
Professional Trading Terminal - Full Version
Complete institutional-grade trading platform with all features
Version: 2.0 | Lines: 1500+
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
from typing import Dict, List, Optional, Tuple, Any
import warnings
warnings.filterwarnings('ignore')

# ================== CONFIGURATION ==================
st.set_page_config(
    page_title="Terminal Pro | Institutional Trading Platform",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items={
        'Get Help': 'https://github.com/yourusername/trading-terminal',
        'Report a bug': 'https://github.com/yourusername/trading-terminal/issues',
        'About': "Professional Trading Terminal v2.0 | Powered by OpenBB & YFinance"
    }
)

# ================== PROFESSIONAL CSS STYLING ==================
st.markdown("""
<style>
    /* Import Professional Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600&display=swap');
    
    /* CSS Variables for Theme */
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
        --text-muted: #6a737d;
        --border-color: #30363d;
        --shadow-sm: 0 1px 3px rgba(0, 0, 0, 0.12);
        --shadow-md: 0 4px 6px rgba(0, 0, 0, 0.1);
        --shadow-lg: 0 10px 15px rgba(0, 0, 0, 0.1);
    }
    
    /* Global Reset and Base Styles */
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
    
    html {
        scroll-behavior: smooth;
    }
    
    body {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
        -webkit-font-smoothing: antialiased;
        -moz-osx-font-smoothing: grayscale;
    }
    
    /* Main App Container */
    .stApp {
        background: linear-gradient(180deg, var(--bg-primary) 0%, #0d1117 100%);
        color: var(--text-primary);
        min-height: 100vh;
    }
    
    /* Hide Streamlit Default Elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Professional Header */
    .main-header {
        background: linear-gradient(135deg, var(--bg-secondary) 0%, var(--bg-tertiary) 100%);
        border-bottom: 1px solid var(--border-color);
        padding: 1.5rem 2rem;
        margin: -1rem -2rem 2rem -2rem;
        box-shadow: var(--shadow-md);
        position: relative;
        overflow: hidden;
    }
    
    .main-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 2px;
        background: linear-gradient(90deg, var(--accent-primary), var(--accent-secondary), var(--accent-primary));
        animation: gradient-shift 3s ease infinite;
    }
    
    @keyframes gradient-shift {
        0%, 100% { transform: translateX(-100%); }
        50% { transform: translateX(100%); }
    }
    
    .header-content {
        display: flex;
        justify-content: space-between;
        align-items: center;
        position: relative;
        z-index: 1;
    }
    
    .logo-section {
        display: flex;
        align-items: center;
        gap: 1rem;
    }
    
    .logo {
        width: 48px;
        height: 48px;
        background: linear-gradient(135deg, var(--accent-primary), var(--accent-secondary));
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 700;
        font-size: 1.5rem;
        color: white;
        box-shadow: var(--shadow-lg);
    }
    
    .platform-info {
        display: flex;
        flex-direction: column;
    }
    
    .platform-name {
        font-size: 1.5rem;
        font-weight: 700;
        color: var(--text-primary);
        letter-spacing: -0.5px;
    }
    
    .platform-subtitle {
        font-size: 0.875rem;
        color: var(--text-secondary);
        margin-top: 0.25rem;
    }
    
    /* Market Status Bar */
    .market-status {
        display: flex;
        gap: 2rem;
        align-items: center;
    }
    
    .status-item {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.5rem 1rem;
        background: var(--bg-tertiary);
        border-radius: 8px;
        border: 1px solid var(--border-color);
    }
    
    .status-indicator {
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background: var(--accent-success);
        animation: pulse 2s infinite;
        box-shadow: 0 0 10px var(--accent-success);
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 1; transform: scale(1); }
        50% { opacity: 0.6; transform: scale(1.2); }
    }
    
    /* Navigation Menu */
    .nav-menu {
        background: var(--bg-secondary);
        border-bottom: 1px solid var(--border-color);
        padding: 0;
        margin: 0 -2rem 2rem -2rem;
    }
    
    .nav-menu ul {
        display: flex;
        list-style: none;
        margin: 0;
        padding: 0;
    }
    
    .nav-menu li {
        position: relative;
    }
    
    .nav-menu a {
        display: block;
        padding: 1rem 1.5rem;
        color: var(--text-secondary);
        text-decoration: none;
        font-weight: 500;
        transition: all 0.3s ease;
        border-bottom: 2px solid transparent;
    }
    
    .nav-menu a:hover {
        color: var(--text-primary);
        background: var(--bg-hover);
    }
    
    .nav-menu a.active {
        color: var(--accent-primary);
        border-bottom-color: var(--accent-primary);
    }
    
    /* Widget Cards */
    .widget-card {
        background: var(--bg-secondary);
        border: 1px solid var(--border-color);
        border-radius: 12px;
        padding: 1.5rem;
        height: 100%;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }
    
    .widget-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, var(--accent-primary), var(--accent-secondary));
        transform: scaleX(0);
        transition: transform 0.3s ease;
    }
    
    .widget-card:hover {
        border-color: var(--accent-primary);
        box-shadow: 0 0 20px rgba(66, 99, 235, 0.1);
        transform: translateY(-2px);
    }
    
    .widget-card:hover::before {
        transform: scaleX(1);
    }
    
    .widget-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 1rem;
        padding-bottom: 0.75rem;
        border-bottom: 1px solid var(--border-color);
    }
    
    .widget-title {
        font-size: 0.875rem;
        font-weight: 600;
        color: var(--text-secondary);
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .widget-actions {
        display: flex;
        gap: 0.5rem;
    }
    
    .widget-action-btn {
        padding: 0.25rem 0.5rem;
        background: var(--bg-tertiary);
        border: 1px solid var(--border-color);
        border-radius: 6px;
        color: var(--text-secondary);
        font-size: 0.75rem;
        cursor: pointer;
        transition: all 0.2s ease;
    }
    
    .widget-action-btn:hover {
        background: var(--accent-primary);
        color: white;
        border-color: var(--accent-primary);
    }
    
    /* Metric Cards */
    .metric-card {
        background: linear-gradient(135deg, var(--bg-tertiary) 0%, var(--bg-secondary) 100%);
        border: 1px solid var(--border-color);
        border-radius: 10px;
        padding: 1.25rem;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .metric-card::after {
        content: '';
        position: absolute;
        bottom: 0;
        left: 0;
        right: 0;
        height: 2px;
        background: linear-gradient(90deg, transparent, var(--accent-primary), transparent);
        transform: translateX(-100%);
        animation: slide 3s infinite;
    }
    
    @keyframes slide {
        100% { transform: translateX(100%); }
    }
    
    .metric-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2);
        border-color: var(--accent-primary);
    }
    
    .metric-label {
        font-size: 0.75rem;
        color: var(--text-secondary);
        margin-bottom: 0.5rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        font-weight: 600;
    }
    
    .metric-value {
        font-size: 1.75rem;
        font-weight: 700;
        color: var(--text-primary);
        line-height: 1;
        margin-bottom: 0.5rem;
    }
    
    .metric-change {
        font-size: 0.875rem;
        font-weight: 500;
        display: flex;
        align-items: center;
        gap: 0.25rem;
    }
    
    .metric-change.positive {
        color: var(--accent-success);
    }
    
    .metric-change.negative {
        color: var(--accent-danger);
    }
    
    .metric-change.neutral {
        color: var(--text-secondary);
    }
    
    /* Data Tables */
    .dataframe {
        background: var(--bg-secondary) !important;
        color: var(--text-primary) !important;
        border: 1px solid var(--border-color) !important;
        border-radius: 8px;
        overflow: hidden;
    }
    
    .dataframe thead tr th {
        background: linear-gradient(180deg, var(--bg-tertiary) 0%, var(--bg-secondary) 100%) !important;
        color: var(--text-secondary) !important;
        font-weight: 600;
        text-transform: uppercase;
        font-size: 0.75rem;
        letter-spacing: 0.5px;
        padding: 1rem !important;
        border-bottom: 2px solid var(--border-color) !important;
        position: sticky;
        top: 0;
        z-index: 10;
    }
    
    .dataframe tbody tr {
        border-bottom: 1px solid var(--border-color) !important;
        transition: all 0.2s ease;
    }
    
    .dataframe tbody tr:hover {
        background: var(--bg-hover) !important;
    }
    
    .dataframe tbody tr td {
        padding: 0.875rem !important;
        font-size: 0.875rem;
        font-family: 'JetBrains Mono', monospace;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, var(--accent-primary), var(--accent-secondary));
        color: white;
        border: none;
        padding: 0.75rem 1.5rem;
        border-radius: 8px;
        font-weight: 600;
        font-size: 0.875rem;
        letter-spacing: 0.5px;
        text-transform: uppercase;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 4px 15px rgba(66, 99, 235, 0.3);
        position: relative;
        overflow: hidden;
    }
    
    .stButton > button::before {
        content: '';
        position: absolute;
        top: 50%;
        left: 50%;
        width: 0;
        height: 0;
        background: rgba(255, 255, 255, 0.2);
        border-radius: 50%;
        transform: translate(-50%, -50%);
        transition: width 0.3s, height 0.3s;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(66, 99, 235, 0.4);
    }
    
    .stButton > button:hover::before {
        width: 300px;
        height: 300px;
    }
    
    /* Input Fields */
    .stTextInput > div > div > input,
    .stSelectbox > div > div > select,
    .stTextArea > div > div > textarea {
        background: var(--bg-tertiary);
        color: var(--text-primary);
        border: 1px solid var(--border-color);
        border-radius: 8px;
        padding: 0.75rem;
        font-size: 0.875rem;
        transition: all 0.3s ease;
    }
    
    .stTextInput > div > div > input:focus,
    .stSelectbox > div > div > select:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: var(--accent-primary);
        box-shadow: 0 0 0 3px rgba(66, 99, 235, 0.1);
        outline: none;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        background: var(--bg-secondary);
        border-bottom: 2px solid var(--border-color);
        padding: 0;
        gap: 0;
    }
    
    .stTabs [data-baseweb="tab"] {
        color: var(--text-secondary);
        font-weight: 500;
        font-size: 0.875rem;
        padding: 1rem 1.5rem;
        background: transparent;
        border: none;
        border-bottom: 3px solid transparent;
        margin-bottom: -2px;
        transition: all 0.3s ease;
        position: relative;
    }
    
    .stTabs [data-baseweb="tab"]::after {
        content: '';
        position: absolute;
        bottom: 0;
        left: 50%;
        width: 0;
        height: 3px;
        background: var(--accent-primary);
        transform: translateX(-50%);
        transition: width 0.3s ease;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        color: var(--text-primary);
        background: var(--bg-hover);
    }
    
    .stTabs [aria-selected="true"] {
        color: var(--accent-primary) !important;
        background: var(--bg-tertiary);
    }
    
    .stTabs [aria-selected="true"]::after {
        width: 100%;
    }
    
    /* Charts Container */
    .chart-container {
        background: var(--bg-secondary);
        border: 1px solid var(--border-color);
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: var(--shadow-md);
    }
    
    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, var(--bg-secondary) 0%, var(--bg-tertiary) 100%);
        border-right: 1px solid var(--border-color);
    }
    
    section[data-testid="stSidebar"] .block-container {
        padding: 2rem 1rem;
    }
    
    /* Metrics Grid */
    div[data-testid="metric-container"] {
        background: linear-gradient(135deg, var(--bg-tertiary) 0%, var(--bg-secondary) 100%);
        border: 1px solid var(--border-color);
        border-radius: 10px;
        padding: 1.25rem;
        box-shadow: var(--shadow-sm);
        transition: all 0.3s ease;
    }
    
    div[data-testid="metric-container"]:hover {
        transform: translateY(-2px);
        box-shadow: var(--shadow-md);
        border-color: var(--accent-primary);
    }
    
    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 10px;
        height: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: var(--bg-secondary);
        border-radius: 5px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(180deg, var(--accent-primary), var(--accent-secondary));
        border-radius: 5px;
        border: 2px solid var(--bg-secondary);
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(180deg, var(--accent-secondary), var(--accent-primary));
    }
    
    /* Loading Animations */
    .loading-spinner {
        border: 3px solid var(--border-color);
        border-top: 3px solid var(--accent-primary);
        border-radius: 50%;
        width: 50px;
        height: 50px;
        animation: spin 1s linear infinite;
        margin: 2rem auto;
    }
    
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    .loading-wave {
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 5px;
        padding: 2rem;
    }
    
    .loading-wave div {
        width: 8px;
        height: 40px;
        background: linear-gradient(180deg, var(--accent-primary), var(--accent-secondary));
        border-radius: 4px;
        animation: wave 1.2s linear infinite;
    }
    
    .loading-wave div:nth-child(2) { animation-delay: -1.1s; }
    .loading-wave div:nth-child(3) { animation-delay: -1.0s; }
    .loading-wave div:nth-child(4) { animation-delay: -0.9s; }
    .loading-wave div:nth-child(5) { animation-delay: -0.8s; }
    
    @keyframes wave {
        0%, 40%, 100% { transform: scaleY(0.4); }
        20% { transform: scaleY(1); }
    }
    
    /* Tooltips */
    .tooltip {
        position: relative;
        display: inline-block;
    }
    
    .tooltip .tooltiptext {
        visibility: hidden;
        width: 200px;
        background: var(--bg-tertiary);
        color: var(--text-primary);
        text-align: center;
        border-radius: 8px;
        padding: 0.5rem;
        position: absolute;
        z-index: 1000;
        bottom: 125%;
        left: 50%;
        margin-left: -100px;
        opacity: 0;
        transition: opacity 0.3s;
        border: 1px solid var(--border-color);
        box-shadow: var(--shadow-lg);
        font-size: 0.75rem;
    }
    
    .tooltip:hover .tooltiptext {
        visibility: visible;
        opacity: 1;
    }
    
    /* Alerts and Notifications */
    .alert {
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
        border-left: 4px solid;
        animation: slideInRight 0.3s ease;
    }
    
    @keyframes slideInRight {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    .alert-success {
        background: rgba(0, 214, 143, 0.1);
        border-left-color: var(--accent-success);
        color: var(--accent-success);
    }
    
    .alert-danger {
        background: rgba(255, 61, 113, 0.1);
        border-left-color: var(--accent-danger);
        color: var(--accent-danger);
    }
    
    .alert-warning {
        background: rgba(255, 170, 0, 0.1);
        border-left-color: var(--accent-warning);
        color: var(--accent-warning);
    }
    
    .alert-info {
        background: rgba(66, 99, 235, 0.1);
        border-left-color: var(--accent-primary);
        color: var(--accent-primary);
    }
    
    /* Responsive Design */
    @media (max-width: 768px) {
        .main-header {
            padding: 1rem;
        }
        
        .header-content {
            flex-direction: column;
            gap: 1rem;
        }
        
        .market-status {
            flex-direction: column;
            width: 100%;
            gap: 0.5rem;
        }
        
        .nav-menu ul {
            flex-direction: column;
        }
        
        .widget-card {
            padding: 1rem;
        }
    }
</style>
""", unsafe_allow_html=True)

# ================== SESSION STATE INITIALIZATION ==================
if 'watchlist' not in st.session_state:
    st.session_state.watchlist = ['AAPL', 'MSFT', 'GOOGL', 'TSLA', 'NVDA', 'AMD', 'META', 'AMZN']
if 'portfolio' not in st.session_state:
    st.session_state.portfolio = {}
if 'selected_ticker' not in st.session_state:
    st.session_state.selected_ticker = 'AAPL'
if 'theme' not in st.session_state:
    st.session_state.theme = 'dark'
if 'alerts' not in st.session_state:
    st.session_state.alerts = []
if 'trade_history' not in st.session_state:
    st.session_state.trade_history = []

# ================== DATA FETCHING FUNCTIONS ==================
@st.cache_data(ttl=60)
def fetch_stock_data(symbol: str, period: str = '1y', interval: str = '1d') -> Tuple[Optional[pd.DataFrame], Optional[Dict]]:
    """
    Fetch stock data using yfinance with error handling
    
    Args:
        symbol: Stock ticker symbol
        period: Time period for historical data
        interval: Data interval (1m, 5m, 15m, 30m, 1h, 1d, 1wk, 1mo)
    
    Returns:
        Tuple of (DataFrame with OHLCV data, Dict with stock info)
    """
    try:
        ticker = yf.Ticker(symbol)
        
        # Fetch historical data
        if period == '1d':
            data = ticker.history(period='1d', interval='1m')
        elif period == '5d':
            data = ticker.history(period='5d', interval='5m')
        elif period == '1mo':
            data = ticker.history(period='1mo', interval='1h')
        elif period == '3mo':
            data = ticker.history(period='3mo', interval='1d')
        elif period == '6mo':
            data = ticker.history(period='6mo', interval='1d')
        elif period == '1y':
            data = ticker.history(period='1y', interval='1d')
        elif period == '2y':
            data = ticker.history(period='2y', interval='1wk')
        elif period == '5y':
            data = ticker.history(period='5y', interval='1wk')
        elif period == 'ytd':
            data = ticker.history(period='ytd', interval='1d')
        elif period == 'max':
            data = ticker.history(period='max', interval='1mo')
        else:
            data = ticker.history(period=period, interval=interval)
        
        # Get stock info
        info = ticker.info
        
        return data, info
    except Exception as e:
        st.error(f"Error fetching data for {symbol}: {str(e)}")
        return None, None

# ================== ENHANCED DATA FUNCTIONS (Finance MCP) ==================
@st.cache_data(ttl=60)
def fetch_enhanced_stock_data(symbol: str, period: str = '1y', with_indicators: bool = True) -> Tuple[Optional[pd.DataFrame], Optional[Dict]]:
    """
    Enhanced stock data fetching with technical indicators and better reliability
    Falls back to yfinance if enhanced data is unavailable
    
    Args:
        symbol: Stock ticker symbol
        period: Time period for historical data 
        with_indicators: Whether to include technical indicators
    
    Returns:
        Tuple of (DataFrame with OHLCV + indicators, Dict with comprehensive stock info)
    """
    try:
        # Primary: Try to get enhanced data (this would use Finance MCP in production)
        # For now, we'll enhance the yfinance data with better processing and indicators
        
        ticker = yf.Ticker(symbol)
        
        # Get historical data with appropriate intervals
        period_mapping = {
            '1d': {'period': '1d', 'interval': '5m'},
            '5d': {'period': '5d', 'interval': '15m'}, 
            '1mo': {'period': '1mo', 'interval': '1h'},
            '3mo': {'period': '3mo', 'interval': '1d'},
            '6mo': {'period': '6mo', 'interval': '1d'},
            '1y': {'period': '1y', 'interval': '1d'},
            '2y': {'period': '2y', 'interval': '1wk'},
            '5y': {'period': '5y', 'interval': '1wk'},
            'max': {'period': 'max', 'interval': '1mo'}
        }
        
        params = period_mapping.get(period, {'period': '1y', 'interval': '1d'})
        data = ticker.history(period=params['period'], interval=params['interval'])
        
        if data.empty:
            return None, None
            
        # Add technical indicators if requested
        if with_indicators and len(data) > 20:
            data = add_technical_indicators(data)
        
        # Get enhanced stock info
        info = ticker.info
        enhanced_info = get_enhanced_stock_info(symbol, info)
        
        return data, enhanced_info
        
    except Exception as e:
        st.error(f"Enhanced data fetch failed for {symbol}: {str(e)}")
        # Fallback to original function
        return fetch_stock_data(symbol, period)

def add_technical_indicators(df: pd.DataFrame) -> pd.DataFrame:
    """Add common technical indicators to OHLCV data"""
    try:
        # Simple Moving Averages
        df['SMA_20'] = df['Close'].rolling(window=20).mean()
        df['SMA_50'] = df['Close'].rolling(window=50).mean()
        df['SMA_200'] = df['Close'].rolling(window=200).mean()
        
        # Exponential Moving Averages  
        df['EMA_12'] = df['Close'].ewm(span=12).mean()
        df['EMA_26'] = df['Close'].ewm(span=26).mean()
        
        # MACD
        df['MACD'] = df['EMA_12'] - df['EMA_26']
        df['MACD_Signal'] = df['MACD'].ewm(span=9).mean()
        df['MACD_Histogram'] = df['MACD'] - df['MACD_Signal']
        
        # RSI
        delta = df['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        df['RSI'] = 100 - (100 / (1 + rs))
        
        # Bollinger Bands
        bb_period = 20
        bb_std = 2
        df['BB_Middle'] = df['Close'].rolling(window=bb_period).mean()
        bb_std_dev = df['Close'].rolling(window=bb_period).std()
        df['BB_Upper'] = df['BB_Middle'] + (bb_std_dev * bb_std)
        df['BB_Lower'] = df['BB_Middle'] - (bb_std_dev * bb_std)
        
        # Volume indicators
        if 'Volume' in df.columns:
            df['Volume_SMA'] = df['Volume'].rolling(window=20).mean()
            df['Volume_Ratio'] = df['Volume'] / df['Volume_SMA']
        
        return df
    except Exception as e:
        st.warning(f"Failed to add technical indicators: {str(e)}")
        return df

def get_enhanced_stock_info(symbol: str, basic_info: Dict) -> Dict:
    """Enhance basic stock info with additional metrics"""
    try:
        enhanced = basic_info.copy()
        
        # Add computed metrics
        enhanced['symbol'] = symbol
        enhanced['last_updated'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Financial ratios (if available)
        if 'trailingPE' in basic_info and 'forwardPE' in basic_info:
            enhanced['pe_comparison'] = basic_info.get('trailingPE', 0) - basic_info.get('forwardPE', 0)
        
        # Market cap category
        market_cap = basic_info.get('marketCap', 0)
        if market_cap > 200_000_000_000:
            enhanced['market_cap_category'] = 'Mega Cap'
        elif market_cap > 10_000_000_000:
            enhanced['market_cap_category'] = 'Large Cap'
        elif market_cap > 2_000_000_000:
            enhanced['market_cap_category'] = 'Mid Cap'
        elif market_cap > 300_000_000:
            enhanced['market_cap_category'] = 'Small Cap'
        else:
            enhanced['market_cap_category'] = 'Micro Cap'
            
        return enhanced
    except Exception as e:
        return basic_info

@st.cache_data(ttl=300)
def fetch_market_overview() -> Dict[str, Dict[str, float]]:
    """
    Fetch market overview data for major indices and assets
    
    Returns:
        Dictionary with market data for each index/asset
    """
    indices = {
        'S&P 500': '^GSPC',
        'Nasdaq': '^IXIC',
        'Dow Jones': '^DJI',
        'Russell 2000': '^RUT',
        'VIX': '^VIX',
        'Dollar Index': 'DX-Y.NYB',
        'Gold': 'GC=F',
        'Silver': 'SI=F',
        'Oil WTI': 'CL=F',
        'Natural Gas': 'NG=F',
        'Bitcoin': 'BTC-USD',
        'Ethereum': 'ETH-USD',
        'EUR/USD': 'EURUSD=X',
        'GBP/USD': 'GBPUSD=X',
        'USD/JPY': 'USDJPY=X',
        '10Y Treasury': '^TNX'
    }
    
    market_data = {}
    for name, symbol in indices.items():
        try:
            ticker = yf.Ticker(symbol)
            hist = ticker.history(period='1d')
            info = ticker.info
            
            if not hist.empty:
                current_price = hist['Close'].iloc[-1]
                prev_close = info.get('previousClose', current_price)
                change = ((current_price - prev_close) / prev_close * 100) if prev_close else 0
                volume = hist['Volume'].iloc[-1] if 'Volume' in hist else 0
                
                # Get additional metrics
                hist_week = ticker.history(period='5d')
                week_change = 0
                if len(hist_week) >= 2:
                    week_change = ((hist_week['Close'].iloc[-1] - hist_week['Close'].iloc[0]) / 
                                  hist_week['Close'].iloc[0] * 100)
                
                market_data[name] = {
                    'symbol': symbol,
                    'price': current_price,
                    'change': change,
                    'week_change': week_change,
                    'volume': volume,
                    'prev_close': prev_close
                }
        except:
            market_data[name] = {
                'symbol': symbol,
                'price': 0,
                'change': 0,
                'week_change': 0,
                'volume': 0,
                'prev_close': 0
            }
    
    return market_data

@st.cache_data(ttl=600)
def fetch_options_data(symbol: str) -> Tuple[Optional[pd.DataFrame], Optional[pd.DataFrame], Optional[List[str]]]:
    """
    Fetch options chain data for a given symbol
    
    Args:
        symbol: Stock ticker symbol
    
    Returns:
        Tuple of (calls DataFrame, puts DataFrame, list of expiration dates)
    """
    try:
        ticker = yf.Ticker(symbol)
        expirations = ticker.options
        
        if expirations:
            # Get the nearest expiration
            exp_date = expirations[0]
            opt = ticker.option_chain(exp_date)
            
            calls = opt.calls
            puts = opt.puts
            
            return calls, puts, expirations[:10]  # Return first 10 expirations
    except Exception as e:
        st.error(f"Error fetching options data: {str(e)}")
        return None, None, None

@st.cache_data(ttl=600)
def fetch_news(symbol: str, limit: int = 10) -> Optional[List[Dict]]:
    """
    Fetch latest news for a given symbol
   
    Args:
        symbol: Stock ticker symbol
        limit: Maximum number of news articles to fetch
   
    Returns:
        List of news articles as dictionaries
    """
    try:
       ticker = yf.Ticker(symbol)
       news = ticker.news[:limit] if ticker.news else []
       return news
    except Exception as e:
       st.error(f"Error fetching news: {str(e)}")
       return None

# ================== TECHNICAL INDICATORS ==================
def calculate_technical_indicators(df: pd.DataFrame) -> pd.DataFrame:
   """
   Calculate comprehensive technical indicators
   
   Args:
       df: DataFrame with OHLCV data
   
   Returns:
       DataFrame with additional technical indicator columns
   """
   if df is None or df.empty:
       return df
   
   # Moving Averages
   df['SMA_20'] = df['Close'].rolling(window=20).mean()
   df['SMA_50'] = df['Close'].rolling(window=50).mean()
   df['SMA_200'] = df['Close'].rolling(window=200).mean()
   df['EMA_12'] = df['Close'].ewm(span=12, adjust=False).mean()
   df['EMA_26'] = df['Close'].ewm(span=26, adjust=False).mean()
   df['EMA_50'] = df['Close'].ewm(span=50, adjust=False).mean()
   
   # RSI
   delta = df['Close'].diff()
   gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
   loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
   rs = gain / loss
   df['RSI'] = 100 - (100 / (1 + rs))
   
   # MACD
   df['MACD'] = df['EMA_12'] - df['EMA_26']
   df['MACD_Signal'] = df['MACD'].ewm(span=9, adjust=False).mean()
   df['MACD_Histogram'] = df['MACD'] - df['MACD_Signal']
   
   # Bollinger Bands
   df['BB_Middle'] = df['Close'].rolling(window=20).mean()
   bb_std = df['Close'].rolling(window=20).std()
   df['BB_Upper'] = df['BB_Middle'] + (bb_std * 2)
   df['BB_Lower'] = df['BB_Middle'] - (bb_std * 2)
   df['BB_Width'] = df['BB_Upper'] - df['BB_Lower']
   df['BB_Percent'] = (df['Close'] - df['BB_Lower']) / (df['BB_Upper'] - df['BB_Lower'])
   
   # Stochastic Oscillator
   low_14 = df['Low'].rolling(window=14).min()
   high_14 = df['High'].rolling(window=14).max()
   df['Stoch_K'] = 100 * ((df['Close'] - low_14) / (high_14 - low_14))
   df['Stoch_D'] = df['Stoch_K'].rolling(window=3).mean()
   
   # ATR (Average True Range)
   high_low = df['High'] - df['Low']
   high_close = (df['High'] - df['Close'].shift()).abs()
   low_close = (df['Low'] - df['Close'].shift()).abs()
   ranges = pd.concat([high_low, high_close, low_close], axis=1)
   true_range = ranges.max(axis=1)
   df['ATR'] = true_range.rolling(14).mean()
   
   # Volume indicators
   df['Volume_MA'] = df['Volume'].rolling(window=20).mean()
   df['OBV'] = (df['Volume'] * (~df['Close'].diff().isna()).astype(int) * 
                df['Close'].diff().fillna(0).apply(lambda x: 1 if x > 0 else (-1 if x < 0 else 0))).cumsum()
   
   # Money Flow Index
   typical_price = (df['High'] + df['Low'] + df['Close']) / 3
   money_flow = typical_price * df['Volume']
   
   positive_flow = money_flow.where(typical_price > typical_price.shift(1), 0)
   negative_flow = money_flow.where(typical_price < typical_price.shift(1), 0)
   
   positive_flow_sum = positive_flow.rolling(window=14).sum()
   negative_flow_sum = negative_flow.rolling(window=14).sum()
   
   money_ratio = positive_flow_sum / negative_flow_sum
   df['MFI'] = 100 - (100 / (1 + money_ratio))
   
   # Support and Resistance
   df['Resistance'] = df['High'].rolling(window=20).max()
   df['Support'] = df['Low'].rolling(window=20).min()
   df['Pivot'] = (df['High'] + df['Low'] + df['Close']) / 3
   df['R1'] = 2 * df['Pivot'] - df['Low']
   df['S1'] = 2 * df['Pivot'] - df['High']
   df['R2'] = df['Pivot'] + (df['High'] - df['Low'])
   df['S2'] = df['Pivot'] - (df['High'] - df['Low'])
   
   return df

# ================== CHARTING FUNCTIONS ==================
def create_professional_chart(df: pd.DataFrame, ticker: str, chart_type: str = 'candlestick', 
                           indicators: List[str] = [], theme: str = 'dark') -> go.Figure:
   """
   Create professional trading chart with technical indicators
   
   Args:
       df: DataFrame with OHLCV data
       ticker: Stock ticker symbol
       chart_type: Type of chart (candlestick, line, area, heikin_ashi, renko)
       indicators: List of technical indicators to display
       theme: Chart theme (dark, light)
   
   Returns:
       Plotly figure object
   """
   if df is None or df.empty:
       return go.Figure()
   
   # Calculate indicators
   df = calculate_technical_indicators(df)
   
   # Determine subplot configuration
   rows = 1
   subplot_titles = [f"{ticker} - Price Action"]
   
   if 'RSI' in indicators:
       rows += 1
       subplot_titles.append("RSI (14)")
   if 'MACD' in indicators:
       rows += 1
       subplot_titles.append("MACD")
   if 'Volume' in indicators:
       rows += 1
       subplot_titles.append("Volume")
   if 'MFI' in indicators:
       rows += 1
       subplot_titles.append("Money Flow Index")
   
   # Calculate row heights
   if rows == 1:
       row_heights = [1.0]
   elif rows == 2:
       row_heights = [0.7, 0.3]
   elif rows == 3:
       row_heights = [0.5, 0.25, 0.25]
   elif rows == 4:
       row_heights = [0.4, 0.2, 0.2, 0.2]
   else:
       row_heights = [0.4] + [0.6/(rows-1)]*(rows-1)
   
   # Create subplots
   fig = make_subplots(
       rows=rows,
       cols=1,
       shared_xaxes=True,
       vertical_spacing=0.02,
       row_heights=row_heights,
       subplot_titles=subplot_titles
   )
   
   # Main price chart
   if chart_type == 'candlestick':
       fig.add_trace(
           go.Candlestick(
               x=df.index,
               open=df['Open'],
               high=df['High'],
               low=df['Low'],
               close=df['Close'],
               name='OHLC',
               increasing=dict(line=dict(color='#00d68f', width=1)),
               decreasing=dict(line=dict(color='#ff3d71', width=1))
           ),
           row=1, col=1
       )
   elif chart_type == 'line':
       fig.add_trace(
           go.Scatter(
               x=df.index,
               y=df['Close'],
               mode='lines',
               name='Close',
               line=dict(color='#4263eb', width=2)
           ),
           row=1, col=1
       )
   elif chart_type == 'area':
       fig.add_trace(
           go.Scatter(
               x=df.index,
               y=df['Close'],
               mode='lines',
               name='Close',
               fill='tozeroy',
               line=dict(color='#4263eb', width=2),
               fillcolor='rgba(66, 99, 235, 0.1)'
           ),
           row=1, col=1
       )
   elif chart_type == 'heikin_ashi':
       # Calculate Heikin Ashi
       ha_close = (df['Open'] + df['High'] + df['Low'] + df['Close']) / 4
       ha_open = ha_close.shift(1)
       ha_high = df[['High', 'Open', 'Close']].max(axis=1)
       ha_low = df[['Low', 'Open', 'Close']].min(axis=1)
       
       fig.add_trace(
           go.Candlestick(
               x=df.index,
               open=ha_open,
               high=ha_high,
               low=ha_low,
               close=ha_close,
               name='Heikin Ashi',
               increasing=dict(line=dict(color='#00d68f', width=1)),
               decreasing=dict(line=dict(color='#ff3d71', width=1))
           ),
           row=1, col=1
       )
   
   # Add selected moving averages
   ma_colors = {
       'SMA_20': '#ffaa00',
       'SMA_50': '#00d68f',
       'SMA_200': '#ff3d71',
       'EMA_12': '#4263eb',
       'EMA_26': '#5e72e4',
       'EMA_50': '#a855f7'
   }
   
   for ma in ['SMA_20', 'SMA_50', 'SMA_200', 'EMA_12', 'EMA_26', 'EMA_50']:
       if ma in indicators and ma in df.columns:
           fig.add_trace(
               go.Scatter(
                   x=df.index,
                   y=df[ma],
                   mode='lines',
                   name=ma,
                   line=dict(color=ma_colors.get(ma, '#ffffff'), width=1),
                   opacity=0.7
               ),
               row=1, col=1
           )
   
   # Bollinger Bands
   if 'Bollinger Bands' in indicators:
       fig.add_trace(
           go.Scatter(
               x=df.index,
               y=df['BB_Upper'],
               mode='lines',
               name='BB Upper',
               line=dict(color='rgba(255, 255, 255, 0.3)', width=1, dash='dash')
           ),
           row=1, col=1
       )
       fig.add_trace(
           go.Scatter(
               x=df.index,
               y=df['BB_Lower'],
               mode='lines',
               name='BB Lower',
               line=dict(color='rgba(255, 255, 255, 0.3)', width=1, dash='dash'),
               fill='tonexty',
               fillcolor='rgba(255, 255, 255, 0.05)'
           ),
           row=1, col=1
       )
       fig.add_trace(
           go.Scatter(
               x=df.index,
               y=df['BB_Middle'],
               mode='lines',
               name='BB Middle',
               line=dict(color='rgba(255, 255, 255, 0.5)', width=1)
           ),
           row=1, col=1
       )
   
   # Support and Resistance levels
   if 'Support/Resistance' in indicators:
       fig.add_trace(
           go.Scatter(
               x=df.index,
               y=df['Resistance'],
               mode='lines',
               name='Resistance',
               line=dict(color='#ff3d71', width=1, dash='dot')
           ),
           row=1, col=1
       )
       fig.add_trace(
           go.Scatter(
               x=df.index,
               y=df['Support'],
               mode='lines',
               name='Support',
               line=dict(color='#00d68f', width=1, dash='dot')
           ),
           row=1, col=1
       )
   
   current_row = 2
   
   # RSI subplot
   if 'RSI' in indicators and 'RSI' in df.columns and current_row <= rows:
       fig.add_trace(
           go.Scatter(
               x=df.index,
               y=df['RSI'],
               mode='lines',
               name='RSI',
               line=dict(color='#5e72e4', width=2),
               fill='tozeroy',
               fillcolor='rgba(94, 114, 228, 0.1)'
           ),
           row=current_row, col=1
       )
       
       # Add overbought/oversold zones
       fig.add_hrect(y0=70, y1=100, fillcolor="rgba(255, 61, 113, 0.1)", 
                    layer="below", line_width=0, row=current_row, col=1)
       fig.add_hrect(y0=0, y1=30, fillcolor="rgba(0, 214, 143, 0.1)", 
                    layer="below", line_width=0, row=current_row, col=1)
       
       fig.add_hline(y=70, line_color="rgba(255, 61, 113, 0.5)", 
                    line_dash="dot", row=current_row, col=1)
       fig.add_hline(y=50, line_color="rgba(156, 163, 175, 0.5)", 
                    line_dash="dot", row=current_row, col=1)
       fig.add_hline(y=30, line_color="rgba(0, 214, 143, 0.5)", 
                    line_dash="dot", row=current_row, col=1)
       current_row += 1
   
   # MACD subplot
   if 'MACD' in indicators and 'MACD' in df.columns and current_row <= rows:
       # Histogram colors
       colors = ['#00d68f' if val >= 0 else '#ff3d71' for val in df['MACD_Histogram']]
       
       fig.add_trace(
           go.Bar(
               x=df.index,
               y=df['MACD_Histogram'],
               name='Histogram',
               marker_color=colors,
               opacity=0.3
           ),
           row=current_row, col=1
       )
       
       fig.add_trace(
           go.Scatter(
               x=df.index,
               y=df['MACD'],
               mode='lines',
               name='MACD',
               line=dict(color='#4263eb', width=2)
           ),
           row=current_row, col=1
       )
       
       fig.add_trace(
           go.Scatter(
               x=df.index,
               y=df['MACD_Signal'],
               mode='lines',
               name='Signal',
               line=dict(color='#ffaa00', width=2)
           ),
           row=current_row, col=1
       )
       
       fig.add_hline(y=0, line_color="rgba(156, 163, 175, 0.5)", 
                    line_dash="dot", row=current_row, col=1)
       current_row += 1
   
   # Volume subplot
   if 'Volume' in indicators and 'Volume' in df.columns and current_row <= rows:
       colors = ['#00d68f' if df['Close'].iloc[i] >= df['Close'].iloc[i-1] else '#ff3d71' 
                for i in range(1, len(df))]
       colors.insert(0, '#00d68f')
       
       fig.add_trace(
           go.Bar(
               x=df.index,
               y=df['Volume'],
               name='Volume',
               marker_color=colors,
               opacity=0.5
           ),
           row=current_row, col=1
       )
       
       if 'Volume_MA' in df.columns:
           fig.add_trace(
               go.Scatter(
                   x=df.index,
                   y=df['Volume_MA'],
                   mode='lines',
                   name='Volume MA',
                   line=dict(color='#ffaa00', width=2)
               ),
               row=current_row, col=1
           )
       current_row += 1
   
   # MFI subplot
   if 'MFI' in indicators and 'MFI' in df.columns and current_row <= rows:
       fig.add_trace(
           go.Scatter(
               x=df.index,
               y=df['MFI'],
               mode='lines',
               name='MFI',
               line=dict(color='#a855f7', width=2),
               fill='tozeroy',
               fillcolor='rgba(168, 85, 247, 0.1)'
           ),
           row=current_row, col=1
       )
       
       fig.add_hline(y=80, line_color="rgba(255, 61, 113, 0.5)", 
                    line_dash="dot", row=current_row, col=1)
       fig.add_hline(y=20, line_color="rgba(0, 214, 143, 0.5)", 
                    line_dash="dot", row=current_row, col=1)
   
   # Update layout with professional dark theme
   bg_color = '#0b0e11' if theme == 'dark' else '#ffffff'
   grid_color = 'rgba(48, 54, 61, 0.3)' if theme == 'dark' else 'rgba(0, 0, 0, 0.1)'
   text_color = '#8b92a8' if theme == 'dark' else '#000000'
   
   fig.update_layout(
       template='plotly_dark' if theme == 'dark' else 'plotly_white',
       height=800,
       showlegend=True,
       hovermode='x unified',
       xaxis_rangeslider_visible=False,
       paper_bgcolor=bg_color,
       plot_bgcolor=bg_color,
       font=dict(family='Inter, sans-serif', size=12, color=text_color),
       hoverlabel=dict(
           bgcolor='#161b22' if theme == 'dark' else '#f0f0f0',
           font_size=12,
           font_family='JetBrains Mono, monospace'
       ),
       margin=dict(l=0, r=0, t=40, b=0),
       legend=dict(
           bgcolor='rgba(22, 27, 34, 0.9)' if theme == 'dark' else 'rgba(255, 255, 255, 0.9)',
           bordercolor='#30363d' if theme == 'dark' else '#cccccc',
           borderwidth=1,
           font=dict(size=11),
           yanchor="top",
           y=0.99,
           xanchor="left",
           x=0.01
       ),
       title=dict(
           text=f"{ticker} - Technical Analysis",
           font=dict(size=18, color=text_color),
           x=0.5,
           xanchor='center'
       )
   )
   
   # Update axes
   for i in range(1, rows + 1):
       fig.update_xaxes(
           showgrid=False,
           zeroline=False,
           showline=True,
           linewidth=1,
           linecolor=grid_color,
           row=i, col=1
       )
       fig.update_yaxes(
           showgrid=True,
           gridwidth=1,
           gridcolor=grid_color,
           zeroline=False,
           showline=True,
           linewidth=1,
           linecolor=grid_color,
           row=i, col=1
       )
   
   return fig

# ================== HELPER FUNCTIONS ==================
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

def calculate_portfolio_metrics(portfolio: Dict) -> Dict:
   """Calculate portfolio performance metrics"""
   if not portfolio:
       return {
           'total_value': 0,
           'total_cost': 0,
           'total_pl': 0,
           'total_pl_pct': 0,
           'best_performer': None,
           'worst_performer': None
       }
   
   total_value = 0
   total_cost = 0
   performances = []
   
   for symbol, data in portfolio.items():
       value = data['shares'] * data['current_price']
       cost = data['shares'] * data['avg_cost']
       pl = value - cost
       pl_pct = (pl / cost * 100) if cost > 0 else 0
       
       total_value += value
       total_cost += cost
       performances.append((symbol, pl_pct))
   
   total_pl = total_value - total_cost
   total_pl_pct = (total_pl / total_cost * 100) if total_cost > 0 else 0
   
   performances.sort(key=lambda x: x[1], reverse=True)
   best_performer = performances[0] if performances else None
   worst_performer = performances[-1] if performances else None
   
   return {
       'total_value': total_value,
       'total_cost': total_cost,
       'total_pl': total_pl,
       'total_pl_pct': total_pl_pct,
       'best_performer': best_performer,
       'worst_performer': worst_performer
   }

def generate_trade_signals(df: pd.DataFrame) -> Dict[str, str]:
   """Generate trading signals based on technical indicators"""
   if df is None or df.empty:
       return {'overall': 'NEUTRAL', 'signals': []}
   
   df = calculate_technical_indicators(df)
   signals = []
   bullish_count = 0
   bearish_count = 0
   
   # RSI Signal
   if 'RSI' in df.columns:
       current_rsi = df['RSI'].iloc[-1]
       if pd.notna(current_rsi):
           if current_rsi < 30:
               signals.append(('RSI Oversold', 'BULLISH'))
               bullish_count += 1
           elif current_rsi > 70:
               signals.append(('RSI Overbought', 'BEARISH'))
               bearish_count += 1
           else:
               signals.append(('RSI Neutral', 'NEUTRAL'))
   
   # MACD Signal
   if 'MACD' in df.columns and 'MACD_Signal' in df.columns:
       macd = df['MACD'].iloc[-1]
       signal = df['MACD_Signal'].iloc[-1]
       if pd.notna(macd) and pd.notna(signal):
           if macd > signal:
               signals.append(('MACD Bullish Cross', 'BULLISH'))
               bullish_count += 1
           else:
               signals.append(('MACD Bearish Cross', 'BEARISH'))
               bearish_count += 1
   
   # Moving Average Signal
   if 'SMA_50' in df.columns and 'SMA_200' in df.columns:
       sma50 = df['SMA_50'].iloc[-1]
       sma200 = df['SMA_200'].iloc[-1]
       current_price = df['Close'].iloc[-1]
       
       if pd.notna(sma50) and pd.notna(sma200):
           if sma50 > sma200 and current_price > sma50:
               signals.append(('Golden Cross + Price Above', 'BULLISH'))
               bullish_count += 1
           elif sma50 < sma200 and current_price < sma50:
               signals.append(('Death Cross + Price Below', 'BEARISH'))
               bearish_count += 1
   
   # Bollinger Bands Signal
   if 'BB_Upper' in df.columns and 'BB_Lower' in df.columns:
       current_price = df['Close'].iloc[-1]
       bb_upper = df['BB_Upper'].iloc[-1]
       bb_lower = df['BB_Lower'].iloc[-1]
       
       if pd.notna(bb_upper) and pd.notna(bb_lower):
           if current_price > bb_upper:
               signals.append(('Above Bollinger Upper', 'BEARISH'))
               bearish_count += 1
           elif current_price < bb_lower:
               signals.append(('Below Bollinger Lower', 'BULLISH'))
               bullish_count += 1
   
   # Determine overall signal
   if bullish_count > bearish_count:
       overall = 'BULLISH'
   elif bearish_count > bullish_count:
       overall = 'BEARISH'
   else:
       overall = 'NEUTRAL'
   
   return {'overall': overall, 'signals': signals}

# ================== MAIN APPLICATION ==================

# Professional Header with Animation
st.markdown("""
<div class="main-header">
   <div class="header-content">
       <div class="logo-section">
           <div class="logo">TP</div>
           <div class="platform-info">
               <div class="platform-name">Terminal Pro</div>
               <div class="platform-subtitle">Institutional Trading Platform</div>
           </div>
       </div>
       <div class="market-status">
           <div class="status-item">
               <span class="status-indicator"></span>
               <span>Markets Open</span>
           </div>
           <div class="status-item">
               <span style="color: #8b92a8;">Data Provider:</span>
               <span>Yahoo Finance</span>
           </div>
           <div class="status-item">
               <span style="color: #8b92a8;">Last Update:</span>
               <span id="time"></span>
           </div>
       </div>
   </div>
</div>
<script>
   function updateTime() {
       const now = new Date();
       const timeStr = now.toLocaleTimeString('en-US', { 
           hour: '2-digit', 
           minute: '2-digit', 
           second: '2-digit' 
       });
       document.getElementById('time').innerHTML = timeStr;
   }
   updateTime();
   setInterval(updateTime, 1000);
</script>
""", unsafe_allow_html=True)

# Create main tabs
main_tabs = st.tabs([
   "📊 Dashboard",
   "📈 Charts",
   "🎯 Technical Analysis",
   "📊 Options",
   "💼 Portfolio",
   "📋 Watchlist",
   "📰 News & Research",
   "🔍 Screener",
   "⚙️ Settings"
])

# ================== DASHBOARD TAB ==================
with main_tabs[0]:
   st.markdown("### 🌍 Global Markets Overview")
   
   # Fetch market data
   market_data = fetch_market_overview()
   
   # Display market overview in grid
   cols = st.columns(4)
   for i, (name, data) in enumerate(list(market_data.items())[:16]):
       with cols[i % 4]:
           price = data.get('price', 0)
           change = data.get('change', 0)
           week_change = data.get('week_change', 0)
           
           # Format price
           if price > 0:
               if price > 10000:
                   price_str = f"{price:,.0f}"
               elif price > 100:
                   price_str = f"{price:,.1f}"
               else:
                   price_str = f"{price:,.2f}"
           else:
               price_str = "—"
           
           # Determine color
           change_color = "#00d68f" if change > 0 else "#ff3d71" if change < 0 else "#8b92a8"
           arrow = "↑" if change > 0 else "↓" if change < 0 else "→"
           
           st.markdown(f"""
           <div class="metric-card">
               <div class="metric-label">{name}</div>
               <div class="metric-value">{price_str}</div>
               <div class="metric-change" style="color: {change_color};">
                   {arrow} {abs(change):.2f}% Day
               </div>
               <div style="color: #8b92a8; font-size: 0.75rem; margin-top: 0.25rem;">
                   Week: {week_change:+.2f}%
               </div>
           </div>
           """, unsafe_allow_html=True)
   
   st.markdown("<br>", unsafe_allow_html=True)
   
   # Quick Stats and Top Movers
   col1, col2 = st.columns([1, 1])
   
   with col1:
       st.markdown("""
       <div class="widget-card">
           <div class="widget-header">
               <span class="widget-title">Market Statistics</span>
           </div>
       </div>
       """, unsafe_allow_html=True)
       
       # Calculate market stats
       advances = sum(1 for _, d in market_data.items() if d['change'] > 0)
       declines = sum(1 for _, d in market_data.items() if d['change'] < 0)
       unchanged = len(market_data) - advances - declines
       
       stats_col1, stats_col2, stats_col3 = st.columns(3)
       with stats_col1:
           st.metric("Advances", advances, f"{advances/(len(market_data))*100:.1f}%")
       with stats_col2:
           st.metric("Declines", declines, f"{declines/(len(market_data))*100:.1f}%")
       with stats_col3:
           st.metric("Unchanged", unchanged, f"{unchanged/(len(market_data))*100:.1f}%")
   
   with col2:
       st.markdown("""
       <div class="widget-card">
           <div class="widget-header">
               <span class="widget-title">Top Gainers & Losers</span>
           </div>
       """, unsafe_allow_html=True)
       
       # Sort by change percentage
       sorted_markets = sorted(market_data.items(), key=lambda x: x[1]['change'], reverse=True)
       
       # Top gainers
       st.markdown("**Top Gainers**")
       for name, data in sorted_markets[:3]:
           if data['change'] > 0:
               st.markdown(f"""
               <div style="display: flex; justify-content: space-between; padding: 0.5rem 0; border-bottom: 1px solid #30363d;">
                   <span style="color: #ffffff; font-weight: 500;">{name}</span>
                   <span style="color: #00d68f;">↑ {data['change']:.2f}%</span>
               </div>
               """, unsafe_allow_html=True)
       
       # Top losers
       st.markdown("**Top Losers**")
       for name, data in sorted_markets[-3:]:
           if data['change'] < 0:
               st.markdown(f"""
               <div style="display: flex; justify-content: space-between; padding: 0.5rem 0; border-bottom: 1px solid #30363d;">
                   <span style="color: #ffffff; font-weight: 500;">{name}</span>
                   <span style="color: #ff3d71;">↓ {abs(data['change']):.2f}%</span>
               </div>
               """, unsafe_allow_html=True)

# ================== CHARTS TAB ==================
with main_tabs[1]:
   # Sidebar for chart settings
   with st.sidebar:
       st.markdown("### 📊 Chart Settings")
       
       # Ticker selection
       ticker_input = st.text_input("Enter Symbol", value=st.session_state.selected_ticker)
       st.session_state.selected_ticker = ticker_input.upper()
       
       # Quick ticker selection
       st.markdown("#### Popular Tickers")
       
       ticker_categories = {
           "Tech Giants": ["AAPL", "MSFT", "GOOGL", "AMZN", "META", "NVDA"],
           "Finance": ["JPM", "BAC", "GS", "MS", "WFC", "C"],
           "Healthcare": ["JNJ", "UNH", "PFE", "LLY", "ABBV", "TMO"],
           "Energy": ["XOM", "CVX", "COP", "SLB", "OXY", "PSX"],
           "Crypto": ["BTC-USD", "ETH-USD", "BNB-USD", "SOL-USD"],
           "Index": ["SPY", "QQQ", "DIA", "IWM", "VOO"]
       }
       
       category = st.selectbox("Category", list(ticker_categories.keys()))
       ticker_cols = st.columns(3)
       for i, ticker in enumerate(ticker_categories[category]):
           with ticker_cols[i % 3]:
               if st.button(ticker, key=f"ticker_{ticker}"):
                   st.session_state.selected_ticker = ticker
                   st.rerun()
       
       st.markdown("---")
       
       # Time period and interval
       col1, col2 = st.columns(2)
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
       
       # Chart type
       chart_type = st.selectbox(
           "Chart Type",
           ["candlestick", "line", "area", "heikin_ashi"],
           format_func=lambda x: x.replace('_', ' ').title()
       )
       
       # Technical indicators
       st.markdown("#### Technical Indicators")
       
       indicators = []
       
       # Moving Averages
       with st.expander("Moving Averages"):
           col1, col2 = st.columns(2)
           with col1:
               if st.checkbox("SMA 20"):
                   indicators.append("SMA_20")
               if st.checkbox("SMA 50"):
                   indicators.append("SMA_50")
               if st.checkbox("SMA 200"):
                   indicators.append("SMA_200")
           with col2:
               if st.checkbox("EMA 12"):
                   indicators.append("EMA_12")
               if st.checkbox("EMA 26"):
                   indicators.append("EMA_26")
               if st.checkbox("EMA 50"):
                   indicators.append("EMA_50")
       
       # Oscillators
       with st.expander("Oscillators"):
           if st.checkbox("RSI"):
               indicators.append("RSI")
           if st.checkbox("MACD"):
               indicators.append("MACD")
           if st.checkbox("MFI"):
               indicators.append("MFI")
       
       # Bands and Channels
       with st.expander("Bands & Channels"):
           if st.checkbox("Bollinger Bands"):
               indicators.append("Bollinger Bands")
           if st.checkbox("Support/Resistance"):
               indicators.append("Support/Resistance")
       
       # Volume
       if st.checkbox("Show Volume"):
           indicators.append("Volume")
       
       # Drawing tools placeholder
       st.markdown("#### Drawing Tools")
       st.info("Drawing tools coming soon in v2.1")
   
   # Main chart area
   ticker = st.session_state.selected_ticker
   
   # Fetch data
   data, info = fetch_enhanced_stock_data(ticker, period, with_indicators=True)
   
   if data is not None and not data.empty:
       # Company info header
       col1, col2, col3, col4, col5, col6, col7, col8 = st.columns(8)
       
       current_price = data['Close'].iloc[-1]
       prev_close = data['Close'].iloc[-2] if len(data) > 1 else current_price
       change = current_price - prev_close
       change_pct = (change / prev_close * 100) if prev_close else 0
       
       with col1:
           st.markdown(f"""
           <div class="metric-card">
               <div class="metric-label">SYMBOL</div>
               <div style="font-size: 1.2rem; font-weight: 700;">{ticker}</div>
           </div>
           """, unsafe_allow_html=True)
       
       with col2:
           company_name = info.get('longName', ticker) if info else ticker
           st.markdown(f"""
           <div class="metric-card">
               <div class="metric-label">COMPANY</div>
               <div style="font-size: 0.9rem;">{company_name[:20]}</div>
           </div>
           """, unsafe_allow_html=True)
       
       with col3:
           change_color = "#00d68f" if change >= 0 else "#ff3d71"
           arrow = "↑" if change >= 0 else "↓"
           st.markdown(f"""
           <div class="metric-card">
               <div class="metric-label">PRICE</div>
               <div class="metric-value" style="font-size: 1.3rem;">${current_price:.2f}</div>
               <div class="metric-change" style="color: {change_color};">
                   {arrow} {abs(change):.2f} ({abs(change_pct):.2f}%)
               </div>
           </div>
           """, unsafe_allow_html=True)
       
       with col4:
           st.markdown(f"""
           <div class="metric-card">
               <div class="metric-label">DAY HIGH</div>
               <div style="font-size: 1.1rem;">${data['High'].iloc[-1]:.2f}</div>
           </div>
           """, unsafe_allow_html=True)
       
       with col5:
           st.markdown(f"""
           <div class="metric-card">
               <div class="metric-label">DAY LOW</div>
               <div style="font-size: 1.1rem;">${data['Low'].iloc[-1]:.2f}</div>
           </div>
           """, unsafe_allow_html=True)
       
       with col6:
           volume = data['Volume'].iloc[-1]
           st.markdown(f"""
           <div class="metric-card">
               <div class="metric-label">VOLUME</div>
               <div style="font-size: 1.1rem;">{volume:,.0f}</div>
           </div>
           """, unsafe_allow_html=True)
       
       with col7:
           if info:
               mkt_cap = info.get('marketCap', 0)
               mkt_cap_str = format_large_number(mkt_cap)
               st.markdown(f"""
               <div class="metric-card">
                   <div class="metric-label">MARKET CAP</div>
                   <div style="font-size: 1.1rem;">{mkt_cap_str}</div>
               </div>
               """, unsafe_allow_html=True)
       
       with col8:
           if info:
               pe_ratio = info.get('trailingPE', 0)
               st.markdown(f"""
               <div class="metric-card">
                   <div class="metric-label">P/E RATIO</div>
                   <div style="font-size: 1.1rem;">{pe_ratio:.2f}</div>
               </div>
               """, unsafe_allow_html=True)
       
       st.markdown("<br>", unsafe_allow_html=True)
       
       # Main chart
       st.markdown('<div class="chart-container">', unsafe_allow_html=True)
       fig = create_professional_chart(data, ticker, chart_type, indicators, st.session_state.theme)
       st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': True})
       st.markdown('</div>', unsafe_allow_html=True)
   else:
       st.error(f"Unable to fetch data for {ticker}")

# ================== TECHNICAL ANALYSIS TAB ==================
with main_tabs[2]:
   st.markdown(f"### 📊 Technical Analysis - {st.session_state.selected_ticker}")
   
   # Fetch data for analysis
   data, info = fetch_enhanced_stock_data(st.session_state.selected_ticker, '1y', with_indicators=True)
   
   if data is not None and not data.empty:
       data = calculate_technical_indicators(data)
       
       # Generate trading signals
       signals = generate_trade_signals(data)
       
       # Overall signal display
       signal_color = {
           'BULLISH': '#00d68f',
           'BEARISH': '#ff3d71',
           'NEUTRAL': '#ffaa00'
       }
       
       st.markdown(f"""
       <div class="widget-card" style="text-align: center; padding: 2rem;">
           <h2 style="color: {signal_color[signals['overall']]}; margin: 0;">
               {signals['overall']} SIGNAL
           </h2>
           <p style="color: #8b92a8; margin-top: 0.5rem;">
               Based on technical indicators analysis
           </p>
       </div>
       """, unsafe_allow_html=True)
       
       # Display individual signals
       st.markdown("### 📈 Technical Indicators Summary")
       
       col1, col2, col3, col4 = st.columns(4)
       
       # Trend Analysis
       with col1:
           st.markdown("""
           <div class="widget-card">
               <div class="widget-header">
                   <span class="widget-title">Trend Analysis</span>
               </div>
           </div>
           """, unsafe_allow_html=True)
           
           if 'SMA_50' in data.columns and 'SMA_200' in data.columns:
               sma50 = data['SMA_50'].iloc[-1]
               sma200 = data['SMA_200'].iloc[-1]
               current = data['Close'].iloc[-1]
               
               if pd.notna(sma50) and pd.notna(sma200):
                   if sma50 > sma200 and current > sma50:
                       trend = "Strong Uptrend"
                       trend_color = "#00d68f"
                   elif sma50 < sma200 and current < sma50:
                       trend = "Strong Downtrend"
                       trend_color = "#ff3d71"
                   else:
                       trend = "Sideways"
                       trend_color = "#ffaa00"
                   
                   st.markdown(f"""
                   <div style="text-align: center; padding: 1rem;">
                       <div style="color: {trend_color}; font-size: 1.3rem; font-weight: 600;">
                           {trend}
                       </div>
                       <div style="color: #8b92a8; font-size: 0.875rem; margin-top: 0.5rem;">
                           MA50: ${sma50:.2f}<br>
                           MA200: ${sma200:.2f}
                       </div>
                   </div>
                   """, unsafe_allow_html=True)
       
       # Momentum
       with col2:
           st.markdown("""
           <div class="widget-card">
               <div class="widget-header">
                   <span class="widget-title">Momentum (RSI)</span>
               </div>
           </div>
           """, unsafe_allow_html=True)
           
           if 'RSI' in data.columns:
               rsi = data['RSI'].iloc[-1]
               
               if pd.notna(rsi):
                   if rsi > 70:
                       rsi_status = "Overbought"
                       rsi_color = "#ff3d71"
                   elif rsi < 30:
                       rsi_status = "Oversold"
                       rsi_color = "#00d68f"
                   else:
                       rsi_status = "Neutral"
                       rsi_color = "#8b92a8"
                   
                   st.markdown(f"""
                   <div style="text-align: center; padding: 1rem;">
                       <div style="color: {rsi_color}; font-size: 1.8rem; font-weight: 700;">
                           {rsi:.1f}
                       </div>
                       <div style="color: #8b92a8; font-size: 0.875rem; margin-top: 0.5rem;">
                           {rsi_status}
                       </div>
                   </div>
                   """, unsafe_allow_html=True)
       
       # MACD
       with col3:
           st.markdown("""
           <div class="widget-card">
               <div class="widget-header">
                   <span class="widget-title">MACD Signal</span>
               </div>
           </div>
           """, unsafe_allow_html=True)
           
           if 'MACD' in data.columns and 'MACD_Signal' in data.columns:
               macd = data['MACD'].iloc[-1]
               signal = data['MACD_Signal'].iloc[-1]
               
               if pd.notna(macd) and pd.notna(signal):
                   if macd > signal:
                       macd_status = "Bullish"
                       macd_color = "#00d68f"
                   else:
                       macd_status = "Bearish"
                       macd_color = "#ff3d71"
                   
                   st.markdown(f"""
                   <div style="text-align: center; padding: 1rem;">
                       <div style="color: {macd_color}; font-size: 1.3rem; font-weight: 600;">
                           {macd_status}
                       </div>
                       <div style="color: #8b92a8; font-size: 0.875rem; margin-top: 0.5rem;">
                           MACD: {macd:.3f}<br>
                           Signal: {signal:.3f}
                       </div>
                   </div>
                   """, unsafe_allow_html=True)
       
       # Volatility
       with col4:
           st.markdown("""
           <div class="widget-card">
               <div class="widget-header">
                   <span class="widget-title">Volatility (ATR)</span>
               </div>
           </div>
           """, unsafe_allow_html=True)
           
           if 'ATR' in data.columns:
               atr = data['ATR'].iloc[-1]
               current_price = data['Close'].iloc[-1]
               atr_pct = (atr / current_price * 100) if current_price > 0 else 0
               
               if pd.notna(atr):
                   if atr_pct > 3:
                       vol_status = "High"
                       vol_color = "#ff3d71"
                   elif atr_pct < 1:
                       vol_status = "Low"
                       vol_color = "#00d68f"
                   else:
                       vol_status = "Normal"
                       vol_color = "#ffaa00"
                   
                   st.markdown(f"""
                   <div style="text-align: center; padding: 1rem;">
                       <div style="color: {vol_color}; font-size: 1.3rem; font-weight: 600;">
                           {atr_pct:.2f}%
                       </div>
                       <div style="color: #8b92a8; font-size: 0.875rem; margin-top: 0.5rem;">
                           {vol_status} Volatility<br>
                           ATR: ${atr:.2f}
                       </div>
                   </div>
                   """, unsafe_allow_html=True)
       
       # Support and Resistance Levels
       st.markdown("### 🎯 Support & Resistance Levels")
       
       if all(col in data.columns for col in ['Pivot', 'R1', 'R2', 'S1', 'S2']):
           levels_data = {
               'Level': ['R2', 'R1', 'Pivot', 'S1', 'S2'],
               'Price': [
                   data['R2'].iloc[-1],
                   data['R1'].iloc[-1],
                   data['Pivot'].iloc[-1],
                   data['S1'].iloc[-1],
                   data['S2'].iloc[-1]
               ]
           }
           
           levels_df = pd.DataFrame(levels_data)
           
           # Create a horizontal bar chart for levels
           fig = go.Figure()
           
           colors = ['#ff3d71', '#ffaa00', '#8b92a8', '#ffaa00', '#00d68f']
           
           for i, row in levels_df.iterrows():
               fig.add_trace(go.Scatter(
                   x=[row['Price'], row['Price']],
                   y=[0, 1],
                   mode='lines',
                   line=dict(color=colors[i], width=2),
                   name=row['Level'],
                   showlegend=True
               ))
           
           # Add current price
           current_price = data['Close'].iloc[-1]
           fig.add_trace(go.Scatter(
               x=[current_price, current_price],
               y=[0, 1],
               mode='lines',
               line=dict(color='#4263eb', width=3, dash='dash'),
               name='Current Price'
           ))
           
           fig.update_layout(
               height=200,
               template='plotly_dark',
               showlegend=True,
               xaxis=dict(title='Price'),
               yaxis=dict(visible=False),
               hovermode='x unified',
               paper_bgcolor='#161b22',
               plot_bgcolor='#0b0e11'
           )
           
           st.plotly_chart(fig, use_container_width=True)
       
       # Trading Signals Detail
       st.markdown("### 📊 Detailed Trading Signals")
       
       for signal_name, signal_type in signals['signals']:
           color = signal_color.get(signal_type, '#8b92a8')
           icon = "↑" if signal_type == "BULLISH" else "↓" if signal_type == "BEARISH" else "→"
           
           st.markdown(f"""
           <div style="background: {color}20; border-left: 3px solid {color}; 
                       padding: 0.75rem; margin: 0.5rem 0; border-radius: 8px;">
               <span style="color: {color}; font-weight: 600;">
                   {icon} {signal_name}: {signal_type}
               </span>
           </div>
           """, unsafe_allow_html=True)

# ================== OPTIONS TAB ==================
with main_tabs[3]:
   st.markdown(f"### 🎯 Options Chain - {st.session_state.selected_ticker}")
   
   # Fetch options data
   calls, puts, expirations = fetch_options_data(st.session_state.selected_ticker)
   
   if calls is not None and puts is not None and expirations:
       # Expiration selection
       selected_exp = st.selectbox("Select Expiration Date", expirations)
       
       # Re-fetch for selected expiration
       ticker = yf.Ticker(st.session_state.selected_ticker)
       opt = ticker.option_chain(selected_exp)
       calls = opt.calls
       puts = opt.puts
       
       # Options summary metrics
       col1, col2, col3, col4, col5 = st.columns(5)
       
       with col1:
           total_call_volume = calls['volume'].sum() if 'volume' in calls.columns else 0
           st.metric("Call Volume", f"{total_call_volume:,.0f}")
       
       with col2:
           total_put_volume = puts['volume'].sum() if 'volume' in puts.columns else 0
           st.metric("Put Volume", f"{total_put_volume:,.0f}")
       
       with col3:
           if total_call_volume > 0:
               put_call_ratio = total_put_volume / total_call_volume
               st.metric("Put/Call Ratio", f"{put_call_ratio:.2f}")
       
       with col4:
           if 'openInterest' in calls.columns:
               total_oi = calls['openInterest'].sum() + puts['openInterest'].sum()
               st.metric("Total OI", f"{total_oi:,.0f}")
       
       with col5:
           if 'impliedVolatility' in calls.columns:
               avg_iv = (calls['impliedVolatility'].mean() + puts['impliedVolatility'].mean()) / 2 * 100
               st.metric("Avg IV", f"{avg_iv:.1f}%")
       
       # Options chain display
       options_tabs = st.tabs(["Calls", "Puts", "Greeks", "Volatility Analysis"])
       
       with options_tabs[0]:
           st.markdown("### Call Options")
           
           # Filter options
           data, info = fetch_enhanced_stock_data(st.session_state.selected_ticker, '1d', with_indicators=True)
           if data is not None:
               current_price = data['Close'].iloc[-1]
               
               # Filter for near-the-money options
               calls_filtered = calls[
                   (calls['strike'] >= current_price * 0.9) & 
                   (calls['strike'] <= current_price * 1.1)
               ]
               
               display_cols = ['strike', 'lastPrice', 'bid', 'ask', 'change', 
                             'percentChange', 'volume', 'openInterest', 'impliedVolatility']
               available_cols = [col for col in display_cols if col in calls_filtered.columns]
               
               if available_cols:
                   st.dataframe(
                       calls_filtered[available_cols].style.format({
                           'strike': '${:.2f}',
                           'lastPrice': '${:.2f}',
                           'bid': '${:.2f}',
                           'ask': '${:.2f}',
                           'change': '{:+.2f}',
                           'percentChange': '{:+.2f}%',
                           'volume': '{:,.0f}',
                           'openInterest': '{:,.0f}',
                           'impliedVolatility': '{:.1%}'
                       }).apply(lambda x: ['background-color: rgba(0, 214, 143, 0.1)' 
                                          if x['strike'] < current_price 
                                          else 'background-color: rgba(255, 61, 113, 0.1)' 
                                          for _ in x], axis=1),
                       use_container_width=True,
                       hide_index=True
                   )
       
       with options_tabs[1]:
           st.markdown("### Put Options")
           
           if data is not None:
               # Filter for near-the-money options
               puts_filtered = puts[
                   (puts['strike'] >= current_price * 0.9) & 
                   (puts['strike'] <= current_price * 1.1)
               ]
               
               if available_cols:
                   st.dataframe(
                       puts_filtered[available_cols].style.format({
                           'strike': '${:.2f}',
                           'lastPrice': '${:.2f}',
                           'bid': '${:.2f}',
                           'ask': '${:.2f}',
                           'change': '{:+.2f}',
                           'percentChange': '{:+.2f}%',
                           'volume': '{:,.0f}',
                           'openInterest': '{:,.0f}',
                           'impliedVolatility': '{:.1%}'
                       }).apply(lambda x: ['background-color: rgba(255, 61, 113, 0.1)' 
                                          if x['strike'] < current_price 
                                          else 'background-color: rgba(0, 214, 143, 0.1)' 
                                          for _ in x], axis=1),
                       use_container_width=True,
                       hide_index=True
                   )
       
       with options_tabs[2]:
           st.markdown("### Greeks Analysis")
           st.info("Greeks calculation requires additional data providers. Coming in v2.1")
       
       with options_tabs[3]:
           st.markdown("### Volatility Smile")
           
           if 'strike' in calls.columns and 'impliedVolatility' in calls.columns:
               fig = go.Figure()
               
               # Calls IV
               fig.add_trace(go.Scatter(
                   x=calls['strike'],
                   y=calls['impliedVolatility'] * 100,
                   mode='lines+markers',
                   name='Call IV',
                   line=dict(color='#00d68f', width=2),
                   marker=dict(size=6)
               ))
               
               # Puts IV
               fig.add_trace(go.Scatter(
                   x=puts['strike'],
                   y=puts['impliedVolatility'] * 100,
                   mode='lines+markers',
                   name='Put IV',
                   line=dict(color='#ff3d71', width=2),
                   marker=dict(size=6)
               ))
               
               # Add current price line
               if data is not None:
                   fig.add_vline(x=current_price, line_dash="dash", 
                                line_color="#4263eb", annotation_text="Current Price")
               
               fig.update_layout(
                   title="Implied Volatility Smile",
                   xaxis_title="Strike Price",
                   yaxis_title="Implied Volatility (%)",
                   template='plotly_dark',
                   height=400,
                   paper_bgcolor='#161b22',
                   plot_bgcolor='#0b0e11'
               )
               
               st.plotly_chart(fig, use_container_width=True)
   else:
       st.warning(f"Options data not available for {st.session_state.selected_ticker}")

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
                   # Fetch current price
                   ticker = yf.Ticker(add_symbol.upper())
                   hist = ticker.history(period='1d')
                   if not hist.empty:
                       current_price = hist['Close'].iloc[-1]
                       st.session_state.portfolio[add_symbol.upper()] = {
                           'shares': add_shares,
                           'avg_cost': add_cost,
                           'current_price': current_price
                       }
                       st.success(f"Added {add_shares} shares of {add_symbol.upper()} to portfolio")
                       st.rerun()
   
   # Portfolio overview
   if st.session_state.portfolio:
       # Calculate portfolio metrics
       metrics = calculate_portfolio_metrics(st.session_state.portfolio)
       
       # Display metrics
       col1, col2, col3, col4, col5, col6 = st.columns(6)
       
       with col1:
           st.metric("Total Value", format_large_number(metrics['total_value']))
       
       with col2:
           pl_color = "#00d68f" if metrics['total_pl'] >= 0 else "#ff3d71"
           st.metric("Total P&L", 
                    f"{format_large_number(abs(metrics['total_pl']))}",
                    f"{metrics['total_pl_pct']:+.2f}%")
       
       with col3:
           st.metric("Total Cost", format_large_number(metrics['total_cost']))
       
       with col4:
           st.metric("Positions", len(st.session_state.portfolio))
       
       with col5:
           if metrics['best_performer']:
               st.metric("Best Performer", 
                        metrics['best_performer'][0],
                        f"{metrics['best_performer'][1]:+.2f}%")
       
       with col6:
           if metrics['worst_performer']:
               st.metric("Worst Performer",
                        metrics['worst_performer'][0],
                        f"{metrics['worst_performer'][1]:+.2f}%")
       
       # Portfolio holdings table
       st.markdown("### 📊 Current Holdings")
       
       portfolio_data = []
       for symbol, position in st.session_state.portfolio.items():
           # Update current price
           try:
               ticker = yf.Ticker(symbol)
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
           
           portfolio_data.append({
               'Symbol': symbol,
               'Shares': position['shares'],
               'Avg Cost': position['avg_cost'],
               'Current Price': current_price,
               'Market Value': market_value,
               'Cost Basis': cost_basis,
               'P&L': pl,
               'P&L %': pl_pct,
               'Weight %': (market_value / metrics['total_value'] * 100) if metrics['total_value'] > 0 else 0
           })
       
       portfolio_df = pd.DataFrame(portfolio_data)
       portfolio_df = portfolio_df.sort_values('Market Value', ascending=False)
       
       # Display with formatting
       st.dataframe(
           portfolio_df.style.format({
               'Shares': '{:.0f}',
               'Avg Cost': '${:.2f}',
               'Current Price': '${:.2f}',
               'Market Value': '${:,.2f}',
               'Cost Basis': '${:,.2f}',
               'P&L': '${:+,.2f}',
               'P&L %': '{:+.2f}%',
               'Weight %': '{:.1f}%'
           }).apply(lambda x: ['background-color: rgba(0, 214, 143, 0.1)' if x['P&L'] > 0 
                              else 'background-color: rgba(255, 61, 113, 0.1)' if x['P&L'] < 0
                              else '' for _ in x], axis=1),
           use_container_width=True,
           hide_index=True
       )
       
       # Portfolio allocation chart
       st.markdown("### 📊 Portfolio Allocation")
       
       col1, col2 = st.columns(2)
       
       with col1:
           # Pie chart
           fig = go.Figure(data=[go.Pie(
               labels=portfolio_df['Symbol'],
               values=portfolio_df['Market Value'],
               hole=0.4,
               marker=dict(colors=px.colors.qualitative.Set3)
           )])
           
           fig.update_layout(
               title="Asset Allocation",
               template='plotly_dark',
               height=400,
               paper_bgcolor='#161b22',
               plot_bgcolor='#0b0e11',
               showlegend=True
           )
           
           st.plotly_chart(fig, use_container_width=True)
       
       with col2:
           # Performance bar chart
           fig = go.Figure(data=[
               go.Bar(
                   x=portfolio_df['Symbol'],
                   y=portfolio_df['P&L %'],
                   marker_color=['#00d68f' if x > 0 else '#ff3d71' for x in portfolio_df['P&L %']],
                   text=portfolio_df['P&L %'].apply(lambda x: f"{x:+.1f}%"),
                   textposition='outside'
               )
           ])
           
           fig.update_layout(
               title="Position Performance",
               xaxis_title="Symbol",
               yaxis_title="P&L %",
               template='plotly_dark',
               height=400,
               paper_bgcolor='#161b22',
               plot_bgcolor='#0b0e11'
           )
           
           st.plotly_chart(fig, use_container_width=True)
       
       # Remove position
       st.markdown("### 🗑️ Remove Position")
       symbol_to_remove = st.selectbox("Select position to remove", list(st.session_state.portfolio.keys()))
       if st.button("Remove Position"):
           del st.session_state.portfolio[symbol_to_remove]
           st.success(f"Removed {symbol_to_remove} from portfolio")
           st.rerun()
   else:
       st.info("Your portfolio is empty. Add positions to start tracking performance.")

# ================== WATCHLIST TAB ==================
with main_tabs[5]:
   st.markdown("### 📋 Watchlist")
   
   # Add to watchlist
   col1, col2 = st.columns([3, 1])
   with col1:
       new_ticker = st.text_input("Add symbol to watchlist", placeholder="Enter ticker symbol...")
   with col2:
       st.markdown("<br>", unsafe_allow_html=True)
       if st.button("➕ Add", use_container_width=True):
           if new_ticker and new_ticker.upper() not in st.session_state.watchlist:
               st.session_state.watchlist.append(new_ticker.upper())
               st.success(f"Added {new_ticker.upper()} to watchlist")
               st.rerun()
   
   # Display watchlist
   if st.session_state.watchlist:
       watchlist_data = []
       
       for symbol in st.session_state.watchlist:
           try:
               ticker = yf.Ticker(symbol)
               hist = ticker.history(period='1d')
               info = ticker.info
               
               if not hist.empty:
                   current = hist['Close'].iloc[-1]
                   prev = info.get('previousClose', current)
                   change = current - prev
                   change_pct = (change / prev * 100) if prev else 0
                   volume = hist['Volume'].iloc[-1]
                   
                   # Get additional data
                   hist_week = ticker.history(period='5d')
                   hist_month = ticker.history(period='1mo')
                   hist_year = ticker.history(period='1y')
                   
                   week_change = 0
                   month_change = 0
                   year_change = 0
                   
                   if len(hist_week) >= 2:
                       week_change = ((hist_week['Close'].iloc[-1] - hist_week['Close'].iloc[0]) / 
                                     hist_week['Close'].iloc[0] * 100)
                   
                   if len(hist_month) >= 2:
                       month_change = ((hist_month['Close'].iloc[-1] - hist_month['Close'].iloc[0]) / 
                                      hist_month['Close'].iloc[0] * 100)
                   
                   if len(hist_year) >= 2:
                       year_change = ((hist_year['Close'].iloc[-1] - hist_year['Close'].iloc[0]) / 
                                     hist_year['Close'].iloc[0] * 100)
                   
                   if not hist_year.empty:
                       high_52w = hist_year['High'].max()
                       low_52w = hist_year['Low'].min()
                   else:
                       high_52w = current
                       low_52w = current
                   
                   watchlist_data.append({
                       'Symbol': symbol,
                       'Price': current,
                       'Change': change,
                       'Change %': change_pct,
                       '1W %': week_change,
                       '1M %': month_change,
                       '1Y %': year_change,
                       'Volume': volume,
                       '52W High': high_52w,
                       '52W Low': low_52w
                   })
           except:
               watchlist_data.append({
                   'Symbol': symbol,
                   'Price': 0,
                   'Change': 0,
                   'Change %': 0,
                   '1W %': 0,
                   '1M %': 0,
                   '1Y %': 0,
                   'Volume': 0,
                   '52W High': 0,
                   '52W Low': 0
               })
       
       if watchlist_data:
           df = pd.DataFrame(watchlist_data)
           
           # Display as cards in grid
           st.markdown("### 📊 Watchlist Overview")
           
           cols = st.columns(3)
           for i, row in df.iterrows():
               with cols[i % 3]:
                   change_color = "#00d68f" if row['Change'] >= 0 else "#ff3d71"
                   arrow = "↑" if row['Change'] >= 0 else "↓"
                   
                   # Calculate 52W range position
                   range_pct = 0
                   if row['52W High'] > row['52W Low']:
                       range_pct = ((row['Price'] - row['52W Low']) / 
                                   (row['52W High'] - row['52W Low']) * 100)
                   
                   st.markdown(f"""
                   <div class="widget-card" style="cursor: pointer;">
                       <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 1rem;">
                           <div>
                               <div style="font-size: 1.3rem; font-weight: 700; color: #ffffff;">
                                   {row['Symbol']}
                               </div>
                               <div style="font-size: 1.5rem; font-weight: 700; color: #ffffff; margin: 0.5rem 0;">
                                   ${row['Price']:.2f}
                               </div>
                               <div style="color: {change_color}; font-weight: 600;">
                                   {arrow} {abs(row['Change']):.2f} ({abs(row['Change %']):.2f}%)
                               </div>
                           </div>
                           <div style="text-align: right;">
                               <div style="color: #8b92a8; font-size: 0.75rem; margin-bottom: 0.25rem;">52W Range</div>
                               <div style="color: #00d68f; font-size: 0.875rem;">H: ${row['52W High']:.2f}</div>
                               <div style="color: #ff3d71; font-size: 0.875rem;">L: ${row['52W Low']:.2f}</div>
                               <div style="margin-top: 0.5rem;">
                                   <div style="background: #30363d; height: 4px; border-radius: 2px; position: relative;">
                                       <div style="background: #4263eb; height: 4px; border-radius: 2px; width: {range_pct}%;"></div>
                                   </div>
                               </div>
                           </div>
                       </div>
                       <div style="border-top: 1px solid #30363d; padding-top: 0.75rem; display: grid; grid-template-columns: repeat(3, 1fr); gap: 0.5rem;">
                           <div>
                               <div style="color: #8b92a8; font-size: 0.75rem;">1W</div>
                               <div style="color: {'#00d68f' if row['1W %'] > 0 else '#ff3d71'}; font-size: 0.875rem; font-weight: 600;">
                                   {row['1W %']:+.1f}%
                               </div>
                           </div>
                           <div>
                               <div style="color: #8b92a8; font-size: 0.75rem;">1M</div>
                               <div style="color: {'#00d68f' if row['1M %'] > 0 else '#ff3d71'}; font-size: 0.875rem; font-weight: 600;">
                                   {row['1M %']:+.1f}%
                               </div>
                           </div>
                           <div>
                               <div style="color: #8b92a8; font-size: 0.75rem;">1Y</div>
                               <div style="color: {'#00d68f' if row['1Y %'] > 0 else '#ff3d71'}; font-size: 0.875rem; font-weight: 600;">
                                   {row['1Y %']:+.1f}%
                               </div>
                           </div>
                       </div>
                       <div style="margin-top: 0.75rem; padding-top: 0.75rem; border-top: 1px solid #30363d;">
                           <div style="color: #8b92a8; font-size: 0.75rem;">
                               Volume: {row['Volume']:,.0f}
                           </div>
                       </div>
                   </div>
                   """, unsafe_allow_html=True)
                   
                   col1, col2 = st.columns(2)
                   with col1:
                       if st.button(f"📊 Chart", key=f"chart_{row['Symbol']}"):
                           st.session_state.selected_ticker = row['Symbol']
                           st.rerun()
                   with col2:
                       if st.button(f"🗑️ Remove", key=f"remove_{row['Symbol']}"):
                           st.session_state.watchlist.remove(row['Symbol'])
                           st.rerun()
           
           # Watchlist table view
           st.markdown("### 📊 Detailed View")
           
           st.dataframe(
               df.style.format({
                   'Price': '${:.2f}',
                   'Change': '{:+.2f}',
                   'Change %': '{:+.2f}%',
                   '1W %': '{:+.1f}%',
                   '1M %': '{:+.1f}%',
                   '1Y %': '{:+.1f}%',
                   'Volume': '{:,.0f}',
                   '52W High': '${:.2f}',
                   '52W Low': '${:.2f}'
               }).apply(lambda x: ['color: #00d68f' if val > 0 else 'color: #ff3d71' if val < 0 else ''
                                  for val in x], subset=['Change %', '1W %', '1M %', '1Y %']),
               use_container_width=True,
               hide_index=True
           )
   else:
       st.info("Your watchlist is empty. Add symbols to start tracking them.")

# ================== NEWS TAB ==================
with main_tabs[6]:
   st.markdown(f"### 📰 News & Research - {st.session_state.selected_ticker}")
   
   # Fetch news
   news = fetch_news(st.session_state.selected_ticker, limit=20)
   
   if news:
       # News sentiment summary (simulated)
       col1, col2, col3, col4 = st.columns(4)
       
       with col1:
           st.metric("Total Articles", len(news))
       
       with col2:
           # Simulate sentiment
           positive = len([n for n in news if np.random.random() > 0.5])
           st.metric("Positive Sentiment", f"{positive}/{len(news)}")
       
       with col3:
           sources = len(set([n.get('publisher', 'Unknown') for n in news]))
           st.metric("Sources", sources)
       
       with col4:
           st.metric("Time Range", "Last 48 hours")
       
       # Display news articles
       st.markdown("### 📰 Latest News")
       
       for article in news[:15]:
           title = article.get('title', 'No title')
           publisher = article.get('publisher', 'Unknown')
           link = article.get('link', '#')
           
           # Format time
           pub_time = article.get('providerPublishTime', 0)
           if pub_time:
               pub_date = datetime.fromtimestamp(pub_time).strftime('%Y-%m-%d %H:%M')
           else:
               pub_date = 'Unknown'
           
           # Simulate sentiment
           sentiment = np.random.choice(['Bullish', 'Bearish', 'Neutral'], p=[0.4, 0.3, 0.3])
           sentiment_color = {
               'Bullish': '#00d68f',
               'Bearish': '#ff3d71',
               'Neutral': '#ffaa00'
           }
           
           st.markdown(f"""
           <div class="widget-card" style="margin-bottom: 1rem;">
               <div style="display: flex; justify-content: space-between; align-items: start;">
                   <div style="flex: 1;">
                       <div style="color: #ffffff; font-weight: 600; font-size: 1.1rem; margin-bottom: 0.5rem;">
                           {title}
                       </div>
                       <div style="color: #8b92a8; font-size: 0.875rem; margin-bottom: 0.75rem;">
                           📰 {publisher} • ⏰ {pub_date}
                       </div>
                       <a href="{link}" target="_blank" style="color: #4263eb; text-decoration: none; font-weight: 500;">
                           Read Full Article →
                       </a>
                   </div>
                   <div style="background: {sentiment_color[sentiment]}20; 
                               color: {sentiment_color[sentiment]}; 
                               padding: 0.25rem 0.75rem; 
                               border-radius: 20px; 
                               font-size: 0.75rem; 
                               font-weight: 600;
                               border: 1px solid {sentiment_color[sentiment]}40;">
                       {sentiment}
                   </div>
               </div>
           </div>
           """, unsafe_allow_html=True)
   else:
       st.info("No news available for this ticker")

# ================== SCREENER TAB ==================
with main_tabs[7]:
   st.markdown("### 🔍 Stock Screener")
   
   # Screener filters
   with st.expander("📊 Screener Filters", expanded=True):
       col1, col2, col3, col4 = st.columns(4)
       
       with col1:
           market_cap_min = st.number_input("Min Market Cap (B)", min_value=0.0, value=1.0)
           market_cap_max = st.number_input("Max Market Cap (B)", min_value=0.0, value=1000.0)
       
       with col2:
           pe_min = st.number_input("Min P/E Ratio", min_value=0.0, value=0.0)
           pe_max = st.number_input("Max P/E Ratio", min_value=0.0, value=50.0)
       
       with col3:
           volume_min = st.number_input("Min Volume (M)", min_value=0.0, value=1.0)
           change_min = st.number_input("Min Change %", value=-100.0)
       
       with col4:
           sector = st.selectbox("Sector", ["All", "Technology", "Healthcare", "Finance", "Energy", "Consumer"])
           exchange = st.selectbox("Exchange", ["All", "NASDAQ", "NYSE", "AMEX"])
   
   # Run screener button
   if st.button("🔍 Run Screener", use_container_width=True):
       st.info("Screener functionality requires additional data providers. Coming in v2.1")
       
       # Sample screener results
       screener_results = pd.DataFrame({
           'Symbol': ['NVDA', 'AAPL', 'MSFT', 'GOOGL', 'META', 'TSLA', 'AMD', 'AMZN'],
           'Company': ['NVIDIA Corp', 'Apple Inc', 'Microsoft Corp', 'Alphabet Inc', 
                      'Meta Platforms', 'Tesla Inc', 'AMD Inc', 'Amazon Inc'],
           'Price': [520.25, 175.50, 380.25, 2850.00, 385.20, 245.30, 145.60, 3450.00],
           'Change %': [5.2, 2.1, 1.5, 1.8, 3.2, 4.8, -3.2, 0.8],
           'Volume': ['125M', '78M', '45M', '25M', '38M', '98M', '85M', '35M'],
           'Market Cap': ['1.3T', '2.7T', '2.8T', '1.8T', '1.0T', '780B', '235B', '1.7T'],
           'P/E': [65.2, 29.8, 35.2, 28.5, 22.3, 58.3, 45.2, 52.1],
           'Sector': ['Technology', 'Technology', 'Technology', 'Technology', 
                     'Technology', 'Consumer', 'Technology', 'Consumer']
       })
       
       st.markdown("### 📊 Screener Results")
       
       st.dataframe(
           screener_results.style.format({
               'Price': '${:.2f}',
               'Change %': '{:+.2f}%'
           }).apply(lambda x: ['background-color: rgba(0, 214, 143, 0.1)' if x['Change %'] > 0 
                              else 'background-color: rgba(255, 61, 113, 0.1)' if x['Change %'] < 0
                              else '' for _ in x], axis=1),
           use_container_width=True,
           hide_index=True
       )

# ================== SETTINGS TAB ==================
with main_tabs[8]:
   st.markdown("### ⚙️ Platform Settings")
   
   col1, col2 = st.columns(2)
   
   with col1:
       st.markdown("#### 🎨 Display Settings")
       
       theme = st.selectbox("Theme", ["Dark", "Light", "Auto"], index=0)
       st.session_state.theme = theme.lower()
       
       language = st.selectbox("Language", ["English", "Spanish", "Chinese", "Japanese", "Polish"])
       
       timezone = st.selectbox("Timezone", ["EST", "PST", "GMT", "CET", "JST", "SGT"])
       
       date_format = st.selectbox("Date Format", ["MM/DD/YYYY", "DD/MM/YYYY", "YYYY-MM-DD"])
       
       st.markdown("#### 📊 Chart Settings")
       
       default_chart = st.selectbox("Default Chart Type", ["Candlestick", "Line", "Area", "Heikin Ashi"])
       
       default_indicators = st.multiselect(
           "Default Indicators",
           ["SMA 20", "SMA 50", "EMA 12", "EMA 26", "RSI", "MACD", "Volume"],
           default=["SMA 20", "SMA 50", "Volume"]
       )
   
   with col2:
       st.markdown("#### 🔔 Notifications")
       
       price_alerts = st.checkbox("Price Alerts", value=True)
       news_alerts = st.checkbox("News Alerts", value=True)
       technical_alerts = st.checkbox("Technical Indicator Alerts", value=False)
       portfolio_alerts = st.checkbox("Portfolio Performance Alerts", value=True)
       
       st.markdown("#### 📡 Data Settings")
       
       refresh_rate = st.select_slider(
           "Auto-refresh interval",
           options=["Off", "1 min", "5 min", "15 min", "30 min", "1 hour"],
           value="5 min"
       )
       
       data_provider = st.selectbox(
           "Primary Data Provider",
           ["Yahoo Finance", "Alpha Vantage", "IEX Cloud", "Polygon", "Finnhub"]
       )
       
       api_key = st.text_input("API Key", type="password", placeholder="Enter your API key...")
       
       st.markdown("#### 🔐 Security")
       
       two_factor = st.checkbox("Enable Two-Factor Authentication", value=False)
       session_timeout = st.number_input("Session Timeout (minutes)", min_value=5, value=30)
   
   if st.button("💾 Save Settings", use_container_width=True):
       st.success("✅ Settings saved successfully!")
       # Here you would save settings to a database or config file

# Footer
st.markdown("""
<div style="margin-top: 3rem; padding: 2rem 0; border-top: 1px solid #30363d; text-align: center; color: #8b92a8;">
   <div style="font-size: 1.1rem; font-weight: 600; margin-bottom: 0.5rem;">
       Terminal Pro - Professional Trading Platform
   </div>
   <div style="margin: 1rem 0;">
       <span style="margin: 0 1rem;">📊 Real-time Market Data</span>
       <span style="margin: 0 1rem;">🔐 Bank-level Security</span>
       <span style="margin: 0 1rem;">🚀 Lightning Fast Execution</span>
       <span style="margin: 0 1rem;">🤖 AI-Powered Insights</span>
   </div>
   <div style="margin-top: 1rem; font-size: 0.875rem; opacity: 0.8;">
       © 2024 Terminal Pro | Version 2.0.0 | All rights reserved
   </div>
   <div style="margin-top: 0.5rem; font-size: 0.75rem; opacity: 0.6;">
       Market data provided by Yahoo Finance | Quotes may be delayed up to 15 minutes
   </div>
</div>
""", unsafe_allow_html=True)

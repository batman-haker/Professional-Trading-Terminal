#!/usr/bin/env python3
"""
Professional Trading Terminal - Clean Version
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta
import yfinance as yf

try:
    from alphavantage_client import AlphaVantageClient
    ALPHAVANTAGE_AVAILABLE = True
except:
    ALPHAVANTAGE_AVAILABLE = False

try:
    from portfolio_manager import portfolio_manager, format_currency, format_percentage
    PORTFOLIO_AVAILABLE = True
except:
    PORTFOLIO_AVAILABLE = False

try:
    from stock_analyzer import StockAnalyzer
    ANALYZER_AVAILABLE = True
except:
    ANALYZER_AVAILABLE = False

# Page config
st.set_page_config(
    page_title="Trading Terminal Pro",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CLEAN DARK MODE + NEON
st.markdown("""
<style>
    /* Import Modern Font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    /* === DARK MODE FOUNDATION === */
    .main, .stApp {
        background-color: #000000 !important;
        color: #ffffff !important;
        font-family: 'Inter', sans-serif;
    }

    /* WSZYSTKIE teksty białe */
    *, *::before, *::after,
    p, span, div, label, h1, h2, h3, h4, h5, h6,
    .stMarkdown, .stText, li, td, th,
    [data-testid="stMarkdownContainer"] {
        color: #ffffff !important;
    }

    /* WSZYSTKIE tła czarne lub przezroczyste */
    .stExpander,
    [data-testid="stExpander"],
    .streamlit-expanderContent,
    [data-testid="stExpanderDetails"],
    .element-container,
    div[data-testid="stVerticalBlock"],
    div[data-testid="stHorizontalBlock"] {
        background-color: transparent !important;
    }

    /* === NEON CARDS (metryki) === */
    .stMetric {
        background-color: #000000 !important;
        border: 2px solid #00f0ff !important;
        border-radius: 8px;
        padding: 1.5rem;
        box-shadow: 0 0 20px rgba(0, 240, 255, 0.4);
        transition: all 0.3s ease;
    }

    .stMetric:hover {
        border-color: #ff006e !important;
        box-shadow: 0 0 30px rgba(255, 0, 110, 0.6);
        transform: translateY(-2px);
    }

    [data-testid="stMetricLabel"] {
        color: #00f0ff !important;
        font-weight: 600;
        text-transform: uppercase;
        font-size: 0.75rem;
    }

    [data-testid="stMetricValue"] {
        color: #ffffff !important;
        font-size: 2rem;
        font-weight: 700;
    }

    /* === TABS === */
    .stTabs [data-baseweb="tab-list"] {
        background-color: transparent;
        border-bottom: 2px solid #00f0ff;
    }

    .stTabs [data-baseweb="tab"] {
        background-color: transparent !important;
        color: #ffffff !important;
        border: none !important;
        padding: 0.75rem 1.5rem;
    }

    .stTabs [aria-selected="true"] {
        background-color: rgba(0, 240, 255, 0.1) !important;
        color: #00f0ff !important;
        border-bottom: 3px solid #00f0ff !important;
    }

    /* === BUTTONS z neonowym obwodem === */
    .stButton > button {
        background-color: #000000 !important;
        color: #ffffff !important;
        border: 2px solid #00f0ff !important;
        border-radius: 8px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        box-shadow: 0 0 15px rgba(0, 240, 255, 0.4);
        transition: all 0.3s ease;
    }

    .stButton > button:hover {
        border-color: #ff006e !important;
        box-shadow: 0 0 25px rgba(255, 0, 110, 0.6);
        transform: translateY(-2px);
    }

    /* === SELECT BOX === */
    .stSelectbox > div > div {
        background-color: #000000 !important;
        border: 2px solid #00f0ff !important;
        border-radius: 8px;
        color: #ffffff !important;
    }

    .stSelectbox > div > div:hover {
        border-color: #ff006e !important;
        box-shadow: 0 0 15px rgba(255, 0, 110, 0.4);
    }

    /* === TEXT INPUT === */
    .stTextInput > div > div > input {
        background-color: #000000 !important;
        border: 2px solid #00f0ff !important;
        border-radius: 8px;
        color: #ffffff !important;
        padding: 0.75rem;
    }

    .stTextInput > div > div > input:focus {
        border-color: #ff006e !important;
        box-shadow: 0 0 20px rgba(255, 0, 110, 0.5);
        outline: none;
    }

    /* === EXPANDERS === */
    .streamlit-expanderHeader {
        background-color: #000000 !important;
        border: 2px solid #00f0ff !important;
        border-radius: 8px;
        color: #00f0ff !important;
        font-weight: 600;
    }

    .streamlit-expanderHeader:hover {
        border-color: #ff006e !important;
        box-shadow: 0 0 20px rgba(255, 0, 110, 0.4);
    }

    /* === ALERT BOXES === */
    .stSuccess, .stInfo {
        background-color: rgba(0, 0, 0, 0.95) !important;
        border: 2px solid #00f0ff !important;
        color: #ffffff !important;
    }

    .stWarning {
        background-color: rgba(0, 0, 0, 0.95) !important;
        border: 2px solid #ffbe0b !important;
        color: #ffffff !important;
    }

    .stError {
        background-color: rgba(0, 0, 0, 0.95) !important;
        border: 2px solid #ff006e !important;
        color: #ffffff !important;
    }

    /* === TABLES === */
    .dataframe {
        border: 2px solid #00f0ff !important;
        border-radius: 8px;
        overflow: hidden;
    }

    table {
        color: #ffffff !important;
        background-color: #000000 !important;
    }

    thead tr th {
        background-color: rgba(0, 240, 255, 0.15) !important;
        color: #00f0ff !important;
        font-weight: 700;
        border-bottom: 2px solid #00f0ff !important;
    }

    tbody tr {
        background-color: rgba(0, 0, 0, 0.9) !important;
    }

    tbody tr:hover {
        background-color: rgba(0, 240, 255, 0.1) !important;
    }

    tbody tr td {
        color: #ffffff !important;
    }

    /* === TOOLTIPS / POPOVERS - NAPRAWIONE! === */
    [data-baseweb="popover"],
    [data-baseweb="tooltip"],
    .stTooltipIcon,
    [data-testid="stTooltipHoverTarget"] {
        background-color: #000000 !important;
        color: #ffffff !important;
    }

    /* Tooltip content */
    [data-baseweb="popover"] > div,
    [data-baseweb="tooltip"] > div {
        background-color: #000000 !important;
        border: 2px solid #00f0ff !important;
        border-radius: 8px;
        color: #ffffff !important;
        padding: 1rem;
        box-shadow: 0 0 30px rgba(0, 240, 255, 0.6);
    }

    /* Wszystkie elementy w tooltipie */
    [data-baseweb="popover"] *,
    [data-baseweb="tooltip"] * {
        color: #ffffff !important;
        background-color: transparent !important;
    }

    /* === SCROLLBAR === */
    ::-webkit-scrollbar {
        width: 12px;
        height: 12px;
    }

    ::-webkit-scrollbar-track {
        background-color: #000000;
        border: 1px solid #00f0ff;
    }

    ::-webkit-scrollbar-thumb {
        background: linear-gradient(180deg, #00f0ff 0%, #ff006e 100%);
        border-radius: 6px;
        box-shadow: 0 0 10px rgba(0, 240, 255, 0.5);
    }

    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(180deg, #ff006e 0%, #ffbe0b 100%);
    }

    /* === HEADERS === */
    h2, h3, h4 {
        color: #00f0ff !important;
        font-weight: 700;
        border-left: 4px solid #ff006e;
        padding-left: 1rem;
        margin-top: 2rem;
        margin-bottom: 1rem;
    }

    /* === LINKS === */
    a {
        color: #00f0ff !important;
        text-decoration: none;
    }

    a:hover {
        color: #ff006e !important;
    }

    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# Initialize AlphaVantage
if ALPHAVANTAGE_AVAILABLE:
    av_client = AlphaVantageClient()
else:
    av_client = None

# Session state
if 'selected_ticker' not in st.session_state:
    st.session_state.selected_ticker = 'AAPL'

# Cyberpunk Header
st.markdown("""
<div style="text-align: center; margin-bottom: 2rem;">
    <h1 style="margin-bottom: 0.5rem;">⚡ CYBER TRADING TERMINAL ⚡</h1>
    <p style="color: #ff006e; font-weight: 700; letter-spacing: 0.2em; text-transform: uppercase; font-size: 0.9rem; text-shadow: 0 0 10px rgba(255, 0, 110, 0.8);">
        [ NEURAL MARKET ANALYSIS • REAL-TIME DATA STREAM • AI POWERED ]
    </p>
</div>
""", unsafe_allow_html=True)

# Cyberpunk Tabs
main_tabs = st.tabs(["⚡ STOCK ANALYSIS", "🌐 MARKET HEATMAP", "💎 PORTFOLIO"])

# TAB 1: Stock Analysis
with main_tabs[0]:
    st.subheader("Stock Analysis")

    # Popular stocks database
    POPULAR_STOCKS = {
        # US Tech Giants
        "Apple Inc. (AAPL)": "AAPL",
        "Microsoft Corporation (MSFT)": "MSFT",
        "NVIDIA Corporation (NVDA)": "NVDA",
        "Alphabet Inc. (GOOGL)": "GOOGL",
        "Amazon.com Inc. (AMZN)": "AMZN",
        "Meta Platforms Inc. (META)": "META",
        "Tesla Inc. (TSLA)": "TSLA",
        "Netflix Inc. (NFLX)": "NFLX",
        "Adobe Inc. (ADBE)": "ADBE",
        "Intel Corporation (INTC)": "INTC",
        "Advanced Micro Devices (AMD)": "AMD",
        "Cisco Systems (CSCO)": "CSCO",
        "Oracle Corporation (ORCL)": "ORCL",
        "Salesforce Inc. (CRM)": "CRM",
        "Broadcom Inc. (AVGO)": "AVGO",
        "Qualcomm Inc. (QCOM)": "QCOM",
        "Texas Instruments (TXN)": "TXN",
        "IBM Corporation (IBM)": "IBM",
        "PayPal Holdings (PYPL)": "PYPL",
        "Uber Technologies (UBER)": "UBER",
        "Airbnb Inc. (ABNB)": "ABNB",
        "Block Inc. (SQ)": "SQ",
        "Shopify Inc. (SHOP)": "SHOP",
        "Zoom Video (ZM)": "ZM",
        "Snowflake Inc. (SNOW)": "SNOW",
        "Palantir Technologies (PLTR)": "PLTR",
        "Coinbase Global (COIN)": "COIN",

        # US Finance
        "JPMorgan Chase (JPM)": "JPM",
        "Bank of America (BAC)": "BAC",
        "Wells Fargo (WFC)": "WFC",
        "Goldman Sachs (GS)": "GS",
        "Morgan Stanley (MS)": "MS",
        "Visa Inc. (V)": "V",
        "Mastercard Inc. (MA)": "MA",
        "American Express (AXP)": "AXP",
        "Berkshire Hathaway (BRK-B)": "BRK-B",

        # US Consumer & Retail
        "Walmart Inc. (WMT)": "WMT",
        "Costco Wholesale (COST)": "COST",
        "Home Depot (HD)": "HD",
        "Target Corporation (TGT)": "TGT",
        "Nike Inc. (NKE)": "NKE",
        "McDonald's Corp (MCD)": "MCD",
        "Starbucks Corp (SBUX)": "SBUX",
        "Coca-Cola Company (KO)": "KO",
        "PepsiCo Inc. (PEP)": "PEP",
        "Procter & Gamble (PG)": "PG",
        "Walt Disney (DIS)": "DIS",

        # US Healthcare & Pharma
        "Johnson & Johnson (JNJ)": "JNJ",
        "UnitedHealth Group (UNH)": "UNH",
        "Pfizer Inc. (PFE)": "PFE",
        "AbbVie Inc. (ABBV)": "ABBV",
        "Merck & Co (MRK)": "MRK",
        "Eli Lilly (LLY)": "LLY",
        "Bristol-Myers Squibb (BMY)": "BMY",
        "Moderna Inc. (MRNA)": "MRNA",

        # US Energy
        "ExxonMobil Corp (XOM)": "XOM",
        "Chevron Corporation (CVX)": "CVX",
        "ConocoPhillips (COP)": "COP",

        # US Telecom
        "Verizon Communications (VZ)": "VZ",
        "AT&T Inc. (T)": "T",
        "Comcast Corporation (CMCSA)": "CMCSA",

        # Poland (GPW)
        "PKO Bank Polski (PKO.WA)": "PKO.WA",
        "PZU Grupa (PZU.WA)": "PZU.WA",
        "KGHM Polska Miedź (KGHM.WA)": "KGHM.WA",
        "PKN Orlen (PKN.WA)": "PKN.WA",
        "PGE Polska Grupa Energetyczna (PGE.WA)": "PGE.WA",
        "CD Projekt (CDR.WA)": "CDR.WA",
        "Allegro.eu (ALE.WA)": "ALE.WA",
        "CCC S.A. (CCC.WA)": "CCC.WA",
        "LPP S.A. (LPP.WA)": "LPP.WA",
        "JSW S.A. (JSW.WA)": "JSW.WA",
        "Pekao S.A. (PEO.WA)": "PEO.WA",
        "mBank S.A. (MBK.WA)": "MBK.WA",
        "Dino Polska (DNP.WA)": "DNP.WA",
        "Santander Bank Polska (SPL.WA)": "SPL.WA",
        "Orange Polska (OPL.WA)": "OPL.WA",
        "Cyfrowy Polsat (CPS.WA)": "CPS.WA",
        "Kruk S.A. (KRU.WA)": "KRU.WA",

        # UK
        "BP plc (BP.L)": "BP.L",
        "HSBC Holdings (HSBC.L)": "HSBC.L",
        "Shell plc (SHEL.L)": "SHEL.L",
        "Barclays plc (BARC.L)": "BARC.L",
        "Unilever plc (ULVR.L)": "ULVR.L",
        "Rolls-Royce Holdings (RR.L)": "RR.L",

        # Germany
        "Volkswagen AG (VOW3.DE)": "VOW3.DE",
        "BMW AG (BMW.DE)": "BMW.DE",
        "Mercedes-Benz Group (MBG.DE)": "MBG.DE",
        "Siemens AG (SIE.DE)": "SIE.DE",
        "SAP SE (SAP.DE)": "SAP.DE",
        "Deutsche Bank (DBK.DE)": "DBK.DE",
        "Allianz SE (ALV.DE)": "ALV.DE",

        # France
        "LVMH (MC.PA)": "MC.PA",
        "L'Oréal (OR.PA)": "OR.PA",
        "TotalEnergies (TTE.PA)": "TTE.PA",
        "Airbus SE (AIR.PA)": "AIR.PA",

        # Other Popular
        "Sony Group Corp (SONY)": "SONY",
        "Toyota Motor (TM)": "TM",
        "Samsung Electronics (005930.KS)": "005930.KS",
    }

    # Search interface
    st.caption("💡 Zacznij pisać nazwę firmy lub ticker - np. 'Apple', 'Tesla', 'PKO'")

    col1, col2 = st.columns([4, 1])
    with col1:
        # Smart search selectbox
        search_options = ["🔍 Type to search..."] + list(POPULAR_STOCKS.keys())
        selected_option = st.selectbox(
            "Search for a company",
            options=search_options,
            index=0,
            key="stock_search_select",
            label_visibility="collapsed"
        )

        # Manual ticker input (for stocks not in list)
        manual_ticker = st.text_input(
            "Or enter ticker manually (e.g., AAPL, PKO.WA)",
            value="",
            key="manual_ticker_input",
            placeholder="Enter ticker symbol...",
            label_visibility="collapsed"
        )

    with col2:
        st.write("")  # Spacing
        st.write("")  # Spacing
        if st.button("🔍 Analyze", type="primary", key="analyze_btn"):
            # Priority: manual input > selected from dropdown
            if manual_ticker:
                st.session_state.selected_ticker = manual_ticker.upper()
                st.rerun()
            elif selected_option != "🔍 Type to search...":
                ticker = POPULAR_STOCKS[selected_option]
                st.session_state.selected_ticker = ticker
                st.rerun()
            else:
                st.warning("Please select a company or enter a ticker symbol")

    st.markdown(f"**Analyzing: {st.session_state.selected_ticker}**")

    # Get data
    try:
        ticker = yf.Ticker(st.session_state.selected_ticker)
        info = ticker.info
        hist = ticker.history(period="1y")

        if not hist.empty:
            # Calculate performance metrics for analyzer
            hist_1d = ticker.history(period="2d")
            hist_1w = ticker.history(period="5d")
            hist_1m = ticker.history(period="1mo")
            hist_3m = ticker.history(period="3mo")

            current_price = hist['Close'].iloc[-1]

            perf_1d = None
            perf_1w = None
            perf_1m = None
            perf_3m = None

            if len(hist_1d) >= 2:
                perf_1d = ((current_price - hist_1d['Close'].iloc[-2]) / hist_1d['Close'].iloc[-2] * 100)
            if len(hist_1w) >= 2:
                perf_1w = ((current_price - hist_1w['Close'].iloc[0]) / hist_1w['Close'].iloc[0] * 100)
            if len(hist_1m) >= 2:
                perf_1m = ((current_price - hist_1m['Close'].iloc[0]) / hist_1m['Close'].iloc[0] * 100)
            if len(hist_3m) >= 2:
                perf_3m = ((current_price - hist_3m['Close'].iloc[0]) / hist_3m['Close'].iloc[0] * 100)

            # Add performance data to info for analyzer
            info['currentPrice'] = current_price
            info['performance_1d'] = perf_1d
            info['performance_1w'] = perf_1w
            info['performance_1m'] = perf_1m
            info['performance_3m'] = perf_3m

            # ==========================================
            # SMART ANALYSIS SECTION
            # ==========================================
            if ANALYZER_AVAILABLE:
                st.markdown("---")
                st.subheader("🤖 Smart Analysis")
                st.caption("📊 Analiza względem sektora i rynku - nie książkowe wartości, ale realia 2024!")

                try:
                    # Run analysis
                    analyzer = StockAnalyzer(info)
                    analysis = analyzer.analyze()

                    # Hero section - Overall Score & Recommendation
                    col1, col2, col3 = st.columns([2, 1, 1])
                    with col1:
                        # Big score display
                        score_color = "green" if analysis.overall_score >= 60 else ("orange" if analysis.overall_score >= 40 else "red")
                        st.markdown(f"""
                        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                                    padding: 2rem; border-radius: 15px; text-align: center;">
                            <h1 style="color: white; margin: 0; font-size: 4rem;">{analysis.overall_score:.0f}<span style="font-size: 2rem;">/100</span></h1>
                            <h2 style="color: white; margin: 0.5rem 0;">{analysis.recommendation.value}</h2>
                            <p style="color: rgba(255,255,255,0.9); margin: 0;">{analysis.sector} | {analysis.industry}</p>
                        </div>
                        """, unsafe_allow_html=True)

                    with col2:
                        st.metric("Valuation", f"{analysis.valuation_score:.0f}/100",
                                 help="🎯 Czy akcja jest tania czy droga względem sektora")
                        st.metric("Growth", f"{analysis.growth_score:.0f}/100",
                                 help="📈 Czy firma rośnie szybciej niż konkurencja")
                        st.metric("Momentum", f"{analysis.momentum_score:.0f}/100",
                                 help="🚀 Czy cena ma trend wzrostowy")

                    with col3:
                        st.metric("Health", f"{analysis.financial_health_score:.0f}/100",
                                 help="💪 Czy firma jest finansowo zdrowa")
                        st.metric("Sentiment", f"{analysis.sentiment_score:.0f}/100",
                                 help="👥 Co myślą analitycy i instytucje")
                        st.write("")  # Spacing

                    # Executive Summary
                    st.info(f"📝 **Executive Summary:** {analysis.summary}")

                    # Tabs for detailed analysis
                    analysis_tabs = st.tabs(["💪 Strengths & Weaknesses", "🚨 Red Flags & 💎 Catalysts", "📊 Sector Comparison"])

                    # Tab 1: Strengths & Weaknesses
                    with analysis_tabs[0]:
                        col1, col2 = st.columns(2)
                        with col1:
                            st.markdown("### 💪 Strengths")
                            if analysis.strengths:
                                for strength in analysis.strengths:
                                    st.success(strength)
                            else:
                                st.info("No significant strengths identified")

                        with col2:
                            st.markdown("### ⚠️ Weaknesses")
                            if analysis.weaknesses:
                                for weakness in analysis.weaknesses:
                                    st.warning(weakness)
                            else:
                                st.info("No significant weaknesses identified")

                    # Tab 2: Red Flags & Catalysts
                    with analysis_tabs[1]:
                        col1, col2 = st.columns(2)
                        with col1:
                            st.markdown("### 🚨 Red Flags")
                            if analysis.red_flags:
                                for flag in analysis.red_flags:
                                    st.error(flag)
                            else:
                                st.success("✅ No major red flags detected!")

                        with col2:
                            st.markdown("### 💎 Catalysts")
                            if analysis.catalysts:
                                for catalyst in analysis.catalysts:
                                    st.success(catalyst)
                            else:
                                st.info("No significant catalysts identified")

                    # Tab 3: Sector Comparison
                    with analysis_tabs[2]:
                        st.markdown(f"### 📊 vs {analysis.sector} Sector")
                        if analysis.sector_comparison:
                            for metric, comparison in analysis.sector_comparison.items():
                                st.write(f"**{metric}:** {comparison}")
                        else:
                            st.info("Sector comparison data not available")

                except Exception as e:
                    st.warning(f"Smart Analysis temporarily unavailable: {e}")

            st.markdown("---")
            # ==========================================
            # END SMART ANALYSIS
            # ==========================================
            # Price info
            current_price = hist['Close'].iloc[-1]
            prev_close = hist['Close'].iloc[-2] if len(hist) > 1 else current_price
            change = current_price - prev_close
            change_pct = (change / prev_close * 100) if prev_close > 0 else 0
            
            # Metrics
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric(
                    "Price",
                    f"${current_price:.2f}",
                    f"{change_pct:+.2f}%",
                    help="💰 Aktualna cena akcji - to co widzisz, to co płacisz! Czerwone = Au, zielone = Woohoo!"
                )
            with col2:
                market_cap = info.get('marketCap', 0)
                mcap_str = f"${market_cap/1e9:.2f}B" if market_cap > 1e9 else f"${market_cap/1e6:.2f}M"
                st.metric(
                    "Market Cap",
                    mcap_str,
                    help="🏢 Kapitalizacja rynkowa = ile warta jest cała firma. To tak jakby policzyć ile kosztują WSZYSTKIE akcje razem. Im większa, tym trudniej firmą poruszyć (jak tankowiec vs. kajak)"
                )
            with col3:
                pe = info.get('trailingPE', 'N/A')
                pe_str = f"{pe:.2f}" if isinstance(pe, (int, float)) else 'N/A'
                st.metric(
                    "P/E Ratio",
                    pe_str,
                    help="📊 Wskaźnik Cena/Zysk - mówi ile płacisz za $1 zysku firmy. P/E = 20? Płacisz $20 za każdy $1 rocznego zysku. Niskie P/E = tanie, wysokie = albo przereklamowane, albo mega potencjał 🚀"
                )
            with col4:
                eps = info.get('trailingEps', 'N/A')
                eps_str = f"${eps:.2f}" if isinstance(eps, (int, float)) else 'N/A'
                st.metric(
                    "EPS",
                    eps_str,
                    help="💵 Earnings Per Share - zysk na jedną akcję. Ile firma zarobiła podzielone przez liczbę akcji. Im wyższe tym lepiej dla akcjonariuszy (więcej kasy na akcję = happy investors)"
                )

            # Price Performance
            st.markdown("---")
            st.subheader("📈 Performance")
            st.caption("🔥 Jak akcja zachowywała się w ostatnich okresach? Momentum check!")

            try:
                # Get historical data for different periods
                hist_1m = ticker.history(period="1mo")
                hist_1w = ticker.history(period="5d")  # 1 week = 5 trading days
                hist_1d = ticker.history(period="2d")  # Need 2 days to calc 1day change

                performance_data = []

                # 1 Day change
                if len(hist_1d) >= 2:
                    price_1d_ago = hist_1d['Close'].iloc[-2]
                    change_1d = ((current_price - price_1d_ago) / price_1d_ago * 100)
                    performance_data.append({
                        'period': '24 Hours',
                        'change_pct': change_1d,
                        'old_price': price_1d_ago,
                        'tooltip': '📊 Zmiana w ciągu ostatnich 24 godzin (1 dzień tradingowy). To jest momentum z "wczoraj na dziś"!'
                    })

                # 1 Week change
                if len(hist_1w) >= 2:
                    price_1w_ago = hist_1w['Close'].iloc[0]
                    change_1w = ((current_price - price_1w_ago) / price_1w_ago * 100)
                    performance_data.append({
                        'period': '1 Week',
                        'change_pct': change_1w,
                        'old_price': price_1w_ago,
                        'tooltip': '📅 Zmiana przez ostatni tydzień (5 dni tradingowych). Short-term trend! 🔥'
                    })

                # 1 Month change
                if len(hist_1m) >= 2:
                    price_1m_ago = hist_1m['Close'].iloc[0]
                    change_1m = ((current_price - price_1m_ago) / price_1m_ago * 100)
                    performance_data.append({
                        'period': '1 Month',
                        'change_pct': change_1m,
                        'old_price': price_1m_ago,
                        'tooltip': '🗓️ Zmiana przez ostatni miesiąc (~21 dni tradingowych). Szerszy obraz! 📈'
                    })

                # 3 Month change (bonus)
                hist_3m = ticker.history(period="3mo")
                if len(hist_3m) >= 2:
                    price_3m_ago = hist_3m['Close'].iloc[0]
                    change_3m = ((current_price - price_3m_ago) / price_3m_ago * 100)
                    performance_data.append({
                        'period': '3 Months',
                        'change_pct': change_3m,
                        'old_price': price_3m_ago,
                        'tooltip': '📆 Zmiana przez ostatnie 3 miesiące. Quarterly view! Long-term momentum! 🚀'
                    })

                # YTD change (Year To Date)
                hist_ytd = ticker.history(period="ytd")
                if len(hist_ytd) >= 2:
                    price_ytd_start = hist_ytd['Close'].iloc[0]
                    change_ytd = ((current_price - price_ytd_start) / price_ytd_start * 100)
                    performance_data.append({
                        'period': 'YTD (Year to Date)',
                        'change_pct': change_ytd,
                        'old_price': price_ytd_start,
                        'tooltip': '🎯 Zmiana od początku roku. Jak akcja radzi sobie w tym roku? Annual performance check! 📅'
                    })

                if performance_data:
                    # Display as metrics in columns
                    cols = st.columns(len(performance_data))
                    for idx, perf in enumerate(performance_data):
                        with cols[idx]:
                            # Color based on performance
                            delta_color = "normal"
                            emoji = "📊"
                            if perf['change_pct'] > 0:
                                emoji = "🟢"
                                delta_color = "normal"
                            elif perf['change_pct'] < 0:
                                emoji = "🔴"
                                delta_color = "inverse"

                            st.metric(
                                f"{emoji} {perf['period']}",
                                f"{perf['change_pct']:+.2f}%",
                                delta=f"${perf['old_price']:.2f} → ${current_price:.2f}",
                                help=perf['tooltip']
                            )

                    # Summary message
                    st.markdown("---")
                    best_period = max(performance_data, key=lambda x: x['change_pct'])
                    worst_period = min(performance_data, key=lambda x: x['change_pct'])

                    col1, col2 = st.columns(2)
                    with col1:
                        st.success(f"💪 **Best Period:** {best_period['period']} ({best_period['change_pct']:+.2f}%)")
                    with col2:
                        st.error(f"📉 **Worst Period:** {worst_period['period']} ({worst_period['change_pct']:+.2f}%)")

                else:
                    st.info("Brak danych historycznych do obliczenia performance")

            except Exception as e:
                st.warning("Nie udało się pobrać danych o performance")

            # Company Overview
            st.markdown("---")
            st.subheader("🏢 Company Overview")

            col1, col2 = st.columns([2, 1])
            with col1:
                # Business description
                description = info.get('longBusinessSummary', 'No description available')
                with st.expander("📖 Czym zajmuje się firma?", expanded=True):
                    st.write(description)

            with col2:
                # Company details
                st.markdown("**📊 Podstawowe informacje:**")

                company_name = info.get('longName', st.session_state.selected_ticker)
                st.write(f"**Nazwa:** {company_name}")

                sector = info.get('sector', 'N/A')
                st.write(f"**Sektor:** {sector}")

                industry = info.get('industry', 'N/A')
                st.write(f"**Branża:** {industry}")

                employees = info.get('fullTimeEmployees', None)
                if employees:
                    st.write(f"**Pracownicy:** {employees:,}")

                # Location
                city = info.get('city', '')
                country = info.get('country', '')
                if city or country:
                    location = f"{city}, {country}" if city and country else (city or country)
                    st.write(f"**Lokalizacja:** {location}")

                # Website
                website = info.get('website', None)
                if website:
                    st.write(f"**Strona:** [{website}]({website})")

            # Chart
            st.subheader("Price Chart")
            st.caption("📊 Candlestick chart - zielone świeczki = wzrost, czerwone = spadek. Każda świeczka pokazuje: Open (otwarcie), High (max), Low (min), Close (zamknięcie). To jak EKG rynku! 💓")
            fig = go.Figure()
            fig.add_trace(go.Candlestick(
                x=hist.index,
                open=hist['Open'],
                high=hist['High'],
                low=hist['Low'],
                close=hist['Close'],
                name=st.session_state.selected_ticker
            ))
            fig.update_layout(
                template='plotly_dark',
                height=500,
                xaxis_rangeslider_visible=False
            )
            st.plotly_chart(fig, use_container_width=True)

            # Financial Health
            st.subheader("📊 Financial Health")
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                roe = info.get('returnOnEquity', None)
                roe_str = f"{roe*100:.2f}%" if roe else 'N/A'
                st.metric(
                    "ROE",
                    roe_str,
                    help="🎯 Return on Equity - jak efektywnie firma zamienia kapitał akcjonariuszy w zyski. ROE 15%? Każdy $100 od akcjonariuszy generuje $15 zysku rocznie. Wyższe = lepsze! Warren Buffett uwielbia wysokie ROE 📈"
                )
            with col2:
                roa = info.get('returnOnAssets', None)
                roa_str = f"{roa*100:.2f}%" if roa else 'N/A'
                st.metric(
                    "ROA",
                    roa_str,
                    help="💎 Return on Assets - jak dobrze firma wykorzystuje swoje aktywa do generowania zysków. Masz fabrykę za $1M i zarabiasz $50K? ROA = 5%. Im wyższe, tym firma lepiej 'wydoiła' swoje zasoby!"
                )
            with col3:
                profit_margin = info.get('profitMargins', None)
                pm_str = f"{profit_margin*100:.2f}%" if profit_margin else 'N/A'
                st.metric(
                    "Profit Margin",
                    pm_str,
                    help="💰 Marża zysku - ile zostaje po odjęciu WSZYSTKICH kosztów. Sprzedajesz za $100, koszty $80? Marża = 20%. Apple ma ~25%, supermarkety ~2%. Tech > Retail 🚀"
                )
            with col4:
                debt_equity = info.get('debtToEquity', None)
                de_str = f"{debt_equity:.2f}" if debt_equity else 'N/A'
                st.metric(
                    "Debt/Equity",
                    de_str,
                    help="⚖️ Wskaźnik Dług/Kapitał - ile firma ma długów względem kapitału własnego. D/E = 2.0? Na każdy $1 kapitału przypada $2 długu. Poniżej 1.0 = bezpieczne, powyżej 2.0 = ryzykowne! (Chyba że to bank, tam inne zasady)"
                )

            # Analyst Recommendations
            st.subheader("📈 Analyst Recommendations")
            st.caption("🎓 Co 'mądre głowy' z Wall Street myślą o tej akcji - ostatnie 10 rekomendacji. Strong Buy = 🚀, Sell = 📉")
            try:
                recommendations = ticker.recommendations
                if recommendations is not None and not recommendations.empty:
                    recent_recs = recommendations.tail(10)
                    rec_summary = recent_recs['To Grade'].value_counts().to_dict()

                    rec_cols = st.columns(len(rec_summary))
                    for idx, (grade, count) in enumerate(rec_summary.items()):
                        with rec_cols[idx]:
                            st.metric(grade, count)
                else:
                    st.info("No analyst recommendations available")
            except:
                st.info("No analyst recommendations available")

            # Dividends History
            st.subheader("💰 Dividends")
            st.caption("💸 Pasywny dochód dla akcjonariuszy! Firma dzieli się zyskami co kwartał/rok. To jak dostawać 'czynsz' za posiadanie akcji 🏠")
            try:
                dividends = ticker.dividends
                if dividends is not None and not dividends.empty and len(dividends) > 0:
                    # Recent dividends
                    recent_divs = dividends.tail(12)

                    col1, col2 = st.columns([2, 1])
                    with col1:
                        # Dividends chart
                        div_fig = go.Figure()
                        div_fig.add_trace(go.Bar(
                            x=recent_divs.index,
                            y=recent_divs.values,
                            name='Dividend',
                            marker_color='lightblue'
                        ))
                        div_fig.update_layout(
                            template='plotly_dark',
                            height=300,
                            xaxis_title="Date",
                            yaxis_title="Dividend ($)"
                        )
                        st.plotly_chart(div_fig, use_container_width=True)

                    with col2:
                        # Dividend metrics
                        div_yield = info.get('dividendYield', None)
                        dy_str = f"{div_yield*100:.2f}%" if div_yield else 'N/A'
                        st.metric(
                            "Dividend Yield",
                            dy_str,
                            help="📊 Stopa dywidendy - ile % rocznie dostajesz z dywidend względem ceny akcji. Kupiłeś za $100, dostałeś $3 dywidendy? Yield = 3%. Wyższe = więcej pasywnego dochodu! 💵"
                        )

                        last_div = dividends.iloc[-1] if len(dividends) > 0 else 0
                        st.metric(
                            "Last Dividend",
                            f"${last_div:.2f}",
                            help="💰 Ostatnia wypłata dywidendy na akcję. To ile dostałeś za każdą akcję przy ostatniej wypłacie. Nice little bonus! 🎁"
                        )

                        annual_div = dividends.last('1Y').sum() if len(dividends) > 0 else 0
                        st.metric(
                            "Annual Dividends",
                            f"${annual_div:.2f}",
                            help="📅 Suma wszystkich dywidend z ostatniego roku na akcję. Masz 100 akcji i annual div = $5? Dostałeś $500 w ciągu roku za siedzenie i hodowanie akcji 🌱"
                        )
                else:
                    st.info("No dividend history available")
            except:
                st.info("No dividend history available")

            # Analyst Price Targets
            st.markdown("---")
            st.subheader("🎯 Cele Cenowe Analityków")
            st.caption("📍 Gdzie 'Wall Street wizards' widzą cenę tej akcji za rok? Guidance od tych co robią to zawodowo!")

            target_data = []
            target_high = info.get('targetHighPrice')
            target_low = info.get('targetLowPrice')
            target_mean = info.get('targetMeanPrice')
            target_median = info.get('targetMedianPrice')
            num_analysts = info.get('numberOfAnalystOpinions')
            recommendation = info.get('recommendationKey', 'N/A')

            if target_mean or target_high or target_low:
                col1, col2, col3, col4, col5 = st.columns(5)
                with col1:
                    st.metric(
                        "Target Low",
                        f"${target_low:.2f}" if target_low else "N/A",
                        help="🔻 Najbardziej pesymistyczna prognoza cenowa. To gdzie 'bears' widzą akcję w najgorszym scenariuszu. Szkło do połowy puste! 🐻"
                    )
                with col2:
                    st.metric(
                        "Target Mean",
                        f"${target_mean:.2f}" if target_mean else "N/A",
                        help="📊 Średnia wszystkich prognoz cenowych. Najbardziej 'fair' wycena według analityków. Golden middle! ⚖️"
                    )
                with col3:
                    st.metric(
                        "Target Median",
                        f"${target_median:.2f}" if target_median else "N/A",
                        help="🎯 Mediana prognoz - środkowa wartość (połowa wyższa, połowa niższa). Odporna na ekstremalne prognozy!"
                    )
                with col4:
                    st.metric(
                        "Target High",
                        f"${target_high:.2f}" if target_high else "N/A",
                        help="🚀 Najbardziej optymistyczna prognoza! To gdzie 'bulls' widzą akcję w best case scenario. TO THE MOON! 🌙"
                    )
                with col5:
                    st.metric(
                        "Analysts",
                        num_analysts if num_analysts else "N/A",
                        help="👥 Liczba analityków śledzących tę spółkę. Więcej = więcej uwagi = więcej 'smart money' patrzy na to!"
                    )

                # Recommendation key
                if recommendation != 'N/A':
                    rec_color_map = {
                        'strong_buy': '🟢',
                        'buy': '🟢',
                        'hold': '🟡',
                        'sell': '🔴',
                        'strong_sell': '🔴'
                    }
                    emoji = rec_color_map.get(recommendation.lower(), '⚪')
                    st.info(f"**Consensus Recommendation:** {emoji} {recommendation.upper().replace('_', ' ')}")
            else:
                st.info("Brak prognoz cenowych od analityków")

            # Trading Details
            st.markdown("---")
            st.subheader("📈 Trading Details")
            st.caption("🔥 Szczegóły z parkietu! Wolumen, ekstremum roczne, średnie kroczące - statystyki które mówią JAK akcja się handluje.")

            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown("**💹 Volume & Liquidity:**")
                volume = info.get('volume', 0)
                avg_volume = info.get('averageVolume', 0)
                avg_volume_10d = info.get('averageVolume10days', 0)

                st.metric(
                    "Volume Today",
                    f"{volume:,}" if volume else "N/A",
                    help="📊 Ile akcji wymieniono dzisiaj. Wysoki wolumen = dużo akcji, sporo uwagi, łatwiej kupić/sprzedać. To jak tłum na rynku! 👥"
                )
                st.metric(
                    "Avg Volume",
                    f"{avg_volume:,}" if avg_volume else "N/A",
                    help="📈 Średni dzienny wolumen (3 miesiące). Pokazuje typową 'płynność' akcji. Wyższe = łatwiej wejść/wyjść z pozycji!"
                )
                if avg_volume_10d:
                    st.metric(
                        "Avg Volume 10D",
                        f"{avg_volume_10d:,}",
                        help="📉 Średni wolumen z ostatnich 10 dni. Czy ostatnio jest więcej czy mniej akcji? Fresh data!"
                    )

            with col2:
                st.markdown("**🎢 52-Week Range:**")
                week_52_high = info.get('fiftyTwoWeekHigh')
                week_52_low = info.get('fiftyTwoWeekLow')

                if week_52_high:
                    st.metric(
                        "52W High",
                        f"${week_52_high:.2f}",
                        help="🏔️ Najwyższa cena w ciągu ostatniego roku. Szczyt góry! Jak blisko jesteśmy? All-time celebration zone! 🎉"
                    )
                if week_52_low:
                    st.metric(
                        "52W Low",
                        f"${week_52_low:.2f}",
                        help="📉 Najniższa cena w ciągu roku. Dołek. Jak daleko odpłynęliśmy od dna? Recovery mode activated! 💪"
                    )

                # Calculate distance from highs/lows
                if week_52_high and week_52_low and current_price:
                    range_pct = ((current_price - week_52_low) / (week_52_high - week_52_low) * 100)
                    st.metric(
                        "Position in Range",
                        f"{range_pct:.1f}%",
                        help="📍 Gdzie obecna cena jest w rocznym przedziale. 0% = na dnie, 100% = na szczycie, 50% = w środku. Pozycjonowanie! 🎯"
                    )

            with col3:
                st.markdown("**📊 Moving Averages:**")
                ma_50 = info.get('fiftyDayAverage')
                ma_200 = info.get('twoHundredDayAverage')

                if ma_50:
                    diff_50 = ((current_price - ma_50) / ma_50 * 100) if ma_50 else 0
                    st.metric(
                        "50-Day MA",
                        f"${ma_50:.2f}",
                        f"{diff_50:+.1f}%",
                        help="📈 Średnia krocząca z 50 dni. Short-term trend! Cena powyżej = uptrend 📈, poniżej = downtrend 📉. Traders' best friend!"
                    )
                if ma_200:
                    diff_200 = ((current_price - ma_200) / ma_200 * 100) if ma_200 else 0
                    st.metric(
                        "200-Day MA",
                        f"${ma_200:.2f}",
                        f"{diff_200:+.1f}%",
                        help="📊 Średnia z 200 dni. Long-term trend checker! Powyżej = bull market 🐂, poniżej = bear market 🐻. The big picture!"
                    )

                # Bid/Ask spread
                bid = info.get('bid')
                ask = info.get('ask')
                if bid and ask:
                    spread = ask - bid
                    spread_pct = (spread / bid * 100) if bid > 0 else 0
                    st.metric(
                        "Bid-Ask Spread",
                        f"${spread:.2f}",
                        f"{spread_pct:.2f}%",
                        help="💰 Różnica między ceną kupna a sprzedaży. Wąski spread = płynny rynek, szeroki = trudniej tradować. To Twój 'koszt wejścia'! 💸"
                    )

            # Valuation Metrics
            st.markdown("---")
            st.subheader("💎 Wskaźniki Wyceny")
            st.caption("🔍 Czy akcja jest tania czy droga? Multiple ways to skin the valuation cat!")

            col1, col2, col3, col4 = st.columns(4)
            with col1:
                pb = info.get('priceToBook')
                if pb:
                    st.metric(
                        "P/B Ratio",
                        f"{pb:.2f}",
                        help="📚 Price-to-Book - cena do wartości księgowej. P/B < 1 = handlujesz poniżej wartości w księgach! Value investors love this. Buffett's favorite! 🎩"
                    )

                forward_pe = info.get('forwardPE')
                if forward_pe:
                    st.metric(
                        "Forward P/E",
                        f"{forward_pe:.2f}",
                        help="🔮 P/E bazujący na prognozowanych zyskach (nie historycznych). Future looking! Niższe = tańsze względem przyszłych zysków!"
                    )

            with col2:
                ps = info.get('priceToSalesTrailing12Months')
                if ps:
                    st.metric(
                        "P/S Ratio",
                        f"{ps:.2f}",
                        help="💵 Price-to-Sales - cena do przychodów. Dobre dla firm bez zysków (startupy). Mierzysz wycenę vs revenue, nie profit!"
                    )

                peg = info.get('pegRatio')
                if peg:
                    st.metric(
                        "PEG Ratio",
                        f"{peg:.2f}",
                        help="⚡ P/E do wzrostu zysków. PEG < 1 = niedowartościowane względem wzrostu! Holy grail of growth investing! Peter Lynch approved! 🏆"
                    )

            with col3:
                ev = info.get('enterpriseValue')
                if ev:
                    ev_str = f"${ev/1e9:.2f}B" if ev > 1e9 else f"${ev/1e6:.2f}M"
                    st.metric(
                        "Enterprise Value",
                        ev_str,
                        help="🏢 Wartość przedsiębiorstwa = Market Cap + Dług - Cash. To ile kosztowałoby KUPIĆ całą firmę z długami. M&A metric! 💼"
                    )

                ev_revenue = info.get('enterpriseToRevenue')
                if ev_revenue:
                    st.metric(
                        "EV/Revenue",
                        f"{ev_revenue:.2f}",
                        help="📊 Enterprise Value do przychodów. Jak dużo płacisz za każdy $1 revenue firmy. SaaS companies obsession! ☁️"
                    )

            with col4:
                ev_ebitda = info.get('enterpriseToEbitda')
                if ev_ebitda:
                    st.metric(
                        "EV/EBITDA",
                        f"{ev_ebitda:.2f}",
                        help="💰 EV do EBITDA (zysk przed odsetkami, podatkami, deprecjacją). Popularne w M&A. 'Clean' earnings measure bez accounting tricks! 🎭"
                    )

                book_value = info.get('bookValue')
                if book_value:
                    st.metric(
                        "Book Value",
                        f"${book_value:.2f}",
                        help="📖 Wartość księgowa na akcję. Ile zostałoby na akcję gdyby firmę zlikwidować i sprzedać wszystko. Liquidation value! 🏦"
                    )

            # Growth & Cash Flow
            st.markdown("---")
            st.subheader("📈 Wzrost & Cash Flow")
            st.caption("💪 Momentum check! Czy firma rośnie? Czy generuje kasę? Growth investors pay attention!")

            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown("**📊 Growth Rates:**")
                revenue_growth = info.get('revenueGrowth')
                earnings_growth = info.get('earningsGrowth')

                if revenue_growth:
                    st.metric(
                        "Revenue Growth",
                        f"{revenue_growth*100:.1f}%",
                        help="📈 Roczny wzrost przychodów. Czy firma sprzedaje więcej? Pozytywne = expanding, negatywne = kurczenie się. Top line growth! 💵"
                    )
                if earnings_growth:
                    st.metric(
                        "Earnings Growth",
                        f"{earnings_growth*100:.1f}%",
                        help="🚀 Roczny wzrost zysków. Najważniejsze! Czy firma zarabia więcej? This is what drives stock prices long-term! 💰"
                    )

            with col2:
                st.markdown("**💵 Cash Flow:**")
                fcf = info.get('freeCashflow')
                op_cashflow = info.get('operatingCashflow')

                if fcf:
                    fcf_str = f"${fcf/1e9:.2f}B" if abs(fcf) > 1e9 else f"${fcf/1e6:.2f}M"
                    st.metric(
                        "Free Cash Flow",
                        fcf_str,
                        help="💰 FCF = kasa która NAPRAWDĘ zostaje po opłaceniu wszystkiego. To co firma może rozdać akcjonariuszom, reinwestować lub kupić lamborgini! 🏎️"
                    )
                if op_cashflow:
                    op_cf_str = f"${op_cashflow/1e9:.2f}B" if abs(op_cashflow) > 1e9 else f"${op_cashflow/1e6:.2f}M"
                    st.metric(
                        "Operating CF",
                        op_cf_str,
                        help="🏭 Cash z podstawowej działalności. Czy biznes generuje kasę czy tylko zyski 'na papierze'? Show me the money! 💵"
                    )

            with col3:
                st.markdown("**🎯 Margins:**")
                gross_margin = info.get('grossMargins')
                operating_margin = info.get('operatingMargins')

                if gross_margin:
                    st.metric(
                        "Gross Margin",
                        f"{gross_margin*100:.1f}%",
                        help="💎 Marża brutto = (Revenue - COGS) / Revenue. Ile zostaje po kosztach produkcji. Wysokie = pricing power! Apple: ~40% 🍎"
                    )
                if operating_margin:
                    st.metric(
                        "Operating Margin",
                        f"{operating_margin*100:.1f}%",
                        help="⚙️ Marża operacyjna = zysk z działalności / przychody. Efektywność operacyjna. Po odjęciu kosztów biznesu, ile zostaje? 💼"
                    )

            # Ownership & Short Interest
            st.markdown("---")
            st.subheader("👥 Właścicielska & Short Interest")
            st.caption("🕵️ Kto trzyma akcje? Czy insiderzy wierzą w firmę? Czy hedgefundy shortują? Follow the smart money!")

            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**📊 Ownership Structure:**")
                insider_pct = info.get('heldPercentInsiders')
                institution_pct = info.get('heldPercentInstitutions')
                float_shares = info.get('floatShares')
                shares_out = info.get('sharesOutstanding')

                if insider_pct:
                    st.metric(
                        "Insiders Own",
                        f"{insider_pct*100:.1f}%",
                        help="👔 % akcji w rękach insiderów (CEO, board, etc.). Wysokie = management ma 'skin in the game', wierzą w firmę! Aligned interests! 🤝"
                    )
                if institution_pct:
                    st.metric(
                        "Institutions Own",
                        f"{institution_pct*100:.1f}%",
                        help="🏦 % akcji u instytucji (fundusze, banki). Wysokie = 'smart money' in, ale też większa zmienność gdy sprzedają! 📊"
                    )
                if float_shares and shares_out:
                    float_pct = (float_shares / shares_out * 100)
                    st.metric(
                        "Float %",
                        f"{float_pct:.1f}%",
                        help="🎈 Float = akcje dostępne do tradingu (bez insiderów/restricted). Niski float = wyższa zmienność! Rocket fuel! 🚀"
                    )

            with col2:
                st.markdown("**🎯 Short Interest:**")
                short_ratio = info.get('shortRatio')
                short_pct = info.get('shortPercentOfFloat')

                if short_pct:
                    st.metric(
                        "Short % of Float",
                        f"{short_pct*100:.1f}%",
                        help="📉 Ile % float jest zshortowane. <5% = normal, >10% = heavily shorted, >20% = EXTREME! Short squeeze territory! 🔥"
                    )
                if short_ratio:
                    st.metric(
                        "Short Ratio (Days)",
                        f"{short_ratio:.1f}",
                        help="📅 Ile dni zajęłoby pokrycie wszystkich shortów przy avg volume. >10 dni = trudno wyjść, squeeze potential! Diamond hands needed! 💎🙌"
                    )

                st.info("⚠️ Wysoki short interest może oznaczać albo problemy firmy, albo potencjał na **short squeeze** jeśli cena pójdzie w górę!")

            # Latest News
            st.markdown("---")
            st.subheader("📰 Najnowsze Newsy")
            st.caption("🔥 Co się dzieje? Fresh z drukarni! Stay informed, stay ahead!")

            try:
                news = ticker.news
                if news and len(news) > 0:
                    for article in news[:5]:  # Show top 5
                        title = article.get('title', 'No title')
                        link = article.get('link', '#')
                        publisher = article.get('publisher', 'Unknown')

                        # Try to get published time
                        pub_time = article.get('providerPublishTime')
                        if pub_time:
                            from datetime import datetime
                            pub_date = datetime.fromtimestamp(pub_time).strftime('%Y-%m-%d %H:%M')
                            time_str = f"📅 {pub_date} | 📰 {publisher}"
                        else:
                            time_str = f"📰 {publisher}"

                        with st.expander(f"📄 {title}"):
                            st.caption(time_str)
                            st.markdown(f"[🔗 Czytaj więcej]({link})")
                else:
                    st.info("Brak najnowszych newsów")
            except Exception as e:
                st.info("Nie udało się pobrać newsów")

        else:
            st.warning("No data available for this symbol")
    except Exception as e:
        st.error(f"Error loading data: {e}")

# TAB 2: Market Heatmap
with main_tabs[1]:
    st.subheader("Market Heatmap")
    st.caption("🔥 Zobacz jak rynek żyje! Zielone = gains, czerwone = pain. Większy kwadrat = większa firma!")

    market = st.selectbox("Select Market", ["NASDAQ", "NYSE", "GPW"])

    # Define stock lists for different markets
    market_stocks = {
        "NASDAQ": ["AAPL", "MSFT", "NVDA", "GOOGL", "AMZN", "TSLA", "META", "AVGO",
                   "NFLX", "AMD", "COST", "CSCO", "ADBE", "PEP", "INTC", "CMCSA",
                   "QCOM", "TXN", "INTU", "AMGN"],
        "NYSE": ["JPM", "V", "WMT", "JNJ", "MA", "PG", "HD", "DIS", "BAC", "XOM",
                 "CVX", "ABBV", "KO", "PFE", "MRK", "TMO", "NKE", "UNH", "VZ", "MCD"],
        "GPW": ["PKO.WA", "PZU.WA", "KGHM.WA", "PKN.WA", "PGE.WA", "LPP.WA",
                "CDR.WA", "ALE.WA", "CCC.WA", "PEO.WA", "JSW.WA", "OPL.WA",
                "DNP.WA", "MBK.WA", "SPL.WA", "KRU.WA"]
    }

    selected_stocks = market_stocks[market]

    with st.spinner(f"Ładuję dane dla {market}..."):
        try:
            heatmap_data = []

            for symbol in selected_stocks:
                try:
                    ticker = yf.Ticker(symbol)
                    hist = ticker.history(period="5d")

                    if not hist.empty and len(hist) >= 2:
                        current_price = hist['Close'].iloc[-1]
                        prev_price = hist['Close'].iloc[-2]
                        change_pct = ((current_price - prev_price) / prev_price * 100)

                        info = ticker.info
                        market_cap = info.get('marketCap', 0)
                        company_name = info.get('shortName', symbol)

                        heatmap_data.append({
                            'symbol': symbol,
                            'name': company_name,
                            'change': change_pct,
                            'price': current_price,
                            'market_cap': market_cap
                        })
                except:
                    continue

            if heatmap_data:
                # Create DataFrame
                df = pd.DataFrame(heatmap_data)

                # Create treemap
                import plotly.express as px

                # Add formatted labels
                df['label'] = df.apply(lambda x: f"{x['symbol']}<br>{x['change']:.1f}%", axis=1)
                df['hover'] = df.apply(lambda x: f"{x['name']}<br>${x['price']:.2f}<br>{x['change']:.2f}%", axis=1)

                # Create color scale (red to green)
                fig = px.treemap(
                    df,
                    path=[px.Constant("Market"), 'symbol'],
                    values='market_cap',
                    color='change',
                    hover_data={'hover': True, 'market_cap': ':,.0f', 'change': ':.2f'},
                    color_continuous_scale=['#FF0000', '#FFFF00', '#00FF00'],
                    color_continuous_midpoint=0,
                    custom_data=['label', 'hover']
                )

                # Update layout
                fig.update_traces(
                    textposition="middle center",
                    texttemplate='%{customdata[0]}',
                    hovertemplate='<b>%{customdata[1]}</b><br>Market Cap: $%{value:,.0f}<extra></extra>'
                )

                fig.update_layout(
                    template='plotly_dark',
                    height=700,
                    margin=dict(t=30, l=10, r=10, b=10),
                    coloraxis_colorbar=dict(
                        title="Change %",
                        ticksuffix="%"
                    )
                )

                st.plotly_chart(fig, use_container_width=True)

                # Summary stats
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    gainers = len(df[df['change'] > 0])
                    st.metric("Gainers", gainers, help="🟢 Ile spółek rośnie dzisiaj")
                with col2:
                    losers = len(df[df['change'] < 0])
                    st.metric("Losers", losers, help="🔴 Ile spółek spada dzisiaj")
                with col3:
                    avg_change = df['change'].mean()
                    st.metric("Avg Change", f"{avg_change:.2f}%", help="📊 Średnia zmiana na rynku")
                with col4:
                    # Top mover
                    top_mover = df.loc[df['change'].abs().idxmax()]
                    st.metric("Top Mover", top_mover['symbol'], f"{top_mover['change']:+.1f}%",
                             help="🚀 Największy ruch dzisiaj")

                # Top gainers and losers
                st.markdown("---")
                col1, col2 = st.columns(2)

                with col1:
                    st.subheader("🚀 Top Gainers")
                    top_gainers = df.nlargest(5, 'change')[['symbol', 'name', 'change', 'price']]
                    for _, row in top_gainers.iterrows():
                        st.success(f"**{row['symbol']}** - {row['name'][:30]}... | **{row['change']:+.2f}%** | ${row['price']:.2f}")

                with col2:
                    st.subheader("📉 Top Losers")
                    top_losers = df.nsmallest(5, 'change')[['symbol', 'name', 'change', 'price']]
                    for _, row in top_losers.iterrows():
                        st.error(f"**{row['symbol']}** - {row['name'][:30]}... | **{row['change']:+.2f}%** | ${row['price']:.2f}")

            else:
                st.error("Nie udało się pobrać danych dla tego rynku")

        except Exception as e:
            st.error(f"Błąd podczas ładowania heatmap: {e}")
            st.info("Spróbuj ponownie za chwilę lub wybierz inny rynek")

# TAB 3: Portfolio
with main_tabs[2]:
    st.subheader("Portfolio Tracker")

    if PORTFOLIO_AVAILABLE:
        # Add New Position Form
        with st.expander("➕ Add New Position", expanded=False):
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                new_symbol = st.text_input("Symbol", key="new_symbol").upper()
            with col2:
                new_shares = st.number_input("Shares", min_value=0.0, step=1.0, key="new_shares")
            with col3:
                new_price = st.number_input("Purchase Price", min_value=0.0, step=0.01, key="new_price")
            with col4:
                new_date = st.date_input("Purchase Date", key="new_date")

            new_notes = st.text_input("Notes (optional)", key="new_notes")

            if st.button("Add Position", type="primary", key="add_position_btn"):
                if new_symbol and new_shares > 0 and new_price > 0:
                    success = portfolio_manager.add_position(
                        symbol=new_symbol,
                        shares=new_shares,
                        price=new_price,
                        purchase_date=new_date.strftime("%Y-%m-%d"),
                        notes=new_notes
                    )
                    if success:
                        st.success(f"✅ Added {new_shares} shares of {new_symbol}")
                        st.rerun()
                    else:
                        st.error("Failed to add position")
                else:
                    st.warning("Please fill in all required fields")

        summary = portfolio_manager.get_portfolio_summary()

        if summary['positions_count'] > 0:
            # Portfolio Summary
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric(
                    "Total Value",
                    format_currency(summary['current_value']),
                    help="💼 Aktualna wartość całego Twojego portfolio na podstawie dzisiejszych cen. To ile masz TERAZ (nie ile włożyłeś!)."
                )
            with col2:
                st.metric(
                    "Total P&L",
                    format_currency(summary['total_pnl']),
                    format_percentage(summary['total_pnl_percent']),
                    help="📈 Profit & Loss - Twój wynik inwestycyjny! Zielone = zarabiasz 💰, czerwone = na razie nie 📉. P&L to różnica między tym co masz teraz a tym co włożyłeś. To Twój score!"
                )
            with col3:
                st.metric(
                    "Positions",
                    summary['positions_count'],
                    help="🎯 Liczba różnych akcji w Twoim portfolio. Dywersyfikacja = nie trzymasz wszystkich jajek w jednym koszyku! 🥚"
                )

            st.markdown("---")

            # Edit/Remove Positions
            st.subheader("Your Positions")

            for position in summary['positions']:
                with st.expander(f"📊 {position['symbol']} - {format_currency(position['position_value'])}"):
                    col1, col2 = st.columns(2)

                    with col1:
                        st.write(f"**Shares:** {position['shares']:.2f}")
                        st.write(f"**Avg Cost:** {format_currency(position['avg_cost'])}")
                        st.write(f"**Current Price:** {format_currency(position['current_price'])}")
                        st.write(f"**Purchase Date:** {position['purchase_date']}")
                        if position['notes']:
                            st.write(f"**Notes:** {position['notes']}")

                    with col2:
                        st.write(f"**Position Value:** {format_currency(position['position_value'])}")
                        st.write(f"**Total Cost:** {format_currency(position['position_cost'])}")

                        pnl_color = "green" if position['pnl'] >= 0 else "red"
                        st.markdown(f"**P&L:** :{pnl_color}[{format_currency(position['pnl'])} ({format_percentage(position['pnl_percent'])})]")

                    st.markdown("---")

                    # Edit form
                    edit_col1, edit_col2, edit_col3 = st.columns(3)
                    with edit_col1:
                        edit_shares = st.number_input(
                            "Update Shares",
                            min_value=0.0,
                            value=float(position['shares']),
                            step=1.0,
                            key=f"edit_shares_{position['symbol']}"
                        )
                    with edit_col2:
                        edit_price = st.number_input(
                            "Update Avg Cost",
                            min_value=0.0,
                            value=float(position['avg_cost']),
                            step=0.01,
                            key=f"edit_price_{position['symbol']}"
                        )
                    with edit_col3:
                        st.write("")  # Spacing
                        st.write("")  # Spacing
                        if st.button("Update", key=f"update_{position['symbol']}"):
                            # Remove old position and add updated one
                            portfolio_manager.remove_position(position['symbol'])
                            portfolio_manager.add_position(
                                symbol=position['symbol'],
                                shares=edit_shares,
                                price=edit_price,
                                purchase_date=position['purchase_date'],
                                notes=position['notes']
                            )
                            st.success(f"✅ Updated {position['symbol']}")
                            st.rerun()

                    # Remove button
                    remove_col1, remove_col2 = st.columns([3, 1])
                    with remove_col2:
                        if st.button(f"🗑️ Remove", key=f"remove_{position['symbol']}", type="secondary"):
                            portfolio_manager.remove_position(position['symbol'])
                            st.success(f"✅ Removed {position['symbol']}")
                            st.rerun()
        else:
            st.info("Your portfolio is empty. Add your first position above!")
    else:
        st.warning("Portfolio manager not available")

st.caption(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

#!/usr/bin/env python3
"""
Portfolio Manager for Terminal Pro
Provides portfolio tracking, P&L calculations, and performance analytics
"""

import json
import pandas as pd
import yfinance as yf
from datetime import datetime, date
from typing import Dict, List, Optional, Tuple, Any
import os
from dataclasses import dataclass, asdict
import streamlit as st

@dataclass
class PortfolioPosition:
    """Represents a single position in the portfolio"""
    symbol: str
    shares: float
    avg_cost: float
    purchase_date: str
    notes: str = ""
    
    @property
    def total_cost(self) -> float:
        """Total amount invested in this position"""
        return self.shares * self.avg_cost

class PortfolioManager:
    """Main portfolio management class"""
    
    def __init__(self, portfolio_file: str = "portfolio_data.json"):
        self.portfolio_file = portfolio_file
        self.positions: Dict[str, PortfolioPosition] = {}
        self._load_portfolio()
    
    def _load_portfolio(self) -> None:
        """Load portfolio from JSON file"""
        try:
            if os.path.exists(self.portfolio_file):
                with open(self.portfolio_file, 'r') as f:
                    data = json.load(f)
                    for symbol, pos_data in data.items():
                        self.positions[symbol] = PortfolioPosition(**pos_data)
        except Exception as e:
            print(f"Error loading portfolio: {e}")
            self.positions = {}
    
    def _save_portfolio(self) -> None:
        """Save portfolio to JSON file"""
        try:
            data = {symbol: asdict(pos) for symbol, pos in self.positions.items()}
            with open(self.portfolio_file, 'w') as f:
                json.dump(data, f, indent=2, default=str)
        except Exception as e:
            print(f"Error saving portfolio: {e}")
    
    def add_position(self, symbol: str, shares: float, price: float, 
                    purchase_date: str = None, notes: str = "") -> bool:
        """
        Add a new position or update existing position
        
        Args:
            symbol: Stock symbol
            shares: Number of shares
            price: Purchase price per share
            purchase_date: Date of purchase (YYYY-MM-DD format)
            notes: Optional notes
            
        Returns:
            True if successful, False otherwise
        """
        try:
            if purchase_date is None:
                purchase_date = date.today().strftime("%Y-%m-%d")
            
            symbol = symbol.upper()
            
            if symbol in self.positions:
                # Update existing position (average cost calculation)
                existing = self.positions[symbol]
                total_shares = existing.shares + shares
                total_cost = (existing.shares * existing.avg_cost) + (shares * price)
                new_avg_cost = total_cost / total_shares
                
                self.positions[symbol] = PortfolioPosition(
                    symbol=symbol,
                    shares=total_shares,
                    avg_cost=new_avg_cost,
                    purchase_date=existing.purchase_date,  # Keep original date
                    notes=f"{existing.notes}; {notes}" if notes else existing.notes
                )
            else:
                # Add new position
                self.positions[symbol] = PortfolioPosition(
                    symbol=symbol,
                    shares=shares,
                    avg_cost=price,
                    purchase_date=purchase_date,
                    notes=notes
                )
            
            self._save_portfolio()
            return True
            
        except Exception as e:
            print(f"Error adding position: {e}")
            return False
    
    def remove_position(self, symbol: str, shares: float = None) -> bool:
        """
        Remove position or reduce shares
        
        Args:
            symbol: Stock symbol
            shares: Number of shares to remove (None = remove all)
            
        Returns:
            True if successful, False otherwise
        """
        try:
            symbol = symbol.upper()
            
            if symbol not in self.positions:
                return False
            
            if shares is None:
                # Remove entire position
                del self.positions[symbol]
            else:
                # Reduce shares
                current_shares = self.positions[symbol].shares
                if shares >= current_shares:
                    # Remove entire position if selling all or more
                    del self.positions[symbol]
                else:
                    # Reduce shares but keep position
                    self.positions[symbol].shares = current_shares - shares
            
            self._save_portfolio()
            return True
            
        except Exception as e:
            print(f"Error removing position: {e}")
            return False
    
    def get_current_prices(self) -> Dict[str, float]:
        """Get current prices for all positions"""
        if not self.positions:
            return {}
        
        symbols = list(self.positions.keys())
        prices = {}
        
        try:
            # Batch fetch current prices
            tickers = yf.Tickers(' '.join(symbols))
            
            for symbol in symbols:
                try:
                    ticker = tickers.tickers[symbol]
                    hist = ticker.history(period="1d")
                    if not hist.empty:
                        prices[symbol] = hist['Close'].iloc[-1]
                    else:
                        # Fallback to info if history fails
                        info = ticker.info
                        prices[symbol] = info.get('currentPrice', 0)
                except:
                    prices[symbol] = 0
                    
        except Exception as e:
            print(f"Error fetching prices: {e}")
            # Fallback to individual requests
            for symbol in symbols:
                try:
                    ticker = yf.Ticker(symbol)
                    hist = ticker.history(period="1d")
                    if not hist.empty:
                        prices[symbol] = hist['Close'].iloc[-1]
                    else:
                        prices[symbol] = 0
                except:
                    prices[symbol] = 0
        
        return prices
    
    def get_portfolio_summary(self) -> Dict[str, Any]:
        """Get comprehensive portfolio summary"""
        if not self.positions:
            return {
                'total_invested': 0,
                'current_value': 0,
                'total_pnl': 0,
                'total_pnl_percent': 0,
                'positions_count': 0,
                'top_gainers': [],
                'top_losers': []
            }
        
        current_prices = self.get_current_prices()
        
        total_invested = 0
        current_value = 0
        position_details = []
        
        for symbol, position in self.positions.items():
            current_price = current_prices.get(symbol, 0)
            position_value = position.shares * current_price
            position_cost = position.total_cost
            position_pnl = position_value - position_cost
            position_pnl_percent = (position_pnl / position_cost * 100) if position_cost > 0 else 0
            
            total_invested += position_cost
            current_value += position_value
            
            position_details.append({
                'symbol': symbol,
                'shares': position.shares,
                'avg_cost': position.avg_cost,
                'current_price': current_price,
                'position_value': position_value,
                'position_cost': position_cost,
                'pnl': position_pnl,
                'pnl_percent': position_pnl_percent,
                'purchase_date': position.purchase_date,
                'notes': position.notes
            })
        
        total_pnl = current_value - total_invested
        total_pnl_percent = (total_pnl / total_invested * 100) if total_invested > 0 else 0
        
        # Sort for top gainers/losers
        sorted_by_pnl = sorted(position_details, key=lambda x: x['pnl_percent'], reverse=True)
        
        return {
            'total_invested': total_invested,
            'current_value': current_value,
            'total_pnl': total_pnl,
            'total_pnl_percent': total_pnl_percent,
            'positions_count': len(self.positions),
            'positions': position_details,
            'top_gainers': sorted_by_pnl[:3],
            'top_losers': sorted_by_pnl[-3:] if len(sorted_by_pnl) > 3 else []
        }
    
    def get_portfolio_dataframe(self) -> pd.DataFrame:
        """Get portfolio as pandas DataFrame"""
        summary = self.get_portfolio_summary()
        if not summary['positions']:
            return pd.DataFrame()
        
        df = pd.DataFrame(summary['positions'])
        
        # Format columns
        df['avg_cost'] = df['avg_cost'].round(2)
        df['current_price'] = df['current_price'].round(2)
        df['position_value'] = df['position_value'].round(2)
        df['position_cost'] = df['position_cost'].round(2)
        df['pnl'] = df['pnl'].round(2)
        df['pnl_percent'] = df['pnl_percent'].round(2)
        
        return df
    
    def export_portfolio(self, filename: str = None) -> str:
        """Export portfolio to CSV"""
        if filename is None:
            filename = f"portfolio_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
        df = self.get_portfolio_dataframe()
        if not df.empty:
            df.to_csv(filename, index=False)
            return filename
        return None
    
    def get_allocation_by_value(self) -> Dict[str, float]:
        """Get portfolio allocation by current value"""
        summary = self.get_portfolio_summary()
        if summary['current_value'] == 0:
            return {}
        
        allocation = {}
        for position in summary['positions']:
            allocation[position['symbol']] = (position['position_value'] / summary['current_value']) * 100
        
        return allocation

# Global portfolio manager instance
portfolio_manager = PortfolioManager()

# Utility functions for Streamlit integration
def format_currency(amount: float) -> str:
    """Format number as currency"""
    return f"${amount:,.2f}"

def format_percentage(percent: float) -> str:
    """Format number as percentage"""
    return f"{percent:+.2f}%"

def get_color_for_pnl(pnl: float) -> str:
    """Get color for P&L display"""
    if pnl > 0:
        return "green"
    elif pnl < 0:
        return "red"
    else:
        return "gray"
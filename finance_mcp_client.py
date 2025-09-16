#!/usr/bin/env python3
"""
FinanceMCP Client for Terminal Pro
Provides integration with FinanceMCP server for enhanced financial data
"""

import json
import subprocess
import asyncio
from typing import Dict, List, Optional, Any
import pandas as pd
from datetime import datetime, timedelta

class FinanceMCPClient:
    """Client to interact with FinanceMCP server"""
    
    def __init__(self):
        self.server_command = ["npx", "finance-mcp"]
        self.available_tools = [
            'stock_data',
            'finance_news', 
            'macro_econ',
            'company_performance',
            'stock_data_minutes'
        ]
    
    def _call_mcp_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Optional[Dict]:
        """
        Call an MCP tool and return the result
        
        Args:
            tool_name: Name of the MCP tool to call
            arguments: Arguments to pass to the tool
            
        Returns:
            Tool result as dictionary or None if error
        """
        try:
            # Prepare the MCP message
            mcp_request = {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "tools/call",
                "params": {
                    "name": tool_name,
                    "arguments": arguments
                }
            }
            
            # Call the MCP server
            process = subprocess.Popen(
                self.server_command,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            stdout, stderr = process.communicate(
                input=json.dumps(mcp_request),
                timeout=30
            )
            
            if process.returncode == 0 and stdout.strip():
                response = json.loads(stdout.strip())
                if 'result' in response:
                    return response['result']
            
            return None
            
        except Exception as e:
            print(f"Error calling MCP tool {tool_name}: {e}")
            return None
    
    def get_stock_data(self, symbol: str, period: str = "1y", 
                      interval: str = "1d", indicators: List[str] = None) -> Optional[pd.DataFrame]:
        """
        Get enhanced stock data with technical indicators
        
        Args:
            symbol: Stock symbol (e.g., 'AAPL')
            period: Time period (e.g., '1y', '6m', '3m')
            interval: Data interval (e.g., '1d', '1h', '15m')
            indicators: List of technical indicators to include
            
        Returns:
            DataFrame with stock data and indicators
        """
        if indicators is None:
            indicators = ['SMA_20', 'SMA_50', 'RSI', 'MACD', 'BOLL']
            
        arguments = {
            "symbol": symbol,
            "period": period,
            "interval": interval,
            "indicators": indicators
        }
        
        result = self._call_mcp_tool("stock_data", arguments)
        
        if result and 'data' in result:
            try:
                # Convert result to pandas DataFrame
                data = result['data']
                if isinstance(data, list) and len(data) > 0:
                    df = pd.DataFrame(data)
                    
                    # Ensure datetime index if available
                    if 'Date' in df.columns:
                        df['Date'] = pd.to_datetime(df['Date'])
                        df.set_index('Date', inplace=True)
                    elif 'Datetime' in df.columns:
                        df['Datetime'] = pd.to_datetime(df['Datetime'])
                        df.set_index('Datetime', inplace=True)
                    
                    return df
                    
            except Exception as e:
                print(f"Error processing stock data: {e}")
        
        return None
    
    def get_minute_data(self, symbol: str, days: int = 5) -> Optional[pd.DataFrame]:
        """
        Get minute-level stock data (K-line data)
        
        Args:
            symbol: Stock symbol
            days: Number of days to fetch (max 30)
            
        Returns:
            DataFrame with minute-level data
        """
        arguments = {
            "symbol": symbol,
            "days": min(days, 30)  # Limit to prevent overload
        }
        
        result = self._call_mcp_tool("stock_data_minutes", arguments)
        
        if result and 'data' in result:
            try:
                data = result['data']
                if isinstance(data, list) and len(data) > 0:
                    df = pd.DataFrame(data)
                    
                    # Convert timestamp to datetime
                    if 'Timestamp' in df.columns:
                        df['Timestamp'] = pd.to_datetime(df['Timestamp'])
                        df.set_index('Timestamp', inplace=True)
                    
                    return df
                    
            except Exception as e:
                print(f"Error processing minute data: {e}")
        
        return None
    
    def get_financial_news(self, symbol: str = None, keyword: str = None, 
                          limit: int = 10) -> Optional[List[Dict]]:
        """
        Get financial news from FinanceMCP
        
        Args:
            symbol: Stock symbol to filter news
            keyword: Keyword to search for
            limit: Maximum number of articles
            
        Returns:
            List of news articles
        """
        arguments = {
            "limit": limit
        }
        
        if symbol:
            arguments["symbol"] = symbol
        if keyword:
            arguments["keyword"] = keyword
            
        result = self._call_mcp_tool("finance_news", arguments)
        
        if result and 'articles' in result:
            return result['articles'][:limit]
        
        return None
    
    def get_company_performance(self, symbol: str, market: str = "US") -> Optional[Dict]:
        """
        Get comprehensive company performance data
        
        Args:
            symbol: Stock symbol
            market: Market type (US, HK, A-shares)
            
        Returns:
            Dictionary with performance metrics
        """
        arguments = {
            "symbol": symbol,
            "market": market
        }
        
        result = self._call_mcp_tool("company_performance", arguments)
        
        if result:
            return result
        
        return None
    
    def get_macro_economic_data(self, indicators: List[str] = None, 
                               region: str = "US") -> Optional[Dict]:
        """
        Get macroeconomic indicators
        
        Args:
            indicators: List of economic indicators to fetch
            region: Region/country for data
            
        Returns:
            Dictionary with economic data
        """
        if indicators is None:
            indicators = ["GDP", "CPI", "unemployment_rate", "interest_rate"]
            
        arguments = {
            "indicators": indicators,
            "region": region
        }
        
        result = self._call_mcp_tool("macro_econ", arguments)
        
        if result:
            return result
        
        return None
    
    def test_connection(self) -> bool:
        """
        Test if FinanceMCP server is available
        
        Returns:
            True if server is responsive, False otherwise
        """
        try:
            # Try a simple stock data call
            result = self.get_stock_data("AAPL", period="1d", interval="1d")
            return result is not None
        except:
            return False
    
    def get_available_indicators(self) -> List[str]:
        """
        Get list of available technical indicators
        
        Returns:
            List of indicator names
        """
        return [
            'SMA_5', 'SMA_10', 'SMA_20', 'SMA_50', 'SMA_200',
            'EMA_12', 'EMA_26', 'EMA_50',
            'RSI', 'RSI_14',
            'MACD', 'MACD_Signal', 'MACD_Histogram', 
            'BOLL', 'BOLL_Upper', 'BOLL_Lower',
            'KDJ_K', 'KDJ_D', 'KDJ_J',
            'ATR', 'ATR_14',
            'Stoch_K', 'Stoch_D',
            'Williams_R',
            'CCI',
            'MFI'
        ]

# Global instance for easy import
finance_mcp = FinanceMCPClient()

# Test function for debugging
def test_finance_mcp():
    """Test function to verify FinanceMCP integration"""
    print("Testing FinanceMCP integration...")
    
    # Test connection
    if finance_mcp.test_connection():
        print("OK FinanceMCP connection successful")
        
        # Test stock data
        print("\nTesting stock data...")
        stock_data = finance_mcp.get_stock_data("AAPL", period="5d")
        if stock_data is not None:
            print(f"OK Stock data retrieved: {len(stock_data)} rows")
            print(f"Columns: {list(stock_data.columns)}")
        else:
            print("FAIL Failed to get stock data")
        
        # Test news
        print("\nTesting news...")
        news = finance_mcp.get_financial_news("AAPL", limit=3)
        if news:
            print(f"OK News retrieved: {len(news)} articles")
        else:
            print("FAIL Failed to get news")
            
        # Test company performance
        print("\nTesting company performance...")
        performance = finance_mcp.get_company_performance("AAPL")
        if performance:
            print("OK Company performance data retrieved")
        else:
            print("FAIL Failed to get company performance")
            
    else:
        print("X FinanceMCP connection failed")
        print("Make sure FinanceMCP is installed: npm install -g finance-mcp")

if __name__ == "__main__":
    test_finance_mcp()
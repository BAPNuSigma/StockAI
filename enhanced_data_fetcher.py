import os
from typing import Dict, List, Optional
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import yfinance as yf
from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame
from tiingo import TiingoClient
import requests
from dotenv import load_dotenv

class EnhancedDataFetcher:
    def __init__(self):
        """Initialize data fetchers with API keys from environment variables."""
        load_dotenv()
        
        # Initialize API clients
        self.alpaca_client = StockHistoricalDataClient(
            api_key=os.getenv('ALPACA_API_KEY'),
            secret_key=os.getenv('ALPACA_SECRET_KEY')
        )
        
        self.tiingo_client = TiingoClient({
            'api_key': os.getenv('TIINGO_API_KEY')
        })
        
        self.fmp_api_key = os.getenv('FMP_API_KEY')
        self.fmp_base_url = "https://financialmodelingprep.com/api/v3"
        
    def get_real_time_data(self, ticker: str) -> Dict:
        """
        Get real-time data from Alpaca.
        
        Args:
            ticker (str): Stock ticker symbol
            
        Returns:
            Dict: Real-time market data
        """
        try:
            request_params = StockBarsRequest(
                symbol_or_symbols=ticker,
                timeframe=TimeFrame.Minute,
                start=datetime.now() - timedelta(days=1),
                end=datetime.now()
            )
            bars = self.alpaca_client.get_stock_bars(request_params)
            return {
                'last_price': bars[ticker][-1].close,
                'volume': bars[ticker][-1].volume,
                'timestamp': bars[ticker][-1].timestamp
            }
        except Exception as e:
            print(f"Error fetching real-time data: {e}")
            return {}
    
    def get_financial_statements(self, ticker: str) -> Dict:
        """
        Get financial statements from Financial Modeling Prep.
        
        Args:
            ticker (str): Stock ticker symbol
            
        Returns:
            Dict: Financial statements data
        """
        try:
            # Get income statement
            income_stmt_url = f"{self.fmp_base_url}/income-statement/{ticker}?apikey={self.fmp_api_key}"
            income_stmt = requests.get(income_stmt_url).json()
            
            # Get balance sheet
            balance_sheet_url = f"{self.fmp_base_url}/balance-sheet-statement/{ticker}?apikey={self.fmp_api_key}"
            balance_sheet = requests.get(balance_sheet_url).json()
            
            # Get cash flow
            cash_flow_url = f"{self.fmp_base_url}/cash-flow-statement/{ticker}?apikey={self.fmp_api_key}"
            cash_flow = requests.get(cash_flow_url).json()
            
            return {
                'income_statement': income_stmt,
                'balance_sheet': balance_sheet,
                'cash_flow': cash_flow
            }
        except Exception as e:
            print(f"Error fetching financial statements: {e}")
            return {}
    
    def get_company_profile(self, ticker: str) -> Dict:
        """
        Get company profile information from Yahoo Finance.
        
        Args:
            ticker (str): Stock ticker symbol
            
        Returns:
            Dict: Company profile data
        """
        try:
            # Get data from Yahoo Finance
            yf_ticker = yf.Ticker(ticker)
            yf_info = yf_ticker.info
            
            return {
                'name': yf_info.get('longName', ''),
                'sector': yf_info.get('sector', ''),
                'industry': yf_info.get('industry', ''),
                'description': yf_info.get('longBusinessSummary', ''),
                'website': yf_info.get('website', ''),
                'employees': yf_info.get('fullTimeEmployees', 0),
                'market_cap': yf_info.get('marketCap', 0),
                'pe_ratio': yf_info.get('trailingPE', 0),
                'dividend_yield': yf_info.get('dividendYield', 0),
                'beta': yf_info.get('beta', 0),
                'fifty_two_week_high': yf_info.get('fiftyTwoWeekHigh', 0),
                'fifty_two_week_low': yf_info.get('fiftyTwoWeekLow', 0),
                'fifty_day_average': yf_info.get('fiftyDayAverage', 0),
                'two_hundred_day_average': yf_info.get('twoHundredDayAverage', 0),
                'shares_outstanding': yf_info.get('sharesOutstanding', 0),
                'shares_float': yf_info.get('floatShares', 0),
                'shares_short': yf_info.get('sharesShort', 0),
                'short_ratio': yf_info.get('shortRatio', 0),
                'short_percent_of_float': yf_info.get('shortPercentOfFloat', 0),
                'institution_ownership': yf_info.get('institutionOwnership', 0),
                'insider_ownership': yf_info.get('insiderOwnership', 0)
            }
        except Exception as e:
            print(f"Error fetching company profile: {e}")
            return {}
    
    def get_news(self, ticker: str, limit: int = 10) -> List[Dict]:
        """
        Get recent news articles from Yahoo Finance.
        
        Args:
            ticker (str): Stock ticker symbol
            limit (int): Maximum number of news articles to return
            
        Returns:
            List[Dict]: List of news articles
        """
        try:
            yf_ticker = yf.Ticker(ticker)
            news = yf_ticker.news
            
            formatted_news = []
            for article in news[:limit]:
                formatted_news.append({
                    'title': article.get('title', ''),
                    'publisher': article.get('publisher', ''),
                    'link': article.get('link', ''),
                    'published': datetime.fromtimestamp(article.get('providerPublishTime', 0)),
                    'type': article.get('type', ''),
                    'summary': article.get('summary', '')
                })
            
            return formatted_news
        except Exception as e:
            print(f"Error fetching news: {e}")
            return []
    
    def get_historical_data(self, ticker: str, period: str = "5y") -> pd.DataFrame:
        """
        Get historical data from Tiingo.
        
        Args:
            ticker (str): Stock ticker symbol
            period (str): Time period for historical data
            
        Returns:
            pd.DataFrame: Historical price data
        """
        try:
            historical_data = self.tiingo_client.get_dataframe(
                ticker,
                startDate=datetime.now() - timedelta(days=365*5),
                endDate=datetime.now(),
                frequency='daily'
            )
            return historical_data
        except Exception as e:
            print(f"Error fetching historical data: {e}")
            return pd.DataFrame()
    
    def calculate_valuation_metrics(self, ticker: str) -> Dict:
        """
        Calculate comprehensive valuation metrics using data from multiple sources.
        
        Args:
            ticker (str): Stock ticker symbol
            
        Returns:
            Dict: Valuation metrics
        """
        try:
            # Get data from multiple sources
            financials = self.get_financial_statements(ticker)
            profile = self.get_company_profile(ticker)
            real_time = self.get_real_time_data(ticker)
            
            # Calculate key metrics
            current_price = real_time.get('last_price', 0)
            market_cap = profile.get('market_cap', 0)
            
            # Calculate growth metrics
            if financials.get('income_statement'):
                income_stmt = financials['income_statement']
                revenue_growth = (
                    (income_stmt[0]['revenue'] - income_stmt[1]['revenue']) /
                    income_stmt[1]['revenue']
                ) if len(income_stmt) > 1 else 0
                
                earnings_growth = (
                    (income_stmt[0]['netIncome'] - income_stmt[1]['netIncome']) /
                    income_stmt[1]['netIncome']
                ) if len(income_stmt) > 1 else 0
            else:
                revenue_growth = 0
                earnings_growth = 0
            
            # Calculate financial health metrics
            if financials.get('balance_sheet'):
                balance_sheet = financials['balance_sheet']
                total_assets = balance_sheet[0]['totalAssets']
                total_liabilities = balance_sheet[0]['totalLiabilities']
                current_assets = balance_sheet[0]['totalCurrentAssets']
                current_liabilities = balance_sheet[0]['totalCurrentLiabilities']
                
                debt_to_equity = total_liabilities / (total_assets - total_liabilities)
                current_ratio = current_assets / current_liabilities
            else:
                debt_to_equity = 0
                current_ratio = 0
            
            return {
                'current_price': current_price,
                'market_cap': market_cap,
                'revenue_growth': revenue_growth,
                'earnings_growth': earnings_growth,
                'debt_to_equity': debt_to_equity,
                'current_ratio': current_ratio,
                'pe_ratio': profile.get('pe_ratio', 0),
                'dividend_yield': profile.get('dividend_yield', 0),
                'beta': profile.get('beta', 0),
                'fifty_two_week_high': profile.get('fifty_two_week_high', 0),
                'fifty_two_week_low': profile.get('fifty_two_week_low', 0),
                'fifty_day_average': profile.get('fifty_day_average', 0),
                'two_hundred_day_average': profile.get('two_hundred_day_average', 0),
                'shares_outstanding': profile.get('shares_outstanding', 0),
                'shares_float': profile.get('shares_float', 0),
                'shares_short': profile.get('shares_short', 0),
                'short_ratio': profile.get('short_ratio', 0),
                'short_percent_of_float': profile.get('short_percent_of_float', 0),
                'institution_ownership': profile.get('institution_ownership', 0),
                'insider_ownership': profile.get('insider_ownership', 0)
            }
        except Exception as e:
            print(f"Error calculating valuation metrics: {e}")
            return {} 
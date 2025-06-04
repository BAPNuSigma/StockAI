import streamlit as st
import plotly.graph_objects as go
from enhanced_data_fetcher import EnhancedDataFetcher
from stock_one_pager import StockOnePager
from technical_analysis import TechnicalAnalyzer
import pandas as pd
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize data fetcher
data_fetcher = EnhancedDataFetcher()

def create_price_chart(historical_data: pd.DataFrame, ticker: str) -> go.Figure:
    """Create an interactive price chart using Plotly."""
    fig = go.Figure()
    
    # Add candlestick chart
    fig.add_trace(go.Candlestick(
        x=historical_data.index,
        open=historical_data['Open'],
        high=historical_data['High'],
        low=historical_data['Low'],
        close=historical_data['Close'],
        name='Price'
    ))
    
    # Add moving averages
    fig.add_trace(go.Scatter(
        x=historical_data.index,
        y=historical_data['SMA_20'],
        name='SMA 20',
        line=dict(color='blue', width=1)
    ))
    fig.add_trace(go.Scatter(
        x=historical_data.index,
        y=historical_data['SMA_50'],
        name='SMA 50',
        line=dict(color='orange', width=1)
    ))
    fig.add_trace(go.Scatter(
        x=historical_data.index,
        y=historical_data['SMA_200'],
        name='SMA 200',
        line=dict(color='red', width=1)
    ))
    
    # Add Bollinger Bands
    fig.add_trace(go.Scatter(
        x=historical_data.index,
        y=historical_data['BB_Upper'],
        name='BB Upper',
        line=dict(color='gray', width=1, dash='dash')
    ))
    fig.add_trace(go.Scatter(
        x=historical_data.index,
        y=historical_data['BB_Lower'],
        name='BB Lower',
        line=dict(color='gray', width=1, dash='dash'),
        fill='tonexty'
    ))
    
    fig.update_layout(
        title=f'{ticker} Price History',
        yaxis_title='Price',
        xaxis_title='Date',
        template='plotly_dark'
    )
    
    return fig

def create_technical_indicators_chart(historical_data: pd.DataFrame) -> go.Figure:
    """Create a chart for technical indicators."""
    fig = go.Figure()
    
    # Add RSI
    fig.add_trace(go.Scatter(
        x=historical_data.index,
        y=historical_data['RSI'],
        name='RSI',
        line=dict(color='purple')
    ))
    # Add overbought/oversold lines
    fig.add_hline(y=70, line_dash="dash", line_color="red")
    fig.add_hline(y=30, line_dash="dash", line_color="green")
    
    # Add MACD
    fig.add_trace(go.Scatter(
        x=historical_data.index,
        y=historical_data['MACD'],
        name='MACD',
        line=dict(color='blue')
    ))
    fig.add_trace(go.Scatter(
        x=historical_data.index,
        y=historical_data['MACD_Signal'],
        name='Signal',
        line=dict(color='orange')
    ))
    fig.add_trace(go.Bar(
        x=historical_data.index,
        y=historical_data['MACD_Hist'],
        name='Histogram',
        marker_color='gray'
    ))
    
    fig.update_layout(
        title='Technical Indicators',
        yaxis_title='Value',
        xaxis_title='Date',
        template='plotly_dark'
    )
    
    return fig

def main():
    st.set_page_config(page_title="Stock One-Pager Generator", layout="wide")
    
    st.title("Stock One-Pager Generator")
    
    # Input for stock ticker
    ticker = st.text_input("Enter Stock Ticker:", "").upper()
    
    if ticker:
        try:
            # Get data
            profile = data_fetcher.get_company_profile(ticker)
            metrics = data_fetcher.calculate_valuation_metrics(ticker)
            historical_data = data_fetcher.get_historical_data(ticker)
            news = data_fetcher.get_news(ticker)
            
            # Calculate technical indicators
            if not historical_data.empty:
                analyzer = TechnicalAnalyzer(historical_data)
                signals = analyzer.get_technical_signals()
            
            # Display company overview
            st.header(f"{profile.get('name', ticker)} ({ticker})")
            st.write(profile.get('description', 'No description available.'))
            
            # Create three columns for metrics
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.subheader("Key Metrics")
                st.metric("Current Price", f"${metrics.get('current_price', 0):.2f}")
                st.metric("Market Cap", f"${metrics.get('market_cap', 0)/1e9:.2f}B")
                st.metric("P/E Ratio", f"{metrics.get('pe_ratio', 0):.2f}")
                st.metric("Dividend Yield", f"{metrics.get('dividend_yield', 0)*100:.2f}%")
            
            with col2:
                st.subheader("Growth & Health")
                st.metric("Revenue Growth", f"{metrics.get('revenue_growth', 0)*100:.2f}%")
                st.metric("Earnings Growth", f"{metrics.get('earnings_growth', 0)*100:.2f}%")
                st.metric("Debt to Equity", f"{metrics.get('debt_to_equity', 0):.2f}")
                st.metric("Current Ratio", f"{metrics.get('current_ratio', 0):.2f}")
            
            with col3:
                st.subheader("Technical Indicators")
                if not historical_data.empty:
                    st.metric("RSI", f"{historical_data['RSI'].iloc[-1]:.2f}")
                    st.metric("MACD", f"{historical_data['MACD'].iloc[-1]:.2f}")
                    st.metric("ADX", f"{historical_data['ADX'].iloc[-1]:.2f}")
                    st.metric("CCI", f"{historical_data['CCI'].iloc[-1]:.2f}")
            
            # Display price chart with indicators
            if not historical_data.empty:
                st.plotly_chart(create_price_chart(historical_data, ticker), use_container_width=True)
                st.plotly_chart(create_technical_indicators_chart(historical_data), use_container_width=True)
            
            # Display technical signals
            if not historical_data.empty:
                st.subheader("Technical Signals")
                tech_col1, tech_col2 = st.columns(2)
                
                with tech_col1:
                    st.write("Moving Averages:")
                    for signal in signals['Moving Averages']:
                        st.write(f"- {signal}")
                    
                    st.write("\nRSI:")
                    for signal in signals['RSI']:
                        st.write(f"- {signal}")
                
                with tech_col2:
                    st.write("MACD:")
                    for signal in signals['MACD']:
                        st.write(f"- {signal}")
                    
                    st.write("\nBollinger Bands:")
                    for signal in signals['Bollinger Bands']:
                        st.write(f"- {signal}")
                    
                    st.write("\nVolume:")
                    for signal in signals['Volume']:
                        st.write(f"- {signal}")
                    
                    st.write("\nTrend:")
                    for signal in signals['Trend']:
                        st.write(f"- {signal}")
            
            # Display news
            if news:
                st.subheader("Latest News")
                for article in news[:5]:  # Show top 5 news articles
                    st.write(f"**{article['title']}**")
                    st.write(f"*{article['source']} - {article['publishedAt']}*")
                    st.write(article['description'])
                    st.write("---")
            
        except Exception as e:
            st.error(f"Error: {str(e)}")

if __name__ == "__main__":
    main() 
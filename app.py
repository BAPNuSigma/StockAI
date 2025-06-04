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

def create_price_chart(historical_data: pd.DataFrame, ticker: str, indicators: dict = None) -> go.Figure:
    """Create an interactive price chart using Plotly."""
    fig = go.Figure()
    
    # Add candlestick chart
    fig.add_trace(go.Candlestick(
        x=historical_data.index,
        open=historical_data['open'],
        high=historical_data['high'],
        low=historical_data['low'],
        close=historical_data['close'],
        name='Price'
    ))
    
    # Add moving averages if available
    if indicators and 'moving_averages' in indicators:
        ma = indicators['moving_averages']
        fig.add_trace(go.Scatter(
            x=historical_data.index,
            y=ma['sma_20'],
            name='SMA 20',
            line=dict(color='blue', width=1)
        ))
        fig.add_trace(go.Scatter(
            x=historical_data.index,
            y=ma['sma_50'],
            name='SMA 50',
            line=dict(color='orange', width=1)
        ))
        fig.add_trace(go.Scatter(
            x=historical_data.index,
            y=ma['sma_200'],
            name='SMA 200',
            line=dict(color='red', width=1)
        ))
    
    # Add Bollinger Bands if available
    if indicators and 'volatility' in indicators:
        bb = indicators['volatility']
        fig.add_trace(go.Scatter(
            x=historical_data.index,
            y=bb['bollinger_upper'],
            name='BB Upper',
            line=dict(color='gray', width=1, dash='dash')
        ))
        fig.add_trace(go.Scatter(
            x=historical_data.index,
            y=bb['bollinger_lower'],
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

def create_technical_indicators_chart(historical_data: pd.DataFrame, indicators: dict) -> go.Figure:
    """Create a chart for technical indicators."""
    fig = go.Figure()
    
    # Add RSI
    if 'momentum' in indicators and 'rsi' in indicators['momentum']:
        fig.add_trace(go.Scatter(
            x=historical_data.index,
            y=indicators['momentum']['rsi'],
            name='RSI',
            line=dict(color='purple')
        ))
        # Add overbought/oversold lines
        fig.add_hline(y=70, line_dash="dash", line_color="red")
        fig.add_hline(y=30, line_dash="dash", line_color="green")
    
    # Add MACD
    if 'momentum' in indicators and 'macd' in indicators['momentum']:
        fig.add_trace(go.Scatter(
            x=historical_data.index,
            y=indicators['momentum']['macd'],
            name='MACD',
            line=dict(color='blue')
        ))
        fig.add_trace(go.Scatter(
            x=historical_data.index,
            y=indicators['momentum']['macd_signal'],
            name='Signal',
            line=dict(color='orange')
        ))
        fig.add_trace(go.Bar(
            x=historical_data.index,
            y=indicators['momentum']['macd_hist'],
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
                indicators = analyzer.get_all_indicators()
                signals = analyzer.get_signal_summary()
            
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
                    st.metric("RSI", f"{signals['rsi']['rsi_value']:.2f}")
                    st.metric("MACD", f"{indicators['momentum']['macd'].iloc[-1]:.2f}")
                    st.metric("ADX", f"{indicators['trend']['adx'].iloc[-1]:.2f}")
                    st.metric("CCI", f"{indicators['trend']['cci'].iloc[-1]:.2f}")
            
            # Display price chart with indicators
            if not historical_data.empty:
                st.plotly_chart(create_price_chart(historical_data, ticker, indicators), use_container_width=True)
                st.plotly_chart(create_technical_indicators_chart(historical_data, indicators), use_container_width=True)
            
            # Display technical signals
            if not historical_data.empty:
                st.subheader("Technical Signals")
                tech_col1, tech_col2 = st.columns(2)
                
                with tech_col1:
                    st.write("Moving Averages:")
                    st.write(f"- Above SMA 20: {'Yes' if signals['moving_averages']['above_sma_20'] else 'No'}")
                    st.write(f"- Above SMA 50: {'Yes' if signals['moving_averages']['above_sma_50'] else 'No'}")
                    st.write(f"- Above SMA 200: {'Yes' if signals['moving_averages']['above_sma_200'] else 'No'}")
                    st.write(f"- Golden Cross: {'Yes' if signals['moving_averages']['golden_cross'] else 'No'}")
                
                with tech_col2:
                    st.write("Momentum Indicators:")
                    st.write(f"- RSI: {signals['rsi']['rsi_value']:.2f} ({'Overbought' if signals['rsi']['overbought'] else 'Oversold' if signals['rsi']['oversold'] else 'Neutral'})")
                    st.write(f"- MACD Signal: {'Bullish' if signals['macd']['bullish_cross'] else 'Bearish' if signals['macd']['bearish_cross'] else 'Neutral'}")
                    st.write(f"- Bollinger Bands: {'Above Upper' if signals['bollinger_bands']['above_upper'] else 'Below Lower' if signals['bollinger_bands']['below_lower'] else 'Within Bands'}")
                    st.write(f"- Bollinger Squeeze: {'Yes' if signals['bollinger_bands']['squeeze'] else 'No'}")
            
            # Display ownership information
            st.subheader("Ownership Information")
            own_col1, own_col2 = st.columns(2)
            
            with own_col1:
                st.metric("Institution Ownership", f"{metrics.get('institution_ownership', 0)*100:.2f}%")
                st.metric("Insider Ownership", f"{metrics.get('insider_ownership', 0)*100:.2f}%")
            
            with own_col2:
                st.metric("Short Interest", f"{metrics.get('shares_short', 0)/1e6:.2f}M")
                st.metric("Short % of Float", f"{metrics.get('short_percent_of_float', 0)*100:.2f}%")
            
            # Display recent news
            st.subheader("Recent News")
            for article in news:
                with st.expander(f"{article['title']} - {article['publisher']} ({article['published'].strftime('%Y-%m-%d')})"):
                    st.write(article['summary'])
                    st.markdown(f"[Read more]({article['link']})")
            
            # Generate one-pagers
            st.subheader("Generate One-Pagers")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if st.button("Generate Growth One-Pager"):
                    generator = StockOnePager(ticker)
                    doc = generator.generate_growth_one_pager()
                    generator.save_one_pager(doc, 'growth')
                    st.success("Growth One-Pager Generated!")
            
            with col2:
                if st.button("Generate Value One-Pager"):
                    generator = StockOnePager(ticker)
                    doc = generator.generate_value_one_pager()
                    generator.save_one_pager(doc, 'value')
                    st.success("Value One-Pager Generated!")
            
            with col3:
                if st.button("Generate Core One-Pager"):
                    generator = StockOnePager(ticker)
                    doc = generator.generate_core_one_pager()
                    generator.save_one_pager(doc, 'core')
                    st.success("Core One-Pager Generated!")
            
        except Exception as e:
            st.error(f"Error processing ticker {ticker}: {str(e)}")

if __name__ == "__main__":
    main() 
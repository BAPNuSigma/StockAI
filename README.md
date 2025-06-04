# Stock One-Pager Generator

A comprehensive stock analysis tool that generates detailed one-pagers for any stock, featuring real-time data, technical analysis, and multiple valuation approaches.

## Requirements

- Python 3.11 (required)
- pip (Python package installer)
- Git

## Features

- **Real-time Data Integration**
  - Yahoo Finance for market data and news
  - Alpaca for real-time trading data
  - Financial Modeling Prep for financial statements
  - Tiingo for historical data

- **Technical Analysis**
  - Moving Averages (SMA, EMA)
  - Momentum Indicators (RSI, MACD, Stochastic)
  - Volatility Indicators (Bollinger Bands, ATR)
  - Volume Indicators (OBV, Accumulation/Distribution)
  - Trend Indicators (ADX, CCI, MFI)

- **One-Pager Generation**
  - Growth-focused analysis
  - Value-focused analysis
  - Core analysis
  - Customizable templates
  - PDF export capability

- **Interactive Dashboard**
  - Real-time price charts
  - Technical indicator visualization
  - News feed
  - Key metrics display
  - Ownership information

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/StockAI.git
cd StockAI
```

2. Create and activate a virtual environment with Python 3.11:
```bash
# Windows
python3.11 -m venv .venv
.venv\Scripts\activate

# Linux/MacOS
python3.11 -m venv .venv
source .venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Install TA-Lib (required for technical analysis):

For Windows:
- Download the appropriate wheel file from: https://www.lfd.uci.edu/~gohlke/pythonlibs/#ta-lib
- Install using pip:
```bash
pip install TA_Lib‑0.4.28‑cp39‑cp39‑win_amd64.whl
```

For Linux:
```bash
sudo apt-get install ta-lib
pip install TA-Lib
```

For macOS:
```bash
brew install ta-lib
pip install TA-Lib
```

5. Create a `.env` file in the project root with your API keys:
```
ALPACA_API_KEY=your_alpaca_api_key_here
ALPACA_SECRET_KEY=your_alpaca_secret_key_here
TIINGO_API_KEY=your_tiingo_api_key_here
FMP_API_KEY=your_financial_modeling_prep_api_key_here
OPENAI_API_KEY=your_openai_api_key_here
```

## Troubleshooting

### Common Installation Issues

1. **Python Version Compatibility**
   - This project requires Python 3.11
   - If you're using a different version, you may encounter compatibility issues
   - Solution: Install Python 3.11 and create a new virtual environment
   ```bash
   # Check your Python version
   python --version
   
   # If not 3.11.x, install Python 3.11 from:
   # Windows: https://www.python.org/downloads/release/python-3110/
   # Linux: Use your distribution's package manager
   # macOS: brew install python@3.11
   ```

2. **TA-Lib Installation Issues**
   - Windows: Make sure to download the correct wheel file matching your Python version
   - Linux: If apt-get fails, try:
     ```bash
     wget http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz
     tar -xzf ta-lib-0.4.0-src.tar.gz
     cd ta-lib/
     ./configure --prefix=/usr
     make
     sudo make install
     ```
   - macOS: If brew fails, try:
     ```bash
     brew update
     brew install ta-lib
     ```

3. **Pandas Installation Issues**
   - If you encounter build errors, try:
     ```bash
     pip install --upgrade pip
     pip install wheel
     pip install pandas
     ```

4. **Virtual Environment Issues**
   - If activation fails, try:
     ```bash
     # Windows
     python -m venv .venv --clear
     # Linux/MacOS
     python3 -m venv .venv --clear
     ```

5. **API Key Issues**
   - Ensure all API keys are correctly set in the `.env` file
   - Check for any typos or extra spaces
   - Verify API key permissions and quotas

### Running the Application

If you encounter issues running the application:

1. **Streamlit Issues**
   ```bash
   # Clear Streamlit cache
   streamlit cache clear
   ```

2. **Data Fetching Issues**
   - Check your internet connection
   - Verify API rate limits
   - Ensure all API keys are valid

3. **Chart Display Issues**
   - Clear browser cache
   - Try a different browser
   - Check if JavaScript is enabled

## Usage

1. Start the application:
```bash
streamlit run app.py
```

2. Enter a stock ticker in the input field

3. View the comprehensive analysis:
   - Company overview
   - Real-time metrics
   - Technical indicators
   - News feed
   - Ownership information

4. Generate one-pagers:
   - Click on the desired one-pager type (Growth, Value, or Core)
   - The document will be saved in the current directory

## Project Structure

```
StockAI/
├── app.py                 # Main Streamlit application
├── enhanced_data_fetcher.py  # Data fetching and processing
├── technical_analysis.py  # Technical analysis calculations
├── stock_one_pager.py     # One-pager generation
├── requirements.txt       # Project dependencies
└── .env                  # API keys (not in version control)
```

## API Keys Required

- [Alpaca](https://alpaca.markets/) - Real-time market data
- [Tiingo](https://api.tiingo.com/) - Historical data
- [Financial Modeling Prep](https://financialmodelingprep.com/) - Financial statements
- [OpenAI](https://openai.com/) - AI-powered analysis

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Yahoo Finance for market data
- Alpaca for real-time trading data
- Financial Modeling Prep for financial statements
- Tiingo for historical data
- TA-Lib for technical analysis calculations 
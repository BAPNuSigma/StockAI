import pandas as pd
import numpy as np
from ta.trend import SMAIndicator, EMAIndicator, MACD, ADXIndicator, CCIIndicator
from ta.momentum import RSIIndicator, StochasticOscillator
from ta.volatility import BollingerBands, AverageTrueRange
from ta.volume import OnBalanceVolumeIndicator, AccDistIndexIndicator

class TechnicalAnalyzer:
    def __init__(self, data):
        """
        Initialize with historical price data
        data: DataFrame with columns ['Open', 'High', 'Low', 'Close', 'Volume']
        """
        self.data = data
        self.calculate_indicators()

    def calculate_indicators(self):
        """Calculate all technical indicators"""
        # Moving Averages
        self.calculate_moving_averages()
        
        # Momentum Indicators
        self.calculate_momentum_indicators()
        
        # Volatility Indicators
        self.calculate_volatility_indicators()
        
        # Volume Indicators
        self.calculate_volume_indicators()
        
        # Trend Indicators
        self.calculate_trend_indicators()

    def calculate_moving_averages(self):
        """Calculate various moving averages"""
        try:
            # Simple Moving Averages
            self.data['SMA_20'] = SMAIndicator(close=self.data['Close'], window=20).sma_indicator()
            self.data['SMA_50'] = SMAIndicator(close=self.data['Close'], window=50).sma_indicator()
            self.data['SMA_200'] = SMAIndicator(close=self.data['Close'], window=200).sma_indicator()
            
            # Exponential Moving Averages
            self.data['EMA_20'] = EMAIndicator(close=self.data['Close'], window=20).ema_indicator()
            self.data['EMA_50'] = EMAIndicator(close=self.data['Close'], window=50).ema_indicator()
            self.data['EMA_200'] = EMAIndicator(close=self.data['Close'], window=200).ema_indicator()
        except Exception as e:
            print(f"Error calculating moving averages: {str(e)}")

    def calculate_momentum_indicators(self):
        """Calculate momentum indicators"""
        try:
            # RSI
            self.data['RSI'] = RSIIndicator(close=self.data['Close']).rsi()
            
            # MACD
            macd = MACD(close=self.data['Close'])
            self.data['MACD'] = macd.macd()
            self.data['MACD_Signal'] = macd.macd_signal()
            self.data['MACD_Hist'] = macd.macd_diff()
            
            # Stochastic Oscillator
            stoch = StochasticOscillator(high=self.data['High'], low=self.data['Low'], close=self.data['Close'])
            self.data['Stoch_K'] = stoch.stoch()
            self.data['Stoch_D'] = stoch.stoch_signal()
        except Exception as e:
            print(f"Error calculating momentum indicators: {str(e)}")

    def calculate_volatility_indicators(self):
        """Calculate volatility indicators"""
        try:
            # Bollinger Bands
            bb = BollingerBands(close=self.data['Close'])
            self.data['BB_Upper'] = bb.bollinger_hband()
            self.data['BB_Middle'] = bb.bollinger_mavg()
            self.data['BB_Lower'] = bb.bollinger_lband()
            
            # Average True Range
            self.data['ATR'] = AverageTrueRange(high=self.data['High'], low=self.data['Low'], close=self.data['Close']).average_true_range()
        except Exception as e:
            print(f"Error calculating volatility indicators: {str(e)}")

    def calculate_volume_indicators(self):
        """Calculate volume indicators"""
        try:
            # On Balance Volume
            self.data['OBV'] = OnBalanceVolumeIndicator(close=self.data['Close'], volume=self.data['Volume']).on_balance_volume()
            
            # Accumulation/Distribution Index
            self.data['ADI'] = AccDistIndexIndicator(high=self.data['High'], low=self.data['Low'], close=self.data['Close'], volume=self.data['Volume']).acc_dist_index()
        except Exception as e:
            print(f"Error calculating volume indicators: {str(e)}")

    def calculate_trend_indicators(self):
        """Calculate trend indicators"""
        try:
            # Average Directional Index
            self.data['ADX'] = ADXIndicator(high=self.data['High'], low=self.data['Low'], close=self.data['Close']).adx()
            
            # Commodity Channel Index
            self.data['CCI'] = CCIIndicator(high=self.data['High'], low=self.data['Low'], close=self.data['Close']).cci()
        except Exception as e:
            print(f"Error calculating trend indicators: {str(e)}")

    def get_technical_signals(self):
        """Generate technical analysis signals"""
        signals = {
            'Moving Averages': self._get_ma_signals(),
            'RSI': self._get_rsi_signals(),
            'MACD': self._get_macd_signals(),
            'Bollinger Bands': self._get_bb_signals(),
            'Volume': self._get_volume_signals(),
            'Trend': self._get_trend_signals()
        }
        return signals

    def _get_ma_signals(self):
        """Get moving average signals"""
        try:
            current_price = self.data['Close'].iloc[-1]
            signals = []
            
            # Check SMA crossovers
            if self.data['SMA_20'].iloc[-1] > self.data['SMA_50'].iloc[-1]:
                signals.append("SMA 20 crossed above SMA 50 (Bullish)")
            elif self.data['SMA_20'].iloc[-1] < self.data['SMA_50'].iloc[-1]:
                signals.append("SMA 20 crossed below SMA 50 (Bearish)")
            
            # Check price vs SMA 200
            if current_price > self.data['SMA_200'].iloc[-1]:
                signals.append("Price above SMA 200 (Long-term Bullish)")
            else:
                signals.append("Price below SMA 200 (Long-term Bearish)")
            
            return signals
        except Exception as e:
            print(f"Error getting MA signals: {str(e)}")
            return []

    def _get_rsi_signals(self):
        """Get RSI signals"""
        try:
            current_rsi = self.data['RSI'].iloc[-1]
            signals = []
            
            if current_rsi > 70:
                signals.append("RSI above 70 (Overbought)")
            elif current_rsi < 30:
                signals.append("RSI below 30 (Oversold)")
            
            return signals
        except Exception as e:
            print(f"Error getting RSI signals: {str(e)}")
            return []

    def _get_macd_signals(self):
        """Get MACD signals"""
        try:
            signals = []
            
            if self.data['MACD'].iloc[-1] > self.data['MACD_Signal'].iloc[-1]:
                signals.append("MACD above Signal Line (Bullish)")
            else:
                signals.append("MACD below Signal Line (Bearish)")
            
            return signals
        except Exception as e:
            print(f"Error getting MACD signals: {str(e)}")
            return []

    def _get_bb_signals(self):
        """Get Bollinger Bands signals"""
        try:
            current_price = self.data['Close'].iloc[-1]
            signals = []
            
            if current_price > self.data['BB_Upper'].iloc[-1]:
                signals.append("Price above Upper Bollinger Band (Overbought)")
            elif current_price < self.data['BB_Lower'].iloc[-1]:
                signals.append("Price below Lower Bollinger Band (Oversold)")
            
            return signals
        except Exception as e:
            print(f"Error getting BB signals: {str(e)}")
            return []

    def _get_volume_signals(self):
        """Get volume signals"""
        try:
            signals = []
            
            # Check OBV trend
            if self.data['OBV'].iloc[-1] > self.data['OBV'].iloc[-2]:
                signals.append("OBV increasing (Bullish Volume)")
            else:
                signals.append("OBV decreasing (Bearish Volume)")
            
            return signals
        except Exception as e:
            print(f"Error getting volume signals: {str(e)}")
            return []

    def _get_trend_signals(self):
        """Get trend signals"""
        try:
            signals = []
            
            # Check ADX strength
            if self.data['ADX'].iloc[-1] > 25:
                signals.append("Strong trend (ADX > 25)")
            else:
                signals.append("Weak trend (ADX < 25)")
            
            return signals
        except Exception as e:
            print(f"Error getting trend signals: {str(e)}")
            return [] 
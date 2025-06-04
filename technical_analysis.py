import pandas as pd
import numpy as np
from typing import Dict, Tuple
import talib

class TechnicalAnalyzer:
    def __init__(self, historical_data: pd.DataFrame):
        """
        Initialize the technical analyzer with historical price data.
        
        Args:
            historical_data (pd.DataFrame): Historical price data with OHLCV columns
        """
        self.data = historical_data
        self.close = self.data['close']
        self.high = self.data['high']
        self.low = self.data['low']
        self.volume = self.data['volume']
    
    def calculate_moving_averages(self) -> Dict:
        """Calculate various moving averages."""
        try:
            return {
                'sma_20': talib.SMA(self.close, timeperiod=20),
                'sma_50': talib.SMA(self.close, timeperiod=50),
                'sma_200': talib.SMA(self.close, timeperiod=200),
                'ema_12': talib.EMA(self.close, timeperiod=12),
                'ema_26': talib.EMA(self.close, timeperiod=26)
            }
        except Exception as e:
            print(f"Error calculating moving averages: {e}")
            return {}
    
    def calculate_momentum_indicators(self) -> Dict:
        """Calculate momentum indicators."""
        try:
            return {
                'rsi': talib.RSI(self.close, timeperiod=14),
                'macd': talib.MACD(self.close)[0],
                'macd_signal': talib.MACD(self.close)[1],
                'macd_hist': talib.MACD(self.close)[2],
                'stoch_k': talib.STOCH(self.high, self.low, self.close)[0],
                'stoch_d': talib.STOCH(self.high, self.low, self.close)[1]
            }
        except Exception as e:
            print(f"Error calculating momentum indicators: {e}")
            return {}
    
    def calculate_volatility_indicators(self) -> Dict:
        """Calculate volatility indicators."""
        try:
            return {
                'atr': talib.ATR(self.high, self.low, self.close, timeperiod=14),
                'natr': talib.NATR(self.high, self.low, self.close, timeperiod=14),
                'bollinger_upper': talib.BBANDS(self.close)[0],
                'bollinger_middle': talib.BBANDS(self.close)[1],
                'bollinger_lower': talib.BBANDS(self.close)[2]
            }
        except Exception as e:
            print(f"Error calculating volatility indicators: {e}")
            return {}
    
    def calculate_volume_indicators(self) -> Dict:
        """Calculate volume-based indicators."""
        try:
            return {
                'obv': talib.OBV(self.close, self.volume),
                'ad': talib.AD(self.high, self.low, self.close, self.volume),
                'adosc': talib.ADOSC(self.high, self.low, self.close, self.volume)
            }
        except Exception as e:
            print(f"Error calculating volume indicators: {e}")
            return {}
    
    def calculate_trend_indicators(self) -> Dict:
        """Calculate trend indicators."""
        try:
            return {
                'adx': talib.ADX(self.high, self.low, self.close, timeperiod=14),
                'cci': talib.CCI(self.high, self.low, self.close, timeperiod=14),
                'mfi': talib.MFI(self.high, self.low, self.close, self.volume, timeperiod=14)
            }
        except Exception as e:
            print(f"Error calculating trend indicators: {e}")
            return {}
    
    def get_all_indicators(self) -> Dict:
        """Calculate all technical indicators."""
        return {
            'moving_averages': self.calculate_moving_averages(),
            'momentum': self.calculate_momentum_indicators(),
            'volatility': self.calculate_volatility_indicators(),
            'volume': self.calculate_volume_indicators(),
            'trend': self.calculate_trend_indicators()
        }
    
    def get_signal_summary(self) -> Dict:
        """Generate a summary of technical signals."""
        indicators = self.get_all_indicators()
        current_price = self.close.iloc[-1]
        
        # Moving Average Signals
        ma_signals = {
            'above_sma_20': current_price > indicators['moving_averages']['sma_20'].iloc[-1],
            'above_sma_50': current_price > indicators['moving_averages']['sma_50'].iloc[-1],
            'above_sma_200': current_price > indicators['moving_averages']['sma_200'].iloc[-1],
            'golden_cross': (indicators['moving_averages']['sma_50'].iloc[-1] > 
                           indicators['moving_averages']['sma_200'].iloc[-1] and
                           indicators['moving_averages']['sma_50'].iloc[-2] <= 
                           indicators['moving_averages']['sma_200'].iloc[-2])
        }
        
        # RSI Signals
        rsi = indicators['momentum']['rsi'].iloc[-1]
        rsi_signals = {
            'overbought': rsi > 70,
            'oversold': rsi < 30,
            'rsi_value': rsi
        }
        
        # MACD Signals
        macd = indicators['momentum']['macd'].iloc[-1]
        macd_signal = indicators['momentum']['macd_signal'].iloc[-1]
        macd_signals = {
            'bullish_cross': (macd > macd_signal and 
                            indicators['momentum']['macd'].iloc[-2] <= 
                            indicators['momentum']['macd_signal'].iloc[-2]),
            'bearish_cross': (macd < macd_signal and 
                            indicators['momentum']['macd'].iloc[-2] >= 
                            indicators['momentum']['macd_signal'].iloc[-2])
        }
        
        # Bollinger Bands Signals
        bb_signals = {
            'above_upper': current_price > indicators['volatility']['bollinger_upper'].iloc[-1],
            'below_lower': current_price < indicators['volatility']['bollinger_lower'].iloc[-1],
            'squeeze': (indicators['volatility']['bollinger_upper'].iloc[-1] - 
                       indicators['volatility']['bollinger_lower'].iloc[-1]) < 
                       (indicators['volatility']['bollinger_upper'].iloc[-20] - 
                        indicators['volatility']['bollinger_lower'].iloc[-20])
        }
        
        return {
            'moving_averages': ma_signals,
            'rsi': rsi_signals,
            'macd': macd_signals,
            'bollinger_bands': bb_signals
        } 
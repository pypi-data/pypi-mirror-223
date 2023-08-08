# encoding: utf-8

import pandas as pd

def calc_ATR_WMA(data, period=14):
    """
    ATR with Weighted Moving Average (WMA)
    Usage: WMA gives more weight to the recent prices and as a result, it's more responsive to current price changes 
    than the SMA.  
    
    Strategy Implication: Useful in momentum strategies. A rising ATR in a strong uptrend might imply that the uptrend 
    is expected to continue. Similarly, a rising ATR in a downtrend might imply that the downtrend will persist.
    """

    # Calculate True Range
    high_low = data['High'] - data['Low']
    high_close = (data['High'] - data['Close'].shift(1)).abs()
    low_close = (data['Low'] - data['Close'].shift(1)).abs()

    ranges = pd.concat([high_low, high_close, low_close], axis=1)
    true_range = ranges.max(axis=1)

    # Compute WMA of True Range
    weights = list(range(1, period + 1))
    atr_wma = true_range.rolling(window=period).apply(lambda x: sum(weights * x[-period:]) / sum(weights), raw=True)

    return atr_wma

def calc_ATR_SMA(data, period=14):
    """
    ATR with Simple Moving Average (SMA)
    Usage: SMA is a straightforward method to smooth out price data. It provides a consistent measure of volatility 
    over a given period. 
    
    Strategy Implication: A sudden increase in the ATR value after a prolonged period of 
    low volatility could suggest the start of a new trend. Conversely, a sudden decrease might indicate a possible 
    consolidation phase.
    """

    # Calculate True Range
    high_low = data['High'] - data['Low']
    high_close = (data['High'] - data['Close'].shift(1)).abs()
    low_close = (data['Low'] - data['Close'].shift(1)).abs()

    ranges = pd.concat([high_low, high_close, low_close], axis=1)
    true_range = ranges.max(axis=1)

    # Use Simple Moving Average for ATR
    atr_sma = true_range.rolling(window=period).mean()

    return atr_sma

def calc_ATR_EMA(data, period=14):
    """
    ATR with Exponential Moving Average (EMA)
    Usage: EMA gives even more emphasis to the recent prices compared to WMA. As a result, it's highly responsive to 
    the latest market conditions.
    
    Strategy Implication: Best for traders who want to react quickly to volatility changes. An abrupt change in 
    the EMA-based ATR could be used as a signal for short-term traders to adjust their positions or for 
    entry/exit points.
    """

    # Calculate True Range
    high_low = data['High'] - data['Low']
    high_close = (data['High'] - data['Close'].shift(1)).abs()
    low_close = (data['Low'] - data['Close'].shift(1)).abs()

    ranges = pd.concat([high_low, high_close, low_close], axis=1)
    true_range = ranges.max(axis=1)

    # Compute EMA of True Range
    alpha = 2 / (period + 1)
    atr_ema = true_range.ewm(alpha=alpha, adjust=False).mean()

    return atr_ema


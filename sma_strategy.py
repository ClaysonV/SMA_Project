import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def run_sma_crossover(ticker='SPY', start_date='2015-01-01', short_window=50, long_window=200):
    """
    Runs a backtest for a simple moving average (SMA) crossover strategy.
    
    - 'ticker': The stock or ETF symbol to test.
    - 'start_date': The date to start downloading data.
    - 'short_window': The number of days for the short-term SMA.
    - 'long_window': The number of days for the long-term SMA.
    """
    
    print(f"Running SMA Crossover for {ticker}...")
    
    # 1. Get Data
    # Download historical price data from Yahoo Finance
    data = yf.download(ticker, start=start_date)
    if data.empty:
        print(f"No data found for {ticker}.")
        return

    # 2. Calculate Indicators (SMAs)
    # Create a new column for the short-term SMA
    data['SMA_short'] = data['Close'].rolling(window=short_window).mean()
    
    # Create a new column for the long-term SMA
    data['SMA_long'] = data['Close'].rolling(window=long_window).mean()
    
    # Remove the initial rows where SMAs are not yet calculated (NaN values)
    data.dropna(inplace=True)

    # 3. Generate Signals
    # Create a 'Signal' column: 1 if short SMA > long SMA (Buy), 0 otherwise (Sell/Neutral)
    data['Signal'] = np.where(data['SMA_short'] > data['SMA_long'], 1, 0)
    
    # Create a 'Position' column. We shift the signal by 1 day.
    # This prevents "look-ahead bias" — we can only trade on the *next day's*
    # price based on *today's* signal.
    data['Position'] = data['Signal'].shift(1)
    
    # Remove the first row that has a NaN for the shifted position
    data.dropna(inplace=True)

    # 4. Calculate Returns
    # Calculate daily market returns (this is the "buy and hold" strategy)
    data['Market_Returns'] = data['Close'].pct_change()
    
    # Calculate our strategy's daily returns
    # Multiply the market return by our position (1 if we hold, 0 if we're in cash)
    data['Strategy_Returns'] = data['Market_Returns'] * data['Position']

    # 5. Analyze Results
    # Calculate the cumulative returns for both strategies
    data['Cumulative_Market'] = (1 + data['Market_Returns']).cumprod()
    data['Cumulative_Strategy'] = (1 + data['Strategy_Returns']).cumprod()

    # Get the final total return
    total_market_return = data['Cumulative_Market'].iloc[-1]
    total_strategy_return = data['Cumulative_Strategy'].iloc[-1]
    
    print(f"\n--- Backtest Results ---")
    print(f"Buy & Hold Total Return: {total_market_return:.2%}")
    print(f"Strategy Total Return:   {total_strategy_return:.2%}")

    # 6. Plot the Results
    
    # Plot 1: Price, SMAs, and Trade Signals
    plt.figure(figsize=(14, 7))
    plt.plot(data['Close'], label='Price', alpha=0.8)
    plt.plot(data['SMA_short'], label=f'{short_window}-Day SMA', linestyle='--')
    plt.plot(data['SMA_long'], label=f'{long_window}-Day SMA', linestyle='--')

    # Find points where we enter a trade (position goes from 0 to 1)
    buy_signals = data[(data['Position'] == 1) & (data['Position'].shift(1) == 0)]
    # Find points where we exit a trade (position goes from 1 to 0)
    sell_signals = data[(data['Position'] == 0) & (data['Position'].shift(1) == 1)]

    plt.plot(buy_signals.index, data.loc[buy_signals.index]['Close'], '^', markersize=10, color='g', label='Buy Signal (Enter)')
    plt.plot(sell_signals.index, data.loc[sell_signals.index]['Close'], 'v', markersize=10, color='r', label='Sell Signal (Exit)')
    
    plt.title(f'{ticker} Price with SMA Crossover Signals')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.legend()
    plt.grid(True)
    plt.show()

    # Plot 2: Cumulative Returns (Equity Curve)
    plt.figure(figsize=(14, 7))
    plt.plot(data['Cumulative_Market'], label='Market (Buy & Hold)')
    plt.plot(data['Cumulative_Strategy'], label='Strategy')
    plt.title('Strategy Performance vs. Buy & Hold')
    plt.xlabel('Date')
    plt.ylabel('Cumulative Returns')
    plt.legend()
    plt.grid(True)
    plt.show()

# --- Run the backtest ---
if __name__ == "__main__":
    # You can change these parameters!
    run_sma_crossover(
        ticker='AAPL',       # Try 'MSFT', 'GOOGL', 'SPY', or 'BTC-USD'
        start_date='2018-01-01',
        short_window=40,
        long_window=100
    )
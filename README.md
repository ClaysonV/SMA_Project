#  Simple Moving Average Backtester

This project is a Python-based backtesting engine that implements the classic Simple Moving Average (SMA) Crossover strategy. It serves as the foundational "Capstone" and is my first major project, demonstrating the core mechanics of algorithmic trading: data ingestion, signal generation, and performance benchmarking.

It uses the classic **Simple Moving Average (SMA) Crossover**. The logic is pretty simple:
* **Buy Signal :** When the short-term (50-day) average price crosses *above* the long-term (200-day) average.
* **Sell Signal :** When the short-term average crosses *below* the long-term average.

## Features
* Automated Data Pipeline: Fetches historical OHLCV data directly from Yahoo Finance APIs.

* Vectorized Signal Logic: Uses numpy and pandas to calculate moving averages and identify crossover points without slow iteration loops.

* Performance Benchmarking: Automatically compares the strategy's cumulative returns against a passive "Buy & Hold" baseline.

* Visual Diagnostics: Generates dual-axis charts plotting price, SMAs, and entry/exit markers.

## Tech Stack
* Python
* pandas
* numpy
* yfinance
* matplotlib

## How to Run It

1.  Clone this repo.
2.  Set up a virtual environment:
    ```bash
    python -m venv venv
    ```
    Activate it:
    ```bash
    # On Windows
    .\venv\Scripts\activate
    
    # On Mac/Linux
    source venv/bin/activate
    ```
3.  Install the packages:
    ```bash
    pip install -r requirements.txt
    ```
4.  Just run the script
    ```bash
    python sma_strategy.py
    ```
5.  Two charts will pop up showing the trades and the final score.

## The Results (for AAPL)

So... did it actually work?

When I ran it on Apple stock (`AAPL`) from 2018, here's what I got:


* **My Strategy's Return:** 330.92%
* **"Buy & Hold" Return:** 598.11%

Key Takeaway: While the strategy was profitable, it failed to beat the market. This validates the Efficient Market Hypothesis in this specific context and highlights the limitations of using lagging indicators (Moving Averages) in high-momentum stocks like Apple. It serves as a baseline for developing more complex strategies in future phases.

Here are the charts my script generated:

### Strategy Signals
![Strategy Signals Chart](images/sma_signals_chart.png)

### Performance vs. Buy & Hold
![Strategy Performance Chart](images/strategy_returns_chart.png)

Feel free to open `sma_strategy.py` and change the ticker or the dates at the bottom to test it on your own.

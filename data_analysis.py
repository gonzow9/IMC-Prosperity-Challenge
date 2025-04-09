# import pandas as pd
# path = "round-1-island-data-bottle"
# trades_day0 = pd.read_csv(f"{path}/trades_round_1_day_0.csv")
# trades_day1 = pd.read_csv(f"{path}/trades_round_1_day_-1.csv")
# trades_day2 = pd.read_csv(f"{path}/trades_round_1_day_-2.csv")

# prices_day0 = pd.read_csv(f"{path}/prices_round_1_day_0.csv")
# prices_day1 = pd.read_csv(f"{path}/prices_round_1_day_-1.csv")
# prices_day2 = pd.read_csv(f"{path}/prices_round_1_day_-2.csv")

# print(trades_day0.columns)
# print(trades_day0.head())
# print(trades_day0.describe())

# print(prices_day0.columns)
# print(prices_day0.head())
# print(prices_day0.describe())

#!/usr/bin/env python3
"""
Script to load trades and prices data from CSV files for days 0, 1, 2,
parse them correctly (using sep=';'), and compute relevant metrics.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 1) Helper Functions to Load Data
def load_trades(day: int) -> pd.DataFrame:
    """
    Loads the trades data for a given day (0, 1, or 2) from a CSV.
    Parses with separator=';'.
    Returns a pandas DataFrame with columns:
      [timestamp, buyer, seller, symbol, currency, price, quantity]
    """
    path = "round-1-island-data-bottle"
    filename = f"{path}/trades_round_1_day_{day}.csv"
    df = pd.read_csv(filename, sep=';', engine='python')
    
    # If the header row isn't recognized automatically, rename columns manually:
    df.columns = ["timestamp", "buyer", "seller", "symbol", "currency", "price", "quantity"]
    
    # Convert numeric columns from string to float or int if needed:
    df["timestamp"] = pd.to_numeric(df["timestamp"], errors='coerce')
    df["price"]     = pd.to_numeric(df["price"], errors='coerce')
    df["quantity"]  = pd.to_numeric(df["quantity"], errors='coerce')
    
    # Optional: if timestamp is in seconds or ms, you could convert it to datetime:
    # df["timestamp"] = pd.to_datetime(df["timestamp"], unit='s')
    
    return df

def load_prices(day: int) -> pd.DataFrame:
    """
    Loads the prices data for a given day (0, 1, or 2) from a CSV.
    Parses with separator=';'.
    Returns a pandas DataFrame with columns:
      [day, timestamp, product,
       bid_price_1, bid_volume_1,
       bid_price_2, bid_volume_2,
       bid_price_3, bid_volume_3,
       ask_price_1, ask_volume_1,
       ask_price_2, ask_volume_2,
       ask_price_3, ask_volume_3,
       mid_price, profit_and_loss]
    """
    path = "round-1-island-data-bottle"
    filename = f"{path}/prices_round_1_day_{day}.csv"
    df = pd.read_csv(filename, sep=';', engine='python')
    
    # Manually assign column names if not auto-detected:
    df.columns = [
        "day", "timestamp", "product",
        "bid_price_1","bid_volume_1",
        "bid_price_2","bid_volume_2",
        "bid_price_3","bid_volume_3",
        "ask_price_1","ask_volume_1",
        "ask_price_2","ask_volume_2",
        "ask_price_3","ask_volume_3",
        "mid_price","profit_and_loss"
    ]
    
    # Convert to numeric types where appropriate:
    numeric_cols = [
        "day","timestamp","bid_price_1","bid_volume_1","bid_price_2","bid_volume_2",
        "bid_price_3","bid_volume_3","ask_price_1","ask_volume_1","ask_price_2",
        "ask_volume_2","ask_price_3","ask_volume_3","mid_price","profit_and_loss"
    ]
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    
    # Optional: Convert timestamp to datetime if desired
    # df["timestamp"] = pd.to_datetime(df["timestamp"], unit='s')
    
    return df

# -----------------------------------------------------------------------------
# 2) Analysis Functions
# -----------------------------------------------------------------------------

def analyze_trades(df_trades: pd.DataFrame) -> pd.DataFrame:
    """
    Given a DataFrame of trades, compute some summary metrics grouped by symbol:
      - Average trade price
      - Total volume
      - Standard deviation of price
      - Min and max trade price
    Returns a summary DataFrame.
    """
    grouped = df_trades.groupby("symbol").agg(
        avg_price = ("price", "mean"),
        total_volume = ("quantity", "sum"),
        std_price = ("price", "std"),
        min_price = ("price", "min"),
        max_price = ("price", "max")
    )
    return grouped

def analyze_prices(df_prices: pd.DataFrame) -> pd.DataFrame:
    """
    Given a DataFrame of prices, compute summary metrics grouped by product:
      - Average mid_price
      - Std dev mid_price
      - Min & max mid_price
      - Average bid-ask spread (ask_price_1 - bid_price_1)
    Returns a summary DataFrame.
    """
    # Create a 'spread' column using the top-of-book (ask_price_1 - bid_price_1)
    df_prices["spread"] = df_prices["ask_price_1"] - df_prices["bid_price_1"]
    
    grouped = df_prices.groupby("product").agg(
        avg_mid_price = ("mid_price", "mean"),
        std_mid_price = ("mid_price", "std"),
        min_mid_price = ("mid_price", "min"),
        max_mid_price = ("mid_price", "max"),
        avg_spread = ("spread", "mean")
    )
    return grouped

# -----------------------------------------------------------------------------
# 3) Main Execution
# -----------------------------------------------------------------------------

def main():
    # We’ll store daily data in dictionaries
    trades_data = {}
    prices_data = {}
    
    # Load and analyze each day
    for day in [0, 1, 2]:
        print(f"\n=== DAY {day} ===")
        
        # Load trades
        df_trades = load_trades(day)
        # Summaries
        trade_summary = analyze_trades(df_trades)
        
        print("\nTrade Summary (Grouped by Symbol):")
        print(trade_summary)
        
        # Load prices
        df_prices = load_prices(day)
        # Summaries
        price_summary = analyze_prices(df_prices)
        
        print("\nPrices Summary (Grouped by Product):")
        print(price_summary)
        
        # Store the full data if we want to do more analysis later
        trades_data[day] = df_trades
        prices_data[day] = df_prices
        
        # Example: If you want to do a quick plot of mid_price for each product
        # (just as a demonstration; normally might do per product)
        # We'll pick one product, e.g. SQUID_INK:
        ink_df = df_prices[df_prices["product"] == "SQUID_INK"].copy()
        if not ink_df.empty:
            plt.figure(figsize=(8,4))
            plt.title(f"SQUID_INK Mid Price - Day {day}")
            plt.plot(ink_df["timestamp"], ink_df["mid_price"], label="mid_price")
            plt.xlabel("Timestamp")
            plt.ylabel("Mid Price")
            plt.legend()
            plt.tight_layout()
            # Uncomment if you want to show or save
            # plt.show()
            # plt.savefig(f"squid_ink_day{day}.png")
    
    # End of main loop
    print("\nAll done! You can further analyze 'trades_data' and 'prices_data' as needed.")

if __name__ == "__main__":
    main()
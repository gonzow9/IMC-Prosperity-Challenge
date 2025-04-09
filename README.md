# IMC-Prosperity-Challenge
## Go Bokke


# IMC Prosperity Trading Challenge - Round 1 Solution

This repository contains code for analysing sample data and executing a trading algorithm for Round 1 of the IMC Prosperity Trading Challenge. The solution includes two main components:
1. `data_analysis.py`: A script to load and analyze historical trade and price data for Rainforest Resin, Kelp, and Squid Ink.
2. `trader.py`: A trading algorithm implemented as a `Trader` class to trade the three products in the challenge simulation.

## Prerequisites

- **Python 3.7+**: Ensure Python is installed on your system.
- **Required Libraries**: Install these via pip:
  ```bash
  pip install pandas numpy matplotlib
  ```
- **Data Files**: Place the Round 1 sample data files in a subdirectory named `round-1-island-data-bottle`. Expected files:
  - `trades_round_1_day_0.csv`
  - `trades_round_1_day_1.csv`
  - `trades_round_1_day_2.csv`
  - `prices_round_1_day_0.csv`
  - `prices_round_1_day_1.csv`
  - `prices_round_1_day_2.csv`

## Directory Structure

```
IMC-Prosperity-Challenge/
│
├── round-1-island-data-bottle/
│   ├── trades_round_1_day_0.csv
│   ├── trades_round_1_day_1.csv
│   ├── trades_round_1_day_2.csv
│   ├── prices_round_1_day_0.csv
│   ├── prices_round_1_day_1.csv
│   └── prices_round_1_day_2.csv
│
├── data_analysis.py
├── trader.py
└── README.md
```

## Running the Code

### 1. Data Analysis (`data_analysis.py`)

This script loads trade and price data for days 0, 1, and 2, computes summary statistics (e.g., average prices, volatility, spreads), and optionally generates plots for Squid Ink’s mid-price.

#### How to Run
1. **Navigate to the project directory**:
   ```bash
   cd your_project
   ```
2. **Execute the script**:
   ```bash
   python3 data_analysis.py
   ```
3. **Output**:
   - Terminal: Prints trade and price summaries for each day (e.g., average mid-price, standard deviation).
   - Files: Saves PNG plots (`squid_ink_day0.png`, etc.) (currenlty commented out) in the current directory if `plt.savefig()` is uncommented.

#### Notes
- Ensure the `round-1-island-data-bottle` directory is present with all six CSV files.
- The script uses a semicolon (`;`) as the delimiter for CSV parsing.
- Uncomment `plt.show()` in the script if you want to display plots interactively instead of saving them.

### 2. Trading Algorithm (`trader.py`)

This script implements the `Trader` class required by the challenge. It uses market-making for Rainforest Resin, trend-following for Kelp, and mean-reversion for Squid Ink, leveraging insights from the data analysis.

#### How to Run
- **Local Testing**: The `trader.py` file isn’t designed to run standalone since it interacts with the challenge’s simulation environment via the `TradingState` object. To test locally:
  1. Simulate a `TradingState` object with mock data (e.g., order depths, positions) and call `Trader().run(state)`.
  2. Example mock setup (add this to `trader.py` for testing):
     ```python
     from datamodel import OrderDepth, TradingState, Order

     if __name__ == "__main__":
         mock_depth = {
             "RAINFOREST_RESIN": OrderDepth(buy_orders={9998: 10}, sell_orders={10002: 10}),
             "KELP": OrderDepth(buy_orders={2010: 10}, sell_orders={2015: 10}),
             "SQUID_INK": OrderDepth(buy_orders={2000: 10}, sell_orders={2050: 10})
         }
         state = TradingState("", 0, {}, mock_depth, {}, {}, {}, None)
         trader = Trader()
         for _ in range(20):  # Simulate iterations
             result, _, new_data = trader.run(state)
             state.traderData = new_data
             print(result)
     ```
  3. Run:
     ```bash
     python3 trader.py
     ```
- **Submission**: Upload `trader.py` to the IMC Prosperity platform as-is. The simulation will call `Trader.run()` with real `TradingState` objects.

#### Notes
- The algorithm uses `traderData` to persist price histories across iterations.
- Position limits (±50) are enforced per product.
- No external dependencies beyond the `datamodel` module (assumed provided by the challenge).

## Usage Tips

1. **Analyze First**: Run `data_analysis.py` to understand the data before tweaking `trader.py`. Adjust parameters (e.g., MA periods, z-score thresholds) based on the output.
2. **Test Iteratively**: Submit `trader.py` to the platform early since Round 1 provides instant results. Refine based on performance feedback.
3. **File Integrity**: Verify CSV files match the expected format (semicolon-separated, correct column names).

## Contact

For questions, reach out to SammyBoi

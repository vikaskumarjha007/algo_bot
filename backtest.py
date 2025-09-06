import pandas as pd
from strategies.sma_strategy import SMA_Bot

# Define SMA ranges
short_windows = [5, 10, 20]
long_windows = [20, 50, 100]

# Store all results
results = []

for short_w in short_windows:
    for long_w in long_windows:
        if short_w >= long_w:
            continue  # skip invalid pairs
        
        bot = SMA_Bot("/Users/vikasjha/Desktop/algo_bot/data/historical_data.csv", short_window=short_w, long_window=long_w)
        bot.generate_signals()
        bot.run_trades()
        perf = bot.performance()
        
        results.append({
            "short_window": short_w,
            "long_window": long_w,
            "Total Return (%)": perf.get("total_return", 0),
            "Num Trades": perf.get("num_trades", 0),
            "Sharpe Ratio": perf.get("sharpe", 0),
            "Max Drawdown (%)": perf.get("max_drawdown", 0)
        })

# Convert results to DataFrame
df_results = pd.DataFrame(results)

# Save to CSV
df_results.to_csv("logs/backtest_results.csv", index=False)

# Print top 5 by Sharpe
print(df_results.sort_values(by="Sharpe Ratio", ascending=False).head())
# Sort results by Sharpe ratio descending
best_sma = df_results.sort_values(by="Sharpe Ratio", ascending=False).iloc[0]

print("\nBest SMA Parameters based on Sharpe Ratio:")
print(f"Short Window: {best_sma['short_window']}")
print(f"Long Window: {best_sma['long_window']}")
print(f"Sharpe Ratio: {best_sma['Sharpe Ratio']}")
print(f"Total Return (%): {best_sma['Total Return (%)']}")

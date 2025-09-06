from strategies.sma_strategy import SMA_Bot

if __name__ == "__main__":
    # Initialize SMA Bot
    bot = SMA_Bot("historical_data.csv", short_window=5, long_window=20, capital=100000)
    
    # Generate signals, run trades, save log
    bot.generate_signals()
    bot.run_trades()
    bot.save_log()
    
from strategies.sma_strategy import SMA_Bot

if __name__ == "__main__":
    bot = SMA_Bot("historical_data.csv", short_window=5, long_window=20, capital=100000)
    bot.generate_signals()
    bot.run_trades()
    bot.save_log()
    bot.plot_trades("plots/sma_trades.png")  # optional: save chart

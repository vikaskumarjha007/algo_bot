import pandas as pd
import matplotlib.pyplot as plt

class SMA_Bot:
    def __init__(self, data_file, short_window=5, long_window=20, capital=100000):
        self.data = pd.read_csv(data_file)
        self.data['Date'] = pd.to_datetime(self.data['Date'])
        self.short_window = short_window
        self.long_window = long_window
        self.capital = capital
        self.trade_log = []
        self.position = None
        self.entry_price = None

    def generate_signals(self):
        self.data['SMA_Short'] = self.data['Close'].rolling(window=self.short_window).mean()
        self.data['SMA_Long'] = self.data['Close'].rolling(window=self.long_window).mean()
        self.data['Signal'] = 0
        self.data.loc[self.data['SMA_Short'] > self.data['SMA_Long'], 'Signal'] = 1
        self.data.loc[self.data['SMA_Short'] < self.data['SMA_Long'], 'Signal'] = -1

    def run_trades(self):
        self.position = None
        self.entry_price = None
        for _, row in self.data.iterrows():
            if row['Signal'] == 1 and self.position != 'long':
                self.position = 'long'
                self.entry_price = row['Close']
                self.trade_log.append({
                    "Date": row['Date'],
                    "Action": "Buy",
                    "Price": row['Close'],
                    "PnL": 0
                })
            elif row['Signal'] == -1 and self.position == 'long':
                pnl = row['Close'] - self.entry_price
                self.trade_log.append({
                    "Date": row['Date'],
                    "Action": "Sell",
                    "Price": row['Close'],
                    "PnL": pnl
                })
                self.position = None
                self.entry_price = None

    def save_log(self, filename="logs/trade_log.csv"):
        pd.DataFrame(self.trade_log).to_csv(filename, index=False)
        print(f"Trades saved to {filename}")

    def plot_trades(self, filename=None):
        plt.figure(figsize=(14,7))
        plt.plot(self.data['Date'], self.data['Close'], label='Close Price', color='blue')
        plt.plot(self.data['Date'], self.data['SMA_Short'], label=f'SMA {self.short_window}', color='orange')
        plt.plot(self.data['Date'], self.data['SMA_Long'], label=f'SMA {self.long_window}', color='green')

        for trade in self.trade_log:
            if trade['Action'] == 'Buy':
                plt.scatter(trade['Date'], trade['Price'], marker='^', color='green', s=100, label='Buy')
            elif trade['Action'] == 'Sell':
                plt.scatter(trade['Date'], trade['Price'], marker='v', color='red', s=100, label='Sell')

        plt.title('SMA Crossover Strategy')
        plt.xlabel('Date')
        plt.ylabel('Price')
        plt.legend()
        plt.grid(True)

        if filename:
            plt.savefig(filename)
            print(f"Plot saved as {filename}")

    def performance(self):
        if not self.trade_log:
            return {"total_return": 0, "num_trades": 0}
        trades = pd.DataFrame(self.trade_log)
        total_pnl = trades["PnL"].sum()
        total_return = (total_pnl / self.capital) * 100
        num_trades = len(trades[trades["Action"] == "Sell"])
        return {
            "total_return": round(total_return, 2),
            "num_trades": num_trades
        }


import pandas as pd

class SMA_Bot:
    def __init__(self, csv_file, short_window=5, long_window=20, capital=100000):
        self.data = pd.read_csv(csv_file)
        self.data['Date'] = pd.to_datetime(self.data['Date'])
        self.short_window = short_window
        self.long_window = long_window
        self.capital = capital
        self.position = 0
        self.trade_log = []

    def generate_signals(self):
        self.data['SMA_Short'] = self.data['Close'].rolling(self.short_window).mean()
        self.data['SMA_Long'] = self.data['Close'].rolling(self.long_window).mean()
        self.data['Signal'] = 0
        self.data['Signal'][self.long_window:] = [
            1 if self.data['SMA_Short'][i] > self.data['SMA_Long'][i] else -1
            for i in range(self.long_window, len(self.data))
        ]

    def run_trades(self):
        for i in range(len(self.data)):
            if self.data['Signal'][i] == 1 and self.position == 0:
                self.position = self.capital / self.data['Close'][i]
                self.trade_log.append({
                    'Date': self.data['Date'][i],
                    'Action': 'Buy',
                    'Price': self.data['Close'][i],
                    'Capital': self.capital
                })
            elif self.data['Signal'][i] == -1 and self.position > 0:
                self.capital = self.position * self.data['Close'][i]
                self.position = 0
                self.trade_log.append({
                    'Date': self.data['Date'][i],
                    'Action': 'Sell',
                    'Price': self.data['Close'][i],
                    'Capital': self.capital
                })

    def save_log(self, filename="trade_log.csv"):
        pd.DataFrame(self.trade_log).to_csv(filename, index=False)
        print(f"Trades logged to {filename}")

import matplotlib.pyplot as plt

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

    def generate_signals(self):
        self.data['SMA_Short'] = self.data['Close'].rolling(window=self.short_window).mean()
        self.data['SMA_Long'] = self.data['Close'].rolling(window=self.long_window).mean()
        self.data['Signal'] = 0
        self.data.loc[self.data['SMA_Short'] > self.data['SMA_Long'], 'Signal'] = 1
        self.data.loc[self.data['SMA_Short'] < self.data['SMA_Long'], 'Signal'] = -1

    def run_trades(self):
        position = None
        for _, row in self.data.iterrows():
            if row['Signal'] == 1 and position != 'long':
                self.trade_log.append({"Date": row['Date'], "Action": "Buy", "Price": row['Close']})
                position = 'long'
            elif row['Signal'] == -1 and position != 'short':
                self.trade_log.append({"Date": row['Date'], "Action": "Sell", "Price": row['Close']})
                position = 'short'

    def save_log(self, filename="logs/trade_log.csv"):
        pd.DataFrame(self.trade_log).to_csv(filename, index=False)
        print(f"Trades saved to {filename}")

    # 👇 Add this method at the end
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

        plt.show()


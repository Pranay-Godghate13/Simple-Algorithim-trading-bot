import matplotlib.pyplot as plt

def plot_results(data):
    plt.figure(figsize=(12, 6))
    plt.plot(data['Date'], data['Close'], label='Close Price', color='blue')
    plt.plot(data['Date'], data['SMA_Short'], label='Short-Term SMA', color='green')
    plt.plot(data['Date'], data['SMA_Long'], label='Long-Term SMA', color='red')
    plt.legend()
    plt.title('Moving Average Crossover Strategy')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.show()

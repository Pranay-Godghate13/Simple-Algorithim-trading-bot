import os
import matplotlib
import matplotlib.pyplot as plt

matplotlib.use('Agg')  # Use non-interactive backend

def create_signal_plot(data_with_signals, save_path):
    
    plt.figure(figsize=(14, 8))
    plt.plot(data_with_signals.index, data_with_signals['Close'], label='Close Price', color='blue')
    plt.plot(data_with_signals.index, data_with_signals['SMA_Short'], label='Short SMA (10 days)', color='green')
    plt.plot(data_with_signals.index, data_with_signals['SMA_Long'], label='Long SMA (50 days)', color='red')

    plt.scatter(
        data_with_signals.index[data_with_signals['Signal'] == 1],
        data_with_signals.loc[data_with_signals['Signal'] == 1, 'Close'],
        label='Buy Signal', marker='^', color='lime', s=100
    )
    plt.scatter(
        data_with_signals.index[data_with_signals['Signal'] == -1],
        data_with_signals.loc[data_with_signals['Signal'] == -1, 'Close'],
        label='Sell Signal', marker='v', color='orange', s=100
    )

    # Explicitly set the x-axis to cover the entire date range
    plt.xlim(data_with_signals.index.min(), data_with_signals.index.max())

    plt.title('Trading Strategy with Signals', fontsize=16)
    plt.xlabel('Date', fontsize=12)
    plt.ylabel('Price (USD)', fontsize=12)
    plt.legend(fontsize=10)
    plt.grid()
    plt.tight_layout()

    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    plt.savefig(save_path)
    plt.close()  # Close the figure to free memory

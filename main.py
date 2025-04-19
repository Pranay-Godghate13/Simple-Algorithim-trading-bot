from app.fetch_data import fetch_stock_data
from app.preprocess_data import preprocess_data
from app.strategy import calculate_moving_averages, generate_signals
from app.backtest import backtest_strategy
from app.visualization import plot_results

if __name__ == "__main__":
    
    ticker = "AAPL"  
    start_date = "2020-01-01"
    end_date = "2023-01-01"
    short_window = 10
    long_window = 50

    
    print("Fetching stock data...")
    data = fetch_stock_data(ticker, start_date, end_date)
    
    print("Preprocessing the data, cleaning and removing NAN value")
    data=preprocess_data(data)

    print("Calculating moving averages...")
    data = calculate_moving_averages(data, short_window, long_window)
    
    print("Generating trading signals...")
    data = generate_signals(data)


    print("Backtesting strategy...")
    final_capital = backtest_strategy(data,10000)
    print(f"Final Portfolio Value: ${final_capital:.2f}")

    
    plot_results(data)

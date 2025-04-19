from flask import Flask, render_template, request
from fetch_data import fetch_stock_data
from preprocess_data import preprocess_data
from strategy import calculate_moving_averages, generate_signals
from backtest import backtest_strategy
import os
import matplotlib
import matplotlib.pyplot as plt

matplotlib.use('Agg')  

app = Flask(__name__)
app.static_folder = 'static'

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        ticker = request.form["ticker"]
        start_date = request.form["start_date"]
        end_date = request.form["end_date"]
        capital = request.form["capital"]

        try:
           
            data = fetch_stock_data(ticker, start_date, end_date)
            data = preprocess_data(data)
            data.set_index('Date', inplace=True)

            if data.empty:
                raise ValueError("No data available for the given inputs.")

         
            data = calculate_moving_averages(data)
            data_with_signals = generate_signals(data)
            data_with_signals.dropna(subset=['SMA_Short', 'SMA_Long'], inplace=True)

            
            final_portfolio_value = backtest_strategy(data_with_signals, int(capital))

            
            signal_plot_path = "static/results/signal_plot.png"
            os.makedirs("static/results", exist_ok=True)

            plt.figure(figsize=(12, 6))
            plt.plot(data_with_signals.index, data_with_signals['Close'], label='Close Price')
            plt.plot(data_with_signals.index, data_with_signals['SMA_Short'], label='Short SMA')
            plt.plot(data_with_signals.index, data_with_signals['SMA_Long'], label='Long SMA')
            plt.scatter(data_with_signals.index[data_with_signals['Signal'] == 1],
                        data_with_signals.loc[data_with_signals['Signal'] == 1, 'Close'],
                        label='Buy Signal', marker='^', color='green')
            plt.scatter(data_with_signals.index[data_with_signals['Signal'] == -1],
                        data_with_signals.loc[data_with_signals['Signal'] == -1, 'Close'],
                        label='Sell Signal', marker='v', color='red')
            plt.title('Trading Strategy Signals')
            plt.xlabel('Date')
            plt.ylabel('Price')
            plt.legend()
            plt.grid()
            plt.savefig(signal_plot_path)

            return render_template(
                "index.html",
                data=data_with_signals.to_html(),
                final_portfolio_value=final_portfolio_value,
                plot_path=signal_plot_path,
            )

        except ValueError as e:
            return render_template("index.html", error=str(e))
        except Exception as e:
            return render_template("index.html", error=f"An unexpected error occurred: {e}")

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)

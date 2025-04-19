from flask import Flask, render_template, request
from app.fetch_data import fetch_stock_data
from app.preprocess_data import preprocess_data
from app.strategy import calculate_moving_averages, generate_signals
from app.backtest import backtest_strategy
from app.visualization import create_signal_plot
import os

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
            # Fetch, preprocess, and calculate signals
            data = fetch_stock_data(ticker, start_date, end_date)
            data = preprocess_data(data)
            data.set_index('Date', inplace=True)

            if data.empty:
                raise ValueError("No data available for the given inputs.")

            data = calculate_moving_averages(data)
            data_with_signals = generate_signals(data)
            data_with_signals.dropna(subset=['SMA_Short', 'SMA_Long'], inplace=True)

            # Backtest the strategy
            final_portfolio_value = backtest_strategy(data_with_signals, int(capital))

            # Visualization
            signal_plot_path = os.path.join(app.static_folder, "results", "signal_plot.png")
            os.makedirs(os.path.dirname(signal_plot_path), exist_ok=True)
            create_signal_plot(data_with_signals, signal_plot_path)

            # Relative URL for the plot
            plot_url = "/static/results/signal_plot.png"

            # Render the template with data
            return render_template(
                "index.html",
                data=data_with_signals.to_html(),
                final_portfolio_value=final_portfolio_value,
                plot_path=plot_url,
            )

        except ValueError as e:
            return render_template("index.html", error=str(e))
        except Exception as e:
            return render_template("index.html", error=f"An unexpected error occurred: {e}")

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)

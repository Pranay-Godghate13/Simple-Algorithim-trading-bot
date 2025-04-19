import yfinance as yf
def fetch_stock_data(ticker,start_date,end_date):
    data=yf.download(ticker,start=start_date,end=end_date)
    data.reset_index(inplace=True)
    return data

#print(fetch_stock_data("AAPL","2020-01-01","2023-01-01").head()) 
import yfinance as yf
def fetch_stock_data(ticker,start_date,end_date):
    data=yf.download(ticker,start=start_date,end=end_date)
    data.reset_index(inplace=True)
    return data
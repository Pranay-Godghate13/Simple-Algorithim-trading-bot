import pandas as pd

def preprocess_data(df):
    
    # Setting column names
    if len(df.columns) == 7:  # Expecting ['Date', 'Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume']
        df.columns = ['Date', 'Adj Close', 'Close', 'High', 'Low', 'Open', 'Volume']
    elif len(df.columns) == 6:  # Sometimes 'Adj Close' is not present
        df.columns = ['Date', 'Close', 'High', 'Low', 'Open', 'Volume']
    else:
        raise KeyError(f"Unexpected DataFrame structure: {df.columns}")

    # Code to check if there is any missing column
    missing_columns = [col for col in ['Open', 'Close', 'Low', 'High'] if col not in df.columns]
    if missing_columns:
        raise KeyError(f"Missing columns in DataFrame: {missing_columns}")

    # Convert row to numeric data and remove any row with NAA value.
    df[['Open', 'Close', 'Low', 'High']] = df[['Open', 'Close', 'Low', 'High']].apply(pd.to_numeric, errors="coerce")
    df.dropna(subset=['Open', 'Close', 'Low', 'High'], inplace=True)
    
    return df

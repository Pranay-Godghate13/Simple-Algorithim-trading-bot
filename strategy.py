def calculate_moving_average(data,short_window=10,long_window=50):
    data['SMA_Short']=data['Close'].rolling(window=short_window).mean()
    data['SMA_Long']=data['Close'].rolling(window=long_window).mean()
    return data

def generate_signals(data):
    data['Signal']=0
    data.loc[data['SMA_Short']>data['SMA_Long'],'Signal']=1
    data.loc[data['SMA_Short']<=data['SMA_Long'],'Signal']=-1
    return data
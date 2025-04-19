def backtest_strategy(data,initial_capital):
    capital=initial_capital
    position=0
    for i in range(1,len(data)):
        if data['Signal'].iloc[i]==1 and position==0:
            position=capital/data['Close'].iloc[i]
            capital=0
        elif data['Signal'].iloc[i]==-1 and position>0:
            capital=position*data['Close'].iloc[i]
            position=0

    return capital+(position*data['Close'].iloc[-1] if position>0 else 0)
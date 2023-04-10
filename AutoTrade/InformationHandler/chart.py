import requests
import numpy as np
import matplotlib.pyplot as plt

# export get_market_list, get_candle_data, plot_candle_chart for 'all'
__all__ = ['get_market_list', 'get_candle_data', 'plot_candle_chart']

def get_market_list():
    url = "https://api.upbit.com/v1/market/all?isDetails=true"
    headers = {"accept": "application/json"}
    response = requests.get(url, headers=headers)
    return response.json()

def get_candle_data(market_code, count=200, interval="days"):
    url = f"https://api.upbit.com/v1/candles/{interval}"
    querystring = {"market": market_code, "count": count}
    headers = {"accept": "application/json"}
    response = requests.get(url, headers=headers, params=querystring)
    return response.json()

def plot_candle_chart(data, market_code):
    # data : get_candle_data() 함수의 리턴값
    # market_code : get_candle_data() 함수의 market_code 인자값
    # data -> list of dict 
    # data sample : {'market': <str>, 'candle_date_time_utc': '2023-04-06T00:00:00', 'candle_date_time_kst': '2023-04-06T09:00:00', 'opening_price': <float>, 'high_price': <float>, 'low_price': <float>, 'trade_price': <float>, 'timestamp': <int>, 'candle_acc_trade_price': <float>, 'candle_acc_trade_volume': <float>, 'prev_closing_price': <float>, 'change_price': <float>, 'change_rate': <float>}
    # plot bar chart with keys : 'candle_date_time_kst', 'opening_price', 'high_price', 'low_price', 'trade_price'
    # Get the data points for the chart
    dates = [d['candle_date_time_kst'].split('T')[0].split('-')[-1] for d in data]
    opens = np.array([d['opening_price'] for d in data])
    highs = np.array([d['high_price'] for d in data])
    lows = np.array([d['low_price'] for d in data])
    closes = np.array([d['trade_price'] for d in data])

    # Calculate the colors for the bars
    colors = ['green' if opens[i] < closes[i] else 'red' for i in range(len(data))]

    # Create the bar chart
    fig, ax = plt.subplots()
    ax.bar(dates, highs-lows, bottom=lows, color=colors, width=0.8, edgecolor='black')
    ax.vlines(dates, lows, highs, color='black', linewidth=1)
    ax.scatter(dates, opens, color=colors, marker='.', edgecolors='black')

    # Add labels and title
    ax.set_title('Candle Chart for ' + market_code)
    ax.set_xlabel('Date')
    ax.set_ylabel('Price')

    # Show the chart
    plt.show()
    
    
    
    

if __name__ == "__main__":
    market_list = get_market_list()
    for market in market_list:
        if market["market"] == "KRW-BTC":

            plot_candle_chart(get_candle_data(market["market"],count=20), market["market"])
    
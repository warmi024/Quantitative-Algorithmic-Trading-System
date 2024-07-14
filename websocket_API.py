import pandas as pd
import numpy as np
import talib
import statsmodels.api as sm
import bybit
import time
from pybit.unified_trading import HTTP, WebSocket
import pickle
import schedule
from functools import partial
from datetime import datetime
from time import sleep

def on_startup():
    # Models data is loaded from excel files
    df = pd.read_excel('results_long_sol.xlsx', engine='openpyxl')
    X = df.iloc[:, 1:]
    y = df.iloc[:, 0]
    X = sm.add_constant(X)
    model = sm.Logit(y, X)
    model_long = model.fit()

    df = pd.read_excel('results_short_sol.xlsx', engine='openpyxl')
    X = df.iloc[:, 1:]
    y = df.iloc[:, 0]
    X = sm.add_constant(X)
    model = sm.Logit(y, X)
    model_short = model.fit()

    # Connection to the Bybit API
    session = HTTP(
        testnet=False,
        api_key="*********************",
        api_secret="**************************",
    )

    # Initial data download
    response = session.get_kline(
        category="linear",
        symbol="SOLUSDT",
        interval=1,
        limit=1000
    )
    # Transforming data into a DataFrame
    data_list = response['result']['list']
    df = pd.DataFrame(data_list, columns=['timestamp', 'open', 'high', 'low', 'close', 'Volume', 'Amount'])
    df = df.drop(columns=['timestamp','Amount', 'Volume'])
    df = df.iloc[::-1]
    df = df.iloc[:-1]
    df.reset_index(inplace=True, drop=True)
    df['open'] = df['open'].astype(float)
    df['high'] = df['high'].astype(float)
    df['low'] = df['low'].astype(float)
    df['close'] = df['close'].astype(float)

    # Connection to the Bybit websocket stream
    ws = WebSocket(testnet=False, channel_type="linear")
    ws.kline_stream(interval=1, symbol="SOLUSDT", callback=candle_closed_algo)
    return [df, model_long, model_short, session]

# Function that detects if candle closed, if so main function is called
def candle_closed_algo(message):
    if 'data' in message:
        for data_item in message['data']:
            if 'confirm' in data_item and data_item['confirm']:
                new_row = {
                    'open': float(data_item['open']),
                    'high': float(data_item['high']),
                    'low': float(data_item['low']),
                    'close': float(data_item['close'])
                }
                print('Candle closed')
                one_minute_period_algo(new_row)

def one_minute_period_algo(new_row):
    start_time = time.time()
    global data
    df=data[0]
    model_long=data[1]
    model_short=data[2]
    session=data[3]

    # Adding new row to the DataFrame
    new_row = pd.DataFrame([new_row])
    new_row['open'] = new_row['open'].astype(float)
    new_row['high'] = new_row['high'].astype(float)
    new_row['low'] = new_row['low'].astype(float)
    new_row['close'] = new_row['close'].astype(float)
    df = pd.concat([df, new_row], ignore_index=True)
    df = df.iloc[1:].reset_index(drop=True)

    #calculation of all variables that are shared between long and short
    calculate_model(df)

    # Creating a call for account balance
    response = session.get_wallet_balance(accountType="CONTRACT", coin="USDT")
    equity = float(response['result']['list'][0]['coin'][0]['equity'])
    risk = equity * 0.001

    # Cancelling all the unrealized orders from the previous iteration
    session.cancel_all_orders(
        category="linear",
        symbol="SOLUSDT",
        orderFilter = 'StopOrder',
        stopOrderType = "Stop"
    )

###########################################long case#################################################
    # Calculation of variables for long
    calculate_long_model(df)

    # If there is a setup detected, we calculate the probability of the setup and send an order to the broker
    if setup_long:     
        predicted_probabilities = model_long.predict(data_for_model)
        take_profit = curret_swing_high + 1
        stop_loss = curret_swing_high - 1
        order_size = round(100*risk / curret_swing_high, 1)
        print(f'Equity: {equity}, risk: {risk}, order size: {order_size}')

        print(f"Probability long: {predicted_probabilities.iloc[0]}")
        if predicted_probabilities.iloc[0] >= 0.65:
            print(f'We send to the broker an order to buy at {current_swing_high} (buystop order), with take profit at {current_swing_high+1} and stop loss at {current_swing_high-1}, order size: {order_size}')
            session.place_order(
                category="linear",
                symbol="SOLUSDT",
                side="Buy",
                orderType="Market",
                qty=str(order_size),
                triggerDirection= 1,
                triggerPrice=str(curret_swing_high),
                triggerBy="MarkPrice",
                positionIdx = 1,
                takeProfit=str(take_profit),
                stopLoss=str(stop_loss),
                tpslMode="Partial"

            )
            print('Order sent')
        else:
            print('Probably not enough probability to send order to broker, we wait for next signal')
    else:
        print('No setup detected')
###########################################short case#################################################
    # Calculation of variables for short
    calculate_short_model(df)

    # If there is a setup detected, we calculate the probability of the setup and send an order to the broker
    if setup_short:     
        predicted_probabilities = model_short.predict(data_for_model)
        take_profit = curret_swing_low - 1
        stop_loss = curret_swing_low + 1
        order_size = round(100*risk / curret_swing_high, 1)
        print(f'Equity: {equity}, risk: {risk}, order size: {order_size}') 
        print(f"Probability short: {predicted_probabilities.iloc[0]}")
        if predicted_probabilities.iloc[0] >= 0.64:
            print(f'We send to the broker an order to sell at {current_swing_low} (sellstop order), with take profit at {take_profit} and stop loss at {stop_loss}, order size: {order_size}.')
            session.place_order(
                category="linear",
                symbol="SOLUSDT",
                side="Sell",
                orderType="Market",
                qty=str(order_size),
                triggerDirection= 2,
                triggerPrice=str(curret_swing_low),
                triggerBy="MarkPrice",
                positionIdx = 2,
                takeProfit=str(take_profit),
                stopLoss=str(stop_loss),
                tpslMode="Partial"
            )
            print('Order sent')
        else:
            print('Probably not enough probability to send order to broker, we wait for next signal')
    else:
        print('No setup detected') 

    # Preparing data for the next iteration
    data = [df, model_long, model_short, session]
    end_time = time.time()
    elapsed_time = end_time - start_time
    end_datetime = datetime.fromtimestamp(end_time)
    print(f"Elapsed time: {elapsed_time}, time: {end_datetime} seconds")

data = on_startup()

while True:
    sleep(5)

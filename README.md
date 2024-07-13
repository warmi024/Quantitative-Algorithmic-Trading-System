# Quantitative-Algorithmic-Trading-System
This repository showcases one of my trading algorithms, along with its integration with the Bybit API.
It is worth noting that I will be sharing only a small part of my trading system. The price data utilized in this project cannot be shared due to licensing restrictions.

This file will contain explanation of more complex concepts presented in my algorythm with images for easier understading, easy concepts are explained in the code. Code will be in .ipynb script with all the code and functions inside, normally I would separate main code and functions, but that way it will be easier to present. Part of the code that can be used in various strategies are written in functions, but this system specific parts are simply in the main code

1. Introductions
   This system is based on popular, as well as my personal trading concepts, mainly based on technical analysis, it utilizes price action, indicators, wyckoff theory concepts and others.
   Data used for all the calculations is nasdaq price data over the period of 2018-2022. It contains timestamp, high, low, close, open prices as well as volume colums. During visualizing concepts I will use standard japanese candlesstick charts. The image below is a short explanation of them.
   ![image](https://github.com/user-attachments/assets/fe246f93-e7f0-4013-8160-a2f8af098af6)
  The heart of the strategy will be so called demand zones. A demand level is an area where investors are expected to be more inclined to buy an asset, potentially leading to price increases. In this system i utilize stoplosses as well as take profit order that allow traders to secure profit or restrict the loss of capital.
![image](https://github.com/user-attachments/assets/e8aa545c-80f5-4a69-bfb5-14be89fbf0ed)

2. Concepts used
   2.1 Trend based on market structure analysis
   ![image](https://github.com/user-attachments/assets/bcb98710-11d8-4574-aa4e-4c3a9b0516e4)
    In the case of an uptrend, new highs and lows should be higher than the previous ones. A peak higher than the previous one is labeled as a "higher high," and a low higher than the previous one is termed a "higher low." As long as the price continues to form  successive higher highs and higher lows, the uptrend is sustained.
   
   2.2 Support


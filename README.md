# Quantitative-Algorithmic-Trading-System
This repository showcases one of my trading algorithms, along with its integration with the Bybit API.
It is worth noting that I will be sharing only a part of my trading system. The price data utilized in this project cannot be shared due to licensing restrictions.

This file will contain explanation of more complex concepts presented in my algorithm with images for easier understading. Code is showcased in .ipynb script with all the code and functions inside, normally I would separate main code and functions, but that way it will be easier to present. Parts of the code that can be used in various strategies are written in functions, but this system specific parts are simply in the main code. It is also important that almost at the beginning of the algorithm we are creating a slice of data to avoid look-ahead bias.

1. Introductions
   
   This system is based on popular, as well as my personal trading concepts, mainly based on technical analysis, it utilizes price action, indicators, wyckoff theory concepts and others.
   Data used for all the calculations is nasdaq price data over the period of 2018-2022. It contains timestamp, high, low, close, open prices as well as volume colums. During visualizing concepts I will use standard japanese candlesstick charts. The image below is a short explanation of them.
   
   ![image](https://github.com/user-attachments/assets/fe246f93-e7f0-4013-8160-a2f8af098af6)
   
  The heart of the strategy will be so called demand zones. A demand level is an area where investors are expected to be more inclined to buy an asset, potentially leading to price increases. In this system I utilize stoplosses as well as take profit order that allow traders to secure profit or limit the potencial loss of capital. The returns (Y-variable) of the strategy are coded in two different ways: one uses binary data (0 for loss, 1 for win), and the other uses a continuous outcome variable. This dual approach allows for capturing information on the possible duration of a trade while also enabling the use of binary models like logistic regression, as well as OLS models. To limit amount of signals I use 5 minute timeframe and signals are valid only after market is open (amount of signals pre-open is closed to 0). I also filter out too small structures to limit amount of payed fees.

   ![image](https://github.com/user-attachments/assets/e8aa545c-80f5-4a69-bfb5-14be89fbf0ed)

2. Concepts used
   
   2.1 Trend based on market structure analysis
   
   ![image](https://github.com/user-attachments/assets/bcb98710-11d8-4574-aa4e-4c3a9b0516e4)
    In the case of an uptrend, new highs and lows should be higher than the previous ones. A peak higher than the previous one is labeled as a "higher high," and a low higher than the previous one is termed a "higher low." As long as the price continues to form  successive higher highs and higher lows, the uptrend is sustained. I have also calculated slope of created highs and lows to better describe dinamics of trend.
   
   2.2 Support and resistance zones
   ![image](https://github.com/user-attachments/assets/1574a9e1-254e-49b2-91aa-e893cd76c283)
   
   These zones represent places from which price bounces in the past resulting in move in oppisite direction, a reversal. In code we are checking how many times price bounces from our entry potencial area. Calculations are done based on different critiria, closing price of candles, amount of wicks as well as bounces, defined as candles moving in opposite direction after hitting a zone.
   
   2.3 Mathematical Indicators
   
      Mathematical indicators are numerical expressions based on price and volume data of financial instruments. Their purpose is to transform market data into graphical or numerical form, facilitating analysis and investment decision-making. These indicators assist investors in identifying trends, assessing the strength of price movements, and determining entry and exit points from positions. For most of calculations I have utilized TA-lib library, but some indicators I have coded by myself, due to lack of them in used library.

   2.4 Lineral reggresion and crosses with EMA
   
      I have used linear regression for judgment of slope, so strengh of up or down side trend. It is calculated in based on closing price of chosen asset. Amount of crosses with exponecial moving average is another way of judging strengh of trend, the stronger it is, the lower the amount of times it will cross moving average.

   2.5 Other variables
   
      Rest of deployed variables have been described in code, due to their simplicity.

3. Research
   
   In order to analize usefullness of these variables I have visualized them on charts, including non linear relationships, squares of them as well as log values and compared pvalues. Interactions between certain variables have also been studied. Only some parameters have been optimized to avoided overfitting my future model. Different closing strategies have been compared with the consensus of holding longer being correlated positively with probability of win, which isnt surprizing as my strategy has been tested on mostly bullish market and presented system is researching only long (buy) case.
   
   After visualization and optimization I have created a backtest of this system using different combinations of variables. Logit model is used for calculating probability of each observations, based on which we take or do not take certain trade into consideration. Probability can be calculated based on whole model or just lookback period to adjust model for changing market conditions, such as trend. Chart of the tested asset is plotted as well as returns chart from the strategy and drawdown chart with some additional statistics in the table below. Plotting assest price is important, so we can see if model is actually capable of predicting market movement and not only following its overall direction. Presented model, which can be seen in the .ipynb is profitable regardless of market movement direction, which proves its usefulness.

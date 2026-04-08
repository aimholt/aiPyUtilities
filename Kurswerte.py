""" 
    Module to get current stock prices using yfinance
    input: stock list with stocks in json format    
"""
import yfinance as yf
import sys, os
import json

if sys.platform.startswith('linux'):
    DATADIR =  "/home/andreas/projects/testData"
else:
    DATADIR = "C:\\Users\\Andreas\\projects\\testData"

FILENAME = "mystock.json"

YFS_CURR = {
        'USD':    'EUR=X'
    }

MYSTOCK = json.load(open(os.path.join(DATADIR, FILENAME), "r"))

if __name__ == "__main__":
    #using yfinance to get stock prices
    for ticker in MYSTOCK['stocks']:
        ticker_info=yf.Ticker(ticker['YFS']).info
        if ticker_info['currency'] == 'USD':
            ticker_info['regularMarketPrice'] *= yf.Ticker(YFS_CURR['USD']).info['regularMarketPrice']
            ticker_info['currency'] = 'EUR*'
        print(  f'Share: {ticker_info['shortName']:35s}{ticker['ISIN']};{ticker['YFS']:15s}  ' \
                f'Price: {ticker_info['regularMarketPrice']:>8.3f} {ticker_info['currency']:4s}  ' \
                f'Exchange: {ticker_info['exchange']} {ticker_info['fullExchangeName']:12s}  ' \
                f'TimeZone: {ticker_info['exchangeTimezoneShortName']} '
                )

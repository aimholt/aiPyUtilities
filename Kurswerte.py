"""
    Module to get current stock prices using yfinance
    input: stock list with stocks in json format
"""
import yfinance as yf
import sys, os
import json
from argparse import ArgumentParser

def format_german_number(value, decimals=3):
    formatted = f"{value:,.{decimals}f}"
    return formatted.replace(',', 'X').replace('.', ',').replace('X', '.')

def main():
    if sys.platform.startswith('linux'):
        DATADIR =  "/home/andreas/projects/testData"
    else:
        DATADIR = "C:\\Users\\Andreas\\projects\\TestData"
    FILENAME = "mystock.json"

    parser=ArgumentParser(
        prog='Kurswerte',
        description='backend-tool to get current stock prices using yfinance'
        )
    parser.add_argument('-c', '--csv',
            help='output stock data csv formatted',
            default=False, action='store_true'
        )
    parser.add_argument('-d', '--directory',
            default=DATADIR,
            help='set directory, default: '+ DATADIR,
            type=str)
    parser.add_argument('-f', '--filename',
            default=FILENAME,
            help='set filename, default' + FILENAME,
            type=str)

    args=parser.parse_args()

    YFS_CURR = {
            'USD':    'EUR=X'
        }

    MYSTOCK = json.load(open(os.path.join(args.directory, args.filename), "r"))

    #using yfinance to get stock prices
    for ticker in MYSTOCK['stocks']:
        ticker_info=yf.Ticker(ticker['YFS']).info
        if ticker_info['currency'] == 'USD':
            ticker_info['regularMarketPrice'] *= yf.Ticker(YFS_CURR['USD']).info['regularMarketPrice']
            ticker_info['currency'] = 'EUR*'

        formatted_price = format_german_number(ticker_info['regularMarketPrice'], decimals=3)

        if args.csv:
            print(f"{ticker_info['shortName']};{ticker['ISIN']};{ticker['YFS']};{formatted_price};{ticker_info['currency']};{ticker_info['exchange']};{ticker_info['fullExchangeName']};{ticker_info['exchangeTimezoneShortName']}")
        else:
            print(  f"Share: {ticker_info['shortName']:35s}{ticker['ISIN']};{ticker['YFS']:15s}  " \
                    f"Price: {formatted_price:>12s} {ticker_info['currency']:4s}  " \
                    f"Exchange: {ticker_info['exchange']} {ticker_info['fullExchangeName']:12s}  " \
                    f"TimeZone: {ticker_info['exchangeTimezoneShortName']} "
                )

if __name__ == "__main__":
    main()
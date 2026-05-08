"""
    Module to get current stock prices using yfinance
    input: stock list with stocks in json format
"""
import yfinance as yf
import sys, os
import json
from argparse import ArgumentParser
from datetime import datetime

def format_german_number(value, decimals=3):
    formatted = f"{value:,.{decimals}f}"
    return formatted.replace(',', 'X').replace('.', ',').replace('X', '.')

def main():
    if sys.platform.startswith('linux'):
        DATADIR =  "/home/andreas/projects/testData"
    else:
        DATADIR = "C:\\Users\\Andreas\\projects\\TestData"
    FILENAME = "mystock.json"
    DATUM_HEUTE = datetime.now().strftime("%d.%m.%Y")
    
    parser=ArgumentParser(
        prog='Kurswerte',
        description='backend-tool to get current stock prices using yfinance'
        )
    group1=parser.add_mutually_exclusive_group(required=False)
    group1.add_argument('-f', '--filename',
            default=FILENAME,
            help='filename for stock list(json format); default is:' + FILENAME,
            type=str
        )
    group1.add_argument('-y', '--yfs',
            help='set yfinance ticker, e.g. AAPL',
            type=str,
        )
    parser.add_argument('-c', '--csv',
            help='output stock data csv formatted',
            default=False, action='store_true'
        )
    parser.add_argument('-d', '--directory',
            default=DATADIR,
            help='set directory, default: '+ DATADIR,
            type=str)

    args=parser.parse_args()

    # currency conversion for USD to EUR, if stock price is in USD
    # other currencies can be added to YFS_CURR if needed, e.g. GBP, CHF, etc.
    YFS_CURR = {
            'USD':    'EUR=X'
            }

    # MYSTOCK, built with json file or from single value via command line argument
    if args.yfs:
        MYSTOCK = {
            "comment":  "stock list for single value json format.", 
            'stocks': [{'ISIN': 'N/A', 'YFS': args.yfs}]
            }
    else:
        MYSTOCK = json.load(open(os.path.join(args.directory, args.filename), "r"))

    #using yfinance to get stock prices
    print(f"Kursdaten;{DATUM_HEUTE}")
    for ticker in MYSTOCK['stocks']:
        ticker_info=yf.Ticker(ticker['YFS']).info
        if ticker_info['currency'] == 'USD':
            ticker_info['regularMarketPrice'] *= yf.Ticker(YFS_CURR['USD']).info['regularMarketPrice']
            ticker_info['currency'] = 'EUR*'

        formatted_price = format_german_number(ticker_info['regularMarketPrice'], decimals=3)
        if args.csv:
            print(  f"{ticker_info['shortName']};" \
                    f"{ticker['ISIN']};" \
                    f"{ticker['YFS']};" \
                    f"{formatted_price};" \
                    f"{ticker_info['currency']};" \
                    f"{ticker_info['exchange']};" \
                    f"{ticker_info['fullExchangeName']};" \
                    f"{ticker_info['exchangeTimezoneShortName']}"
                )
        else:
            print(  f"Share: {ticker_info['shortName']:35s}" \
                    f"ISIN: {ticker['ISIN']:12s} " \
                    f"YFS: {ticker['YFS']:15s}  " \
                    f"Price: {formatted_price:>10s} {ticker_info['currency']:4s}  " \
                    f"Exchange: {ticker_info['exchange']} " \
                    f"Name: {ticker_info['fullExchangeName']:12s}  " \
                    f"TimeZone: {ticker_info['exchangeTimezoneShortName']} "
                )

if __name__ == "__main__":
    main()
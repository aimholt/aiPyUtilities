""" 
    Module to get current stock prices using yfinance
    input: list withc stock of ISIN values    
"""
import yfinance as yf

### YFS - yahoo finance symbol

YFS_CURR = {
        'USD':    'EUR=X'
    }

MYSTOCK = [
    {   'ISIN': 'DE0008471012', 'YFS':  'HJVD.F'},
    {   'ISIN': 'LU0321021312', 'YFS':  'AH8S.HM'},
    {   'ISIN': 'DE0009807016', 'YFS':  'H5AB.F'},
    {   'ISIN': 'LU0061928585', 'YFS':  'OE7A.F'},
    {   'ISIN': 'LU1136260384', 'YFS':  '0P00015JD5.F'},
    {   'ISIN': 'LU0301152442', 'YFS':  'WXO3.F'},
    {   'ISIN': 'IE00BZ02LR44', 'YFS':  'XZW0.DE'},
    {   'ISIN': 'IE0009HF1MK9', 'YFS':  'IE0009HF1MK9.SG'},
    {   'ISIN': 'IE00B3WJKG14', 'YFS':  'IUIT.SW'},
    {   'ISIN': 'IE00B0M62S72', 'YFS':  'IDVY.AS'},
    ]

if __name__ == "__main__":
    #using yfinance to get stock prices
    for ticker in MYSTOCK:
        ticker_info=yf.Ticker(ticker['YFS']).info
        if ticker_info['currency'] == 'USD':
            ticker_info['regularMarketPrice'] *= yf.Ticker(YFS_CURR['USD']).info['regularMarketPrice']
            ticker_info['currency'] = 'EUR*'
        print(  f'Share: {ticker_info['shortName']:35s}{ticker['ISIN']};{ticker['YFS']:15s}  ' \
                f'Price: {ticker_info['regularMarketPrice']:>8.3f} {ticker_info['currency']:4s}  ' \
                f'Exchange: {ticker_info['exchange']} {ticker_info['fullExchangeName']:12s}  ' \
                f'TimeZone: {ticker_info['exchangeTimezoneShortName']} '
                )

""" 
    Module to get current stock prices using yfinance
    input: list withc stock of ISIN values    
"""
import yfinance as yf

MYSTOCK =[
    'DE0008471012',
    'LU0321021312',
    'DE0009807016',
    'LU0061928585',
    'LU1136260384',
    'LU0301152442',
    'IE00BZ02LR44',
    'IE0009HF1MK9',
    'IE00B3WJKG14'
    ]

if __name__ == "__main__":
    #using yfinance to get stock prices
    for ticker in MYSTOCK:
        ticker_info=yf.Ticker(ticker).info
        print(  f'Share: {ticker_info['shortName']:32s}({ticker}):  ' \
                f'Price: {ticker_info['regularMarketPrice']:>8.3f} {ticker_info['currency']}  ' \
                f'Exchange: {ticker_info['exchange']} {ticker_info['fullExchangeName']:12s}  ' \
                f'TimeZone: {ticker_info['exchangeTimezoneShortName']} '
                )

import os, csv
import pandas as pd
from flask import Flask, render_template, request
from patterns import patterns
import yfinance as yf
from vol_screener import volatility_screener

app = Flask(__name__)


@app.route('/')
def index():
    pattern = request.args.get('pattern', None)
    stocks = {}

    with open('dataset/companies.csv') as f:
        for row in csv.reader(f):
            stocks[row[0]] = {'company': row[1]}
    print(stocks)

    if pattern:
        filenames = os.listdir('dataset/daily')
        for filename in filenames:
            df = pd.read_csv(f'dataset/daily/{filename}')
            symbol = filename.split('.')[0]
            vol = volatility_screener(df, symbol)
            pattern_function = getattr(vol, pattern)
            try:
                upper, down = pattern_function()
                if upper:
                    # print('upper')
                    stocks[symbol][pattern] = 'UP'
                elif down:
                    # print('down')
                    stocks[symbol][pattern] = 'DOWN'
                else:
                    stocks[symbol][pattern] = None
            except:
                pass
            
        
    return render_template('index.html', patterns=patterns, stocks=stocks, current_pattern=pattern)


@app.route('/snapshot')
def snapshot():
    with open('dataset/companies.csv') as f:
        companies = f.read().splitlines()
        for company in companies:
            symbol = company.split(',')[0]
            df = yf.download(symbol, start='2020-05-01')
            df.to_csv(f'dataset/daily/{symbol}.csv')
            print(symbol)
    return {
        'code': 'success'
    }

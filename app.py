import os
import csv
import pandas as pd
import yfinance as yf
import talib
from datetime import date
from flask import Flask, render_template, request
from patterns import candlestick_patterns

from sys import argv

app = Flask(__name__)


@app.route('/')
def index():
    Pattrn = request.args.get('Pattrn', None)
    print(Pattrn)
    Date = request.args.get('date', None)
    print(Date)
    today = date.today()
    print(today)
    stocks = {}
    with open('data/data.csv') as f:
        for row in csv.reader(f):
            stocks[row[0]] = {'company': row[0]}
    #print(stocks)
    datafile = os.listdir('data/daily')
    for filename in datafile:
        df = pd.read_csv('data/daily/{}'.format(filename))
        df.dropna(axis=0)
        pattern_function = getattr(talib, Pattrn)
        symbol = filename.split('.')[0] +'.' + filename.split('.')[1]
        #symbol=symbol[0]+'.'+symbol[1]
        #print(symbol)
        try:
            result = pattern_function(df['Open'], df['High'], df['Low'], df['Close'])
            #print(result)
            last = result.tail(1).values[0]
            #print(last)
            if last > 0:
                stocks[symbol][Pattrn] = 'bullish'
            elif last < 0:
                stocks[symbol][Pattrn] = 'bearish'
            else:
                stocks[symbol][Pattrn] = None


            #elif last < 0:
            #    stocks[symbol][Pattrn] = 'bearish'
            #    # print('{}'.format(stocks, Pattrn))

            #else:
            #    stocks[symbol][Pattrn] = None

        except:
            pass

    # print(datafile)
    return render_template('index.html', patterns=candlestick_patterns, stocks=stocks, pattern=Pattrn)


@app.route('/snapshot')
def snapshot():
    # with open('data/data.csv', 'r') as f:
    f = open("data/data.csv", "r")
    # companies = csv.reader(f)
    # print(companies)
    db = []
    for line in csv.reader(f):
        db.append(line)
    # print(db)
    # companies= f.read()
    for company in db:
        symbol = company[0]
        # print(symbol)
        data = yf.download(symbol, start="2020-10-01", end= "today")
        data.to_csv('data/daily/{}.csv'.format(symbol))
    return {

        'code': 'sucess'
    }

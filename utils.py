import csv
import urllib
from datetime import datetime

import pandas as pd
from pandas.io.parsers import read_csv

from db import models

import settings


def load_tickers():
	'''
	Parses ticker_list.csv list and pulls out symbols
	'''
	session = models.create_db_session()

	ticker_file = csv.reader(open('data/ticker_list.csv', 'rU'))
	for row in ticker_file:
		symbol = row[0]
		results = session.query(models.Ticker).filter(models.Ticker.symbol==symbol)
		if not results.count():
			t = models.Ticker(symbol=symbol)
			session.add(t)
	session.commit()

	models.end_db_session(session)


def fetch_all_data():
	'''
	Fetches all available yahoo historical data for all ticker symbols
	'''
	session = models.create_db_session()

	ticker_list = session.query(models.Ticker).all()

	for ticker in ticker_list:
		if settings.SKIP_PREFERRED_STOCKS:
			if '-' in ticker.symbol:
				print "Skipping..." + ticker.symbol
				continue

		fetch_ticker_data(ticker)
		fetch_special_data(ticker)

	models.end_db_session(session)


def fetch_ticker_data(ticker):
	'''
	Fetches all available yahoo historical data for a ticker symbol
	'''

	print "Loading..." + ticker.symbol

	start_date = settings.HISTORICAL_START_DATE
	end_date = datetime.now()

	params = {
			's': ticker.symbol,
			'a': start_date.month,
			'b': start_date.day,
			'c': start_date.year,
			'd': end_date.month,
			'e': end_date.day,
			'f': end_date.year,
			'ignore': '.csv'
		}

	url = 'http://ichart.finance.yahoo.com/table.csv?' + urllib.urlencode(params)

	data = read_csv(urllib.urlopen(url), index_col=0)\
			.reindex([d.strftime('%Y-%m-%d') for d in pd.date_range(start_date,end_date)])\
			.fillna(method='pad')

	session = models.create_db_session()

	results = session.query(models.HistoricalData).filter(models.HistoricalData.ticker==ticker)
	for result in results:
		session.delete(result)

	for date in data.index:
		h = models.HistoricalData(ticker_id=ticker.id, date=datetime.strptime(date,'%Y-%m-%d'),
			open=data['Open'][date], high=data['High'][date], low=data['Low'][date],
			close=data['Close'][date], volume=data['Volume'][date], adj_close=data['Adj Close'][date])

		session.add(h)
	session.commit()

	models.end_db_session(session)


def fetch_special_data(ticker):
	'''
	Fetches all available yahoo fundamental data for a ticker symbol
		gets specific type of data based on format string, e.g. s=symbol, j1=market cap.
		list of format symbols: http://www.gummy-stuff.org/Yahoo-data.htm
		only gets today's data.
	'''

	print "Loading Fundamentals..." + ticker.symbol

	formstr = settings.FUNDAMENTAL_DATA_STRING

	params = {
			's': ticker.symbol,
			'f': formstr,
		}

	url = 'http://finance.yahoo.com/d/quotes.csv?' + urllib.urlencode(params)

	data = read_csv(urllib.urlopen(url), header=None).values[0] # returns one row

	session = models.create_db_session()

	f = models.FundamentalData(ticker_id=ticker.id, date=datetime.now(),
			average_daily_volume=float(data[1]),book_value=float(data[2]),dividend_per_share=float(data[3]),
			earnings_per_share=float(data[4]),ft_week_low=float(data[5]),ft_week_high=float(data[6]),
			market_cap=convert_mktcap(data[7]),name=data[8],p_e_ratio=float(data[9]),short_ratio=float(data[10]))

	session.add(f)
	session.commit()

	models.end_db_session(session)


def convert_mktcap(mktcap_str):
	'''
	converts mktcap from format like '300B' to a number like 300,000,000,000
	'''
	if not isinstance(mktcap_str, str):
		return mktcap_str

	if mktcap_str[-1]=='B':
		mktcap = 1e9*float(mktcap_str[:-1])
	elif mktcap_str[-1]=='M':
		mktcap = 1e6*float(mktcap_str[:-1])
	else:
		mktcap = float(mktcap_str)
	return mktcap


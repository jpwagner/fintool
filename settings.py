from datetime import datetime

DB = {
	'ENGINE': 'sqlite',
	'USER': '',
	'PASSWORD': '',
	'HOST': '',
	'NAME': 'data/ticker_data.db'
}

SKIP_PREFERRED_STOCKS = True

HISTORICAL_START_DATE = datetime(2000,1,1)

FUNDAMENTAL_DATA_STRING = 'sa2b4dejkj1nrs7' # ticker,average_daily_volume,book_value,dividend_per_share,earnings_per_share,ft_week_low,ft_week_high,market_cap,name,p_e_ratio,short_ratio,volume

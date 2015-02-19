from sqlalchemy import MetaData, Column,\
					Integer, Float, String, Text, DateTime, Date, \
					ForeignKey, PickleType, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, validates, relationship, backref
from sqlalchemy.sql import func

import settings

Base = declarative_base()

class CommonBase(Base):
	__abstract__ = True

	id = Column(Integer, primary_key=True)
	created_on = Column(DateTime, default=func.now())
	updated_on = Column(DateTime, default=func.now(), onupdate=func.now())

	@classmethod
	def create_table(self):
		engine = create_db_engine()
		self.__table__.create(engine)	
		return None

	@classmethod
	def drop_table(self):
		engine = create_db_engine()
		self.__table__.drop(engine)
		return None


class Ticker(CommonBase):
	__tablename__ = 'ticker'

	symbol = Column(String(255))
	historical_data = relationship("HistoricalData", backref="ticker", lazy='dynamic')
	fundamental_data = relationship("FundamentalData", backref="ticker", lazy='dynamic')

	def __repr__(self):
		return '<Ticker: %s>' % self.symbol

class HistoricalData(CommonBase):
	__tablename__ = 'historical_data'

	ticker_id = Column(Integer, ForeignKey('ticker.id'))
	date = Column(DateTime)
	open = Column(Float, nullable=True)
	high = Column(Float, nullable=True)
	low = Column(Float, nullable=True)
	close = Column(Float, nullable=True)
	volume = Column(Float, nullable=True)
	adj_close = Column(Float, nullable=True)

	def __repr__(self):
		return '<Historical Data: %s>' % self.ticker.symbol

class FundamentalData(CommonBase):
	__tablename__ = 'fundamental_data'

	ticker_id = Column(Integer, ForeignKey('ticker.id'))
	date = Column(DateTime)
	name = Column(String(255), nullable=True)
	average_daily_volume = Column(Float, nullable=True)
	book_value = Column(Float, nullable=True)
	dividend_per_share = Column(Float, nullable=True)
	earnings_per_share = Column(Float, nullable=True)
	ft_week_low = Column(Float, nullable=True)
	ft_week_high = Column(Float, nullable=True)
	market_cap = Column(Float, nullable=True)
	p_e_ratio = Column(Float, nullable=True)
	short_ratio = Column(Float, nullable=True)

	def __repr__(self):
		return '<Fundamental Data: %s>' % self.ticker.symbol

def create_db_engine(db=settings.DB):
	if db['ENGINE']=='sqlite':
		from sqlite3 import dbapi2 as sqlite
		return create_engine('sqlite+pysqlite:///%s' % (db['NAME']), module=sqlite)

	engine = create_engine('%s://%s:%s@%s/%s' \
			% (db['ENGINE'], db['USER'], db['PASSWORD'], db['HOST'], db['NAME'])\
			, use_native_unicode=False) #, client_encoding='utf8')
	return engine

def create_db_session(db=settings.DB):
	engine = create_db_engine(db)
	Session = sessionmaker(bind=engine)
	session = Session()
	return session

def end_db_session(session):
	session.commit()
	session.close()
	return


from sqlalchemy import exc, event
from sqlalchemy.pool import Pool

@event.listens_for(Pool, "checkout")
def check_connection(dbapi_con, con_record, con_proxy):
	'''Listener for Pool checkout events that pings every connection before using.
	Implements pessimistic disconnect handling strategy. See sqlalchemy docs'''

	cursor = dbapi_con.cursor()
	try:
		cursor.execute("SELECT 1")  # could also be dbapi_con.ping(),
									# not sure what is better
	except exc.OperationalError, ex:
		if ex.args[0] in (2006,   # MySQL server has gone away
						2013,   # Lost connection to MySQL server during query
						2055):  # Lost connection to MySQL server at '%s', system error: %d
			# caught by pool, which will retry with a new connection
			raise exc.DisconnectionError()
		else:
			raise


UPDATE: Yahoo has discontinued the data availability used in this repo.  Will update once I find a better source.

=====

Step 1:
$ python dependencies/get-pip.py

Step 2:
$ pip install virtualenv

Step 3:
$ virtualenv ve

Step 4:
$ source ve/bin/activate

Step 5:
$ pip install -r pip-requires.txt

Step 6:
update the file ...fintool/data/ticker_list.csv
to include all the ticker symbols you want to follow

Step 7:
$ python create_tables.py

Step 8:
$ python load_tickers.py

Step 9:
$ python load_data.py

Download http://sqlitestudio.pl/ to view the data stored in the database which will be located at
...fintool/data/ticker_data.db


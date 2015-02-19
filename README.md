Step 1:
unzip and move fintool somewhere
ex: ~/Projects/fintool

Step 2:
open Applications/Utilities/terminal

Step 3:
(do not type the $ sign, just showing that it's a commandline statement)
$ cd ~/Projects/fintool

Step 4:
$ python dependencies/get-pip.py

Step 5:
$ pip install virtualenv

Step 6:
$ virtualenv ve

Step 7:
$ source ve/bin/activate

Step 8:
$ pip install -r pip-requires.txt

Step 9:
update the file ~/Projects/fintool/data/ticker_list.csv to include all the ticker symbols you want to follow

Step 10:
$ python create_tables.py

Step 11:
$ python load_tickers.py

Step 12:
$ python load_data.py

Step 13:
Download http://sqlitestudio.pl/ to view the data stored in the database which will be located at
~/Projects/fintool/data/ticker_data.db


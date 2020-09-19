import pandas as pd
import yfinance as yf

from datetime import date
from playhouse.db_url import connect


class db:

    def __init__(self):
        self.conn = connect('sqlite:///flywheel.db')
        self.cur = self.conn.cursor()
        if 'MARKET' not in self.conn.get_tables():
            create_market_table_sql = '''CREATE TABLE MARKET(
               ticket CHAR(10),
               date DATE,
               open FLOAT,
               high FLOAT,
               low FLOAT,
               close FLOAT,
               volume INT,
               dividends FLOAT,
               stock_splits INT,
               PRIMARY KEY (ticket, date)
            )'''
            self.cur.execute(create_market_table_sql)
            print("Create market table in the database.")

        self.value_index = {'ticket': 0, 'date': 1, 'open': 2, 'high': 3, 'low': 4, 'close': 5, 'volume': 6, 'dividends': 7, 'stock_splits': 8}

    def get_data(self, ticker, value_name, date=date.today()):
        query_date_format = str(date)[:10]

        read_sql = '''
            SELECT *
            FROM MARKET
            WHERE ticket = ?
            AND date = ?
        '''

        self.cur.execute(read_sql, (ticker, query_date_format,))
        rows = self.cur.fetchall()

        if len(rows) == 0:
            self.__update_db(ticker, query_date_format)

            # re-query in the DB after update
            self.cur.execute(read_sql, (ticker, query_date_format,))
            rows = self.cur.fetchall()

        # If the row is still NULL which means that we don't have data in this date.
        if len(rows) == 0:
            return None
        else:
            return rows[0][self.value_index[value_name]]

    # TODO: query multidate datas instead of querying date.
    def get_multidate_datas(self, ticker, value_name, dates):
        result = []
        for date in dates:
            value = self.get_data(ticker, value_name, date)
            if value is not None:
                result.append([date, value])
        return pd.DataFrame(result, columns=['date', value_name])


    def __update_db(self, ticker, market_date_format):
        stock = yf.Ticker(ticker)
        stock_history_price_dict = self.__crawl_stock_history_price(stock, "10d", "1d")

        # overwrites ticker history price data, updates the stock data and stores in database
        insert_sql = '''
            REPLACE INTO MARKET (ticket, date, open, high, low, close, volume, dividends, stock_splits)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);
        '''
        record_list = []
        for key, value in stock_history_price_dict.items():
            record_list.append((ticker, key, value['Open'], value['High'], value['Low'], value['Close'], value['Volume'], value['Dividends'], value['Stock Splits']))
        self.cur.executemany(insert_sql, record_list)
        self.conn.commit()


    def __crawl_stock_history_price(self, stock_ticker, period="10d", interval="1d"):
        ticker_history_price = stock_ticker.history(period=period, interval=interval)
        ticker_history_price.index = ticker_history_price.index.to_series().apply(lambda x: str(x)[:10])
        return ticker_history_price.to_dict('index')

if __name__ == '__main__':
    database = db()
    t = database.get_multidate_datas('GOOG', 'close', ['2020-09-17', '2020-09-18', '2020-09-19'])
    print(t)
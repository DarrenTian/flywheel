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
            SELECT ?
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
                result.append((date, value))

    def __update_db(self):
        pass

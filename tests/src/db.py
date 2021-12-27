import os

import loguru
import psycopg2 as pg

PG_PASSWORD = os.environ["PG_PASSWORD"]
HOST = os.environ['HOST']


class DB:

    def __init__(self):
        self.connect = pg.connect(dbname="alpaca", user="user", password=PG_PASSWORD, host=HOST, port="5432")
        self.cursor = None
        self.result = None

    def execute_query(self, query: str) -> pg:
        try:
            self.cursor = self.connect.cursor()
            self.cursor.execute(query)
            self.result = self.cursor.fetchone()
            self.connect.commit()
        except (Exception, pg.Error) as err:
            loguru.logger.error(err)
        else:
            return self.result

    def __del__(self):
        if self.connect:
            self.cursor.close()
            self.connect.close()
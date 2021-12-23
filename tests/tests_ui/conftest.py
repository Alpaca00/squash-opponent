import os
import pytest
import psycopg2 as pg

PG_PASSWORD = os.environ["PG_PASSWORD"]
HOST = os.environ['HOST']


@pytest.fixture
def connect_db():
    conn = pg.connect(dbname="alpaca", user="user", password=PG_PASSWORD, host=HOST, port="5432")
    cur = conn.cursor()
    yield cur
    conn.commit()
    cur.close()
    conn.close()

import os
import pytest
import psycopg2 as pg

PG_PASSWORD = os.environ["PG_PASSWORD"]


@pytest.fixture
def connect_db():
    conn = pg.connect(dbname="alpaca", user="user", password=PG_PASSWORD, host="46.101.139.62", port="5432")
    cur = conn.cursor()
    yield cur
    conn.commit()
    cur.close()
    conn.close()

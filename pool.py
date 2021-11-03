from contextlib import contextmanager
from typing import ContextManager
from psycopg2 import pool
import decouple

pool = pool.SimpleConnectionPool(1, 20, decouple.config("DATABASE_URL"),sslmode='require')


@contextmanager
def db():
    con = pool.getconn()
    cur = con.cursor()
    try:
        yield con, cur
    finally:
        cur.close()
        pool.putconn(con)

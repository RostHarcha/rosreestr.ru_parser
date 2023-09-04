from os import environ
from playhouse.pool import PooledSqliteExtDatabase

# DB_NAME = environ['DB_NAME']
# DB_USER = environ['DB_USER']
# DB_PASS = environ['DB_PASS']
# DB_HOST = environ['DB_HOST']
# DB_PORT = environ['DB_PORT']

database = PooledSqliteExtDatabase(
    database='database.db',
    stale_timeout=10,
)

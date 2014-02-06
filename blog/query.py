import datetime

from django.db import connection

def query(sql):
    """
    Execute a query on the default database and yield the rows.
    """
    cursor = connection.cursor()

    try:
        cursor.execute(sql)

        for i in range(cursor.rowcount):
            yield cursor.fetchone()
    finally:
        cursor.close()


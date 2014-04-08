from django.db import connection


def query(sql):
    """
    Execute a query on the default database and yield the rows.
    """
    cursor = connection.cursor()

    try:
        cursor.execute(sql)

        for _ in range(cursor.rowcount):
            yield cursor.fetchone()
    finally:
        cursor.close()

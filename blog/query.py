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

def all_article_months():
    """
    Yield all article months as datetime objects.

    The results will be ordered from latest to oldest.
    """
    results = query(
        "SELECT DISTINCT "
            "EXTRACT(YEAR FROM creation_date), "
            "EXTRACT(MONTH FROM creation_date) "
        "FROM blog_article "
        "WHERE active "
        "ORDER BY 1 DESC, 2 DESC "
    )

    for row in results:
        yield datetime.datetime(int(row[0]), int(row[1]), 1)


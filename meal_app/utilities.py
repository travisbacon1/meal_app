from . import mysql

def execute_mysql_query(query_string):
    db_cursor = mysql.connection.cursor()
    db_cursor.execute(query_string)
    results = db_cursor.fetchall()
    return results
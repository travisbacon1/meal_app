import os
import MySQLdb
import MySQLdb.cursors
import json
from dotenv import load_dotenv

load_dotenv()
database = MySQLdb.connect(
        host=os.environ['MYSQL_HOSTNAME'],
        user=os.environ['MYSQL_USER'],
        password=os.environ['MYSQL_PASSWORD'],
        database=os.environ['MYSQL_DATABASE'],
        cursorclass=MySQLdb.cursors.DictCursor
    )


def execute_mysql_query(data):
    """Executes a MySQL query
    Parameters
    -------
    query_string: string

    Returns
    ------
    result: tuple
    """
    db_cursor = database.cursor()
    statement = f"INSERT IGNORE INTO {os.environ['MYSQL_INGREDIENTS_TABLE']}(Name, Unit, Type) VALUES (%s, %s, %s)"
    db_cursor.executemany(statement, data)
    db_cursor.connection.commit()


def insert_ingredients(filename, ingredient_type):
    with open(filename) as fp:
        data = json.load(fp)
    data_to_insert = [[key, value, ingredient_type] for key, value in data.items()]
    execute_mysql_query(data_to_insert)


def main():
    query_string = f"""CREATE TABLE IF NOT EXISTS `{os.environ['MYSQL_INGREDIENTS_TABLE']}` (
        `Name` varchar(45) NOT NULL,
        `Unit` varchar(45) DEFAULT NULL,
        `Type` varchar(45) DEFAULT NULL,
        PRIMARY KEY (`Name`)
        )"""

    db_cursor = database.cursor()
    db_cursor.execute(query_string)
    db_cursor.connection.commit()
    insert_ingredients('fresh_ingredients.json', "Fresh")
    insert_ingredients('dairy_ingredients.json', "Dairy")
    insert_ingredients('dry_ingredients.json', "Dry")
    insert_ingredients('tinned_ingredients.json', "Tinned")


if __name__=="__main__":
    main()
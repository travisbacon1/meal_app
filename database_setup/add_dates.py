import os
import mysql.connector
import json

if os.path.isfile('../credentials.txt'):
    with open("../credentials.txt", "r") as reader:
        credentials = reader.readlines()
        credentials = [credential.strip("\n") for credential in credentials]
        reader.close()
else:
    username = input("Enter database user: ")
    password = input("Enter database password: ")

database = mysql.connector.connect(
    host="localhost",
    user=credentials[0],
    password=credentials[1],
    )

query_string = f"SELECT Name FROM MealsDatabase.MealsTable;"
db_cursor = database.cursor(dictionary=True)
db_cursor.execute(query_string)
results = db_cursor.fetchall()
meals = [result['Name'] for result in results]

for meal in meals:
    query_string = f"""UPDATE `MealsDatabase`.`MealsTable` SET `Last_Made` = '2021-4-23' WHERE (`Name` = '{meal}');"""
    db_cursor = database.cursor()
    db_cursor.execute(query_string)
    database.commit()
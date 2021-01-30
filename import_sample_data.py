import os
import mysql.connector
import json

if os.path.isfile('credentials.txt'):
    with open("credentials.txt", "r") as reader:
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

query_string = """CREATE TABLE IF NOT EXISTS `MealsDatabase`.`MealsTable2` (
  `Name` varchar(45) NOT NULL,
  `Staple` varchar(45) DEFAULT NULL,
  `Book` varchar(45) DEFAULT NULL,
  `Page` varchar(45) DEFAULT NULL,
  `Website` varchar(45) DEFAULT NULL,
  `Fresh_Ingredients` json DEFAULT NULL,
  `Tinned_Ingredients` json DEFAULT NULL,
  `Dry_Ingredients` json DEFAULT NULL,
  `Dairy_Ingredients` json DEFAULT NULL,
  PRIMARY KEY (`Name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci"""

db_cursor = database.cursor()
db_cursor.execute(query_string)

query_string = """set global local_infile=true;"""
db_cursor = database.cursor()
db_cursor.execute(query_string)

with open(f"sample_database_data.json","r") as f:
    for line in f:
        line = json.loads(line.replace(',\n','').replace(']','').replace('[',''))
        query_string = f"INSERT IGNORE INTO MealsDatabase.MealsTable(Name, Staple, Book, Page, Website, Fresh_Ingredients, Tinned_Ingredients, Dry_Ingredients, Dairy_Ingredients) VALUES (\"{line['Name']}\", \"{line['Staple']}\", \"{line['Book']}\", \"{line['Page']}\", \"{line['Website']}\", \'{json.dumps(line['Fresh_Ingredients'])}\', \'{json.dumps(line['Tinned_Ingredients'])}\', \'{json.dumps(line['Dry_Ingredients'])}\', \'{json.dumps(line['Dairy_Ingredients'])}\')"
        db_cursor = database.cursor()
        db_cursor.execute(query_string)
        database.commit()
    f.close()

query_string = """set global local_infile=false;"""
db_cursor = database.cursor()
db_cursor.execute(query_string)

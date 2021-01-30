import os
import mysql.connector

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

query_string = """CREATE TABLE IF NOT EXISTS `MealsDatabase`.`MealsTable` (
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
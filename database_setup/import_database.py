import os
import mysql.connector
import json
from dotenv import load_dotenv

load_dotenv()

# if os.path.isfile('../credentials.txt'):
#     with open("../credentials.txt", "r") as reader:
#         credentials = reader.readlines()
#         credentials = [credential.strip("\n") for credential in credentials]
#         reader.close()
# else:
#     username = input("Enter database user: ")
#     password = input("Enter database password: ")

database = mysql.connector.connect(
    host=os.environ['MYSQL_HOSTNAME'],
    user=os.environ['MYSQL_USER'],
    password=os.environ['MYSQL_PASSWORD'],
    database=os.environ['MYSQL_DATABASE']
    )

# query_string = """CREATE TABLE IF NOT EXISTS `MealsTableNew` (
#   `Name` varchar(45) NOT NULL,
#   `Staple` varchar(45) DEFAULT NULL,
#   `Book` varchar(45) DEFAULT NULL,
#   `Page` varchar(45) DEFAULT NULL,
#   `Website` varchar(45) DEFAULT NULL,
#   `Fresh_Ingredients` json DEFAULT NULL,
#   `Tinned_Ingredients` json DEFAULT NULL,
#   `Dry_Ingredients` json DEFAULT NULL,
#   `Dairy_Ingredients` json DEFAULT NULL,
#   `Last_Made` date DEFAULT NULL,
#   `Spring_Summer` tinyint DEFAULT NULL,
#   `Autumn_Winter` tinyint DEFAULT NULL,
#   `Quick_Easy` tinyint DEFAULT NULL,
#   `Special` tinyint DEFAULT NULL,
#   PRIMARY KEY (`Name`)
# ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci"""

# db_cursor = database.cursor()
# db_cursor.execute(query_string)

# query_string = """set global local_infile=true;"""
# db_cursor = database.cursor()
# db_cursor.execute(query_string)

with open(f"../full_database_backup3.json","r") as f:
    for line in f:
        line = json.loads(line.replace(',\n','').replace(']','').replace('[',''))
        query_string = f"INSERT IGNORE INTO {os.environ['MYSQL_DATABASE']}.MealsTableNew(Name, Staple, Book, Page, Website, Fresh_Ingredients, Tinned_Ingredients, Dry_Ingredients, Dairy_Ingredients, Last_Made, Spring_Summer, Autumn_Winter, Quick_Easy, Special) VALUES (\"{line['Name']}\", \"{line['Staple']}\", \"{line['Book']}\", \"{line['Page']}\", \"{line['Website']}\", \'{json.dumps(line['Fresh_Ingredients'])}\', \'{json.dumps(line['Tinned_Ingredients'])}\', \'{json.dumps(line['Dry_Ingredients'])}\', \'{json.dumps(line['Dairy_Ingredients'])}\', \'{line['Last_Made']}\', \'{line['Spring_Summer']}\', \'{line['Autumn_Winter']}\', \'{line['Quick_Easy']}\', \'{line['Special']}\')"
        print(query_string)
        db_cursor = database.cursor()
        db_cursor.execute(query_string)
        database.commit()
    f.close()

# query_string = """set global local_infile=false;"""
# db_cursor = database.cursor()
# db_cursor.execute(query_string)

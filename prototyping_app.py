import inquirer
import os
from os import listdir
import mysql.connector
import json
from tabulate import tabulate
from datetime import datetime
from pprint import pprint


def choice_menu(message, choices):
    question = [
    inquirer.List('choice',
                    message=message,
                    choices=choices,
                    ),
    ]
    answers = inquirer.prompt(question)
    return answers['choice']


def checkbox_choice_menu(message, choices):
    question = [
    inquirer.Checkbox('choices',
                    message=message,
                    choices=choices,
                    ),
    ]
    answers = inquirer.prompt(question)
    return answers['choices']


def load_meal_plan():
    meal_plans = listdir('./saved_meal_plans')
    choice = choice_menu("Choose a saved meal plan", meal_plans)
    
    with open('./saved_meal_plans/'+choice) as json_file:
        complete_ingredient_dict = json.load(json_file)
        json_file.close()

    meals_list = complete_ingredient_dict["Meals"]
    display_meal_plan(meals_list, complete_ingredient_dict)


def database_login():
    with open("credentials.txt", "r") as reader:
        credentials = reader.readlines()
        credentials = [credential.strip("\n") for credential in credentials]
        reader.close()

    database = mysql.connector.connect(
    host="localhost",
    user=credentials[0],
    password=credentials[1],
    database="MealsDatabase"
    )
    return database


def tidy_sql_list(sql_response):
    formatted_list = []
    for item in sql_response:
        item = str(item).strip("('),")
        formatted_list.append(item)
    return formatted_list


def get_staples_list(database, db_cursor):
    sql = "SELECT DISTINCT(Staple) FROM MealsTable;"
    db_cursor.execute(sql)
    myresult = db_cursor.fetchall()
    return myresult


def choose_meals(database, db_cursor, staples_list):
    meals_list = []
    for item in staples_list:
        query = f"SELECT Name FROM MealsTable WHERE Staple = '{item}';"
        db_cursor.execute(query)
        result = db_cursor.fetchall()
        formatted_results = tidy_sql_list(result)
        formatted_results.insert(0, "None") 
        choice = choice_menu(f"Choose a {item} meal", formatted_results)
        meals_list.append(choice)
    return meals_list


def get_meal_info(database, meal_list):
    meal_list = str(meal_list).strip("[]")
    query = f"SELECT * FROM MealsTable WHERE Name in ({meal_list});"
    db_cursor = database.cursor(dictionary=True)
    db_cursor.execute(query)
    result = db_cursor.fetchall()
    return result


def build_ingredient_dictionary(meal_ingredient_dict, deduped_ingredient_dict):
    ingredient_list = json.loads(meal_ingredient_dict)
    for ingredient in list(ingredient_list.keys()):
        if ingredient in deduped_ingredient_dict:
            deduped_ingredient_dict[ingredient] += float(ingredient_list[ingredient])
        else:
            deduped_ingredient_dict[ingredient] = float(ingredient_list[ingredient])
    return deduped_ingredient_dict


def collate_ingredients(meal_info_list):
    fresh_ingredient_dict = {}
    tinned_ingredient_dict = {}
    dry_ingredient_dict = {}
    dairy_ingredient_dict = {}
    for meal in meal_info_list:
        if meal["Fresh_Ingredients"] != None:
            build_ingredient_dictionary(meal["Fresh_Ingredients"], fresh_ingredient_dict)
    
        if meal["Tinned_Ingredients"] != None:
            build_ingredient_dictionary(meal["Tinned_Ingredients"], tinned_ingredient_dict)

        if meal["Dry_Ingredients"] != None:
            build_ingredient_dictionary(meal["Dry_Ingredients"], dry_ingredient_dict)

        if meal["Dairy_Ingredients"] != None:
            build_ingredient_dictionary(meal["Dairy_Ingredients"], dairy_ingredient_dict)
    return fresh_ingredient_dict, tinned_ingredient_dict, dry_ingredient_dict, dairy_ingredient_dict


def save_meal_plan(complete_ingredient_dict):
    if not os.path.exists('saved_meal_plans'):
        os.makedirs('saved_meal_plans')
    dt_string = datetime.now().strftime("%d-%m-%Y %H:%M")
    json_file = json.dumps(complete_ingredient_dict, indent=4)
    with open(f"saved_meal_plans/{dt_string}.json","w") as f:
        f.write(json_file)
        f.close()


def display_meal_plan(meals_list, ingredient_dict):
    print(f"\nChosen meals: {meals_list}")
    print("\n", tabulate(ingredient_dict["Fresh Ingredients"].items(), headers=["Fresh Ingredients", "Quantity"], numalign="right"))
    print("\n", tabulate(ingredient_dict["Tinned Ingredients"].items(), headers=["Tinned Ingredients", "Quantity"], numalign="right"))
    print("\n", tabulate(ingredient_dict["Dry Ingredients"].items(), headers=["Dry Ingredients", "Quantity"], numalign="right"))
    print("\n", tabulate(ingredient_dict["Dairy Ingredients"].items(), headers=["Dairy Ingredients", "Quantity"], numalign="right"))
    print("\n", tabulate(zip(ingredient_dict["Extras"]), headers=["Don't forget!"], numalign="right"))    
    print("\n")


def create_meal_plan(database, db_cursor):
    staples_result = get_staples_list(database, db_cursor)
    formatted_staples_list = tidy_sql_list(staples_result)
    meals_list = choose_meals(database, db_cursor, formatted_staples_list)
    meal_info_list = get_meal_info(database, meals_list)
    fresh_ingredient_dict, tinned_ingredient_dict, dry_ingredient_dict, dairy_ingredient_dict = collate_ingredients(meal_info_list)
    extra_ingredients = checkbox_choice_menu("Do you need any of the following (space bar to toggle)", ['Apples', 'Bananas', 'Grapes', 'Gravy Granules', 'Herbs', 'Mackerel', 'Olive Oil', 'Stuffing', 'Sunflower Oil'])
    
    complete_ingredient_dict = {
        "Meals": meals_list,
        "Fresh Ingredients": fresh_ingredient_dict,
        "Tinned Ingredients": tinned_ingredient_dict,
        "Dry Ingredients": dry_ingredient_dict,
        "Dairy Ingredients": dairy_ingredient_dict,
        "Extras": extra_ingredients
        }


    display_meal_plan(meals_list, complete_ingredient_dict)
    choice = choice_menu("Would you like to save this meal plan?", ['Yes', 'No'])
    if choice == "Yes":
        print("Saving meal plan")
        save_meal_plan(complete_ingredient_dict)
        print("Meal plan saved. Very good Ma'am")
    else:
        print("Very good Ma'am")


def list_meals(database, db_cursor):
    query = f"SELECT Name, Book, Page, Website FROM MealsTable;"
    db_cursor = database.cursor(dictionary=True)
    db_cursor.execute(query)
    result = db_cursor.fetchall()
    meal_details_list = []
    for item in result:
        meal_details = [item['Name'], item['Book'], item['Page'], item['Website']]
        meal_details_list.append(meal_details)

    print("\n", tabulate(meal_details_list, headers=["Name", "Book", "Page", "Website"], numalign="right", tablefmt="grid"))


def get_single_meal_info(database, db_cursor):
    query = f"SELECT Name FROM MealsTable;"
    db_cursor.execute(query)
    result = db_cursor.fetchall()
    formatted_results = tidy_sql_list(result)
    choice = choice_menu("Which meal would you like details for?", formatted_results)
    query = f"SELECT * FROM MealsTable WHERE Name = '{choice}';"
    db_cursor = database.cursor(dictionary=True)
    db_cursor.execute(query)
    result = db_cursor.fetchall()

    meal_details_dict = {
        "Book": result[0]['Book'],
        "Page": result[0]['Page'],
        "Website": result[0]['Website'],
        "Fresh_Ingredients": json.loads(result[0]['Fresh_Ingredients']),
        "Tinned_Ingredients": json.loads(result[0]['Tinned_Ingredients']),
        "Dry_Ingredients": json.loads(result[0]['Dry_Ingredients']),
        "Dairy_Ingredients": json.loads(result[0]['Dairy_Ingredients']),        
    }
    pprint(meal_details_dict, sort_dicts=False)


def main():
    choice = choice_menu("What would you like to do?", ['Create Meal Plan', 'Load Meal Plan', 'List Meals', 'Get Meal Info'])
    if choice == "Load Meal Plan":
        load_meal_plan()
    else:
        database = database_login()
        db_cursor = database.cursor()
        if database:
            print("Log in successful")
        else:
            print("Log in failed, please try again")
            exit()
        if choice == "Create Meal Plan":
            create_meal_plan(database, db_cursor)
        elif choice == "List Meals":
            list_meals(database, db_cursor)
        elif choice == "Get Meal Info":
            get_single_meal_info(database, db_cursor)
        else:
            print("Option not yet available, exiting app")
            exit()


if __name__ == "__main__":
    main()
        


from flask import Blueprint, redirect, url_for, render_template, request, session
import os
import json
from datetime import datetime
from ..variables import fresh_ingredients_dict, tinned_ingredients_dict, dry_ingredients_dict, dairy_ingredients_dict
from .. import mysql
from ..utilities import execute_mysql_query
from datetime import datetime

display = Blueprint('display', __name__, template_folder='templates', static_folder='../static')

def save_meal_plan(complete_ingredient_dict) -> str:
    """Saves created meal plan to the local saved_meal_plans directory

    Parameters
    ----------
    complete_ingredient_dict : dict

    Returns
    -------
    str
        File path to saved meal plan
    """
    if not os.path.exists('saved_meal_plans'):
        os.makedirs('saved_meal_plans')
    dt_string = datetime.now().strftime("%Y-%m-%d %H:%M")
    json_file = json.dumps(complete_ingredient_dict, indent=4)
    with open(f"saved_meal_plans/{dt_string}.json","w") as f:
        f.write(json_file)
    file_path = str(os.getcwd()) + f"/saved_meal_plans/{dt_string}.json"
    return file_path


def create_meal_info_table(meal_info_tuple) -> list[dict]:
    """Creates a list of meal info dictionaries

    Parameters
    ----------
    meal_info_tuple : list[tuple]

    Returns
    -------
    list[dict]
        List of meal dictionaries
    """
    meal_list_dicts = [meal for meal in meal_info_tuple]
    meal_info_dicts = [{'Name': meal['Name'], 'Info': f"{meal['Book']}, page {meal['Page']}"} if meal['Website'] == "" else {'Name': meal['Name'], 'Info': meal['Website']} for meal in meal_list_dicts]
    return meal_info_dicts


def append_ingredient_units(ingredients_dict, ingredients_units_list) -> dict:
    """Appends unit ingredients (i.e. g or ml) to ingredient dictionary

    Parameters
    ----------
    ingredients_dict : dict
    ingredients_units_list : list[dict]

    Returns
    -------
    dict
        Ingredient dictionary containing units
    """
    ingredients_with_units = {key: f"{str(value)} {str(ingredients_units_list[key])}" if key in list(ingredients_units_list.keys()) else '' for key, value in ingredients_dict.items()}
    return ingredients_with_units


@display.route('/display', methods=['GET', 'POST'])
def display_meal_plan():
    if request.method == "GET":
        complete_ingredient_dict = session.pop('complete_ingredient_dict')
        session['complete_ingredient_dict'] = complete_ingredient_dict
        meal_list_string = str(complete_ingredient_dict['Meal_List']).strip("[]")
        query_string = f"SELECT Name, Book, Page, Website FROM MealsDatabase.MealsTable WHERE Name IN ({meal_list_string});"
        results = execute_mysql_query(query_string)
        info_meal_dict = create_meal_info_table(results)
        fresh_ingredients = append_ingredient_units(complete_ingredient_dict['Fresh_Ingredients'], fresh_ingredients_dict)
        tinned_ingredients = append_ingredient_units(complete_ingredient_dict['Tinned_Ingredients'], tinned_ingredients_dict)
        dry_ingredients = append_ingredient_units(complete_ingredient_dict['Dry_Ingredients'], dry_ingredients_dict)
        dairy_ingredients = append_ingredient_units(complete_ingredient_dict["Dairy_Ingredients"], dairy_ingredients_dict)
        return render_template('display.html',
                            len_meal_info_list = len(info_meal_dict), meal_info_list=info_meal_dict,
                            len_fresh_ingredients = len(list(fresh_ingredients.keys())), fresh_ingredients_keys=list(fresh_ingredients.keys()), fresh_ingredients_values=list(fresh_ingredients.values()),
                            len_tinned_ingredients = len(list(tinned_ingredients.keys())), tinned_ingredients_keys=list(tinned_ingredients.keys()), tinned_ingredients_values=list(tinned_ingredients.values()),
                            len_dry_ingredients = len(list(dry_ingredients.keys())), dry_ingredients_keys=list(dry_ingredients.keys()), dry_ingredients_values=list(dry_ingredients.values()),
                            len_dairy_ingredients = len(list(dairy_ingredients.keys())), dairy_ingredients_keys=list(dairy_ingredients.keys()), dairy_ingredients_values=list(dairy_ingredients.values()),
                            len_extra_ingredients = len(complete_ingredient_dict['Extra_Ingredients']), extra_ingredients=complete_ingredient_dict['Extra_Ingredients'])

    if request.method == "POST":
        complete_ingredient_dict = session.pop('complete_ingredient_dict')
        session['complete_ingredient_dict'] = complete_ingredient_dict
        if request.form['submit'] == 'Save':
            file_path = save_meal_plan(complete_ingredient_dict)
            return render_template('save_complete.html', file_path = file_path)
        if request.form['submit'] == 'Update Dates':
            date_now = datetime.now().strftime("%Y-%-m-%d")
            meals = complete_ingredient_dict['Meal_List']
            for meal in meals:
                query_string = f"""UPDATE `MealsDatabase`.`MealsTable` SET `Last_Made` = '{date_now}' WHERE (`Name` = '{meal}');"""
                cur = mysql.connection.cursor()
                cur.execute(query_string)
                mysql.connection.commit()
                cur.close()
            return redirect(url_for('display.display_meal_plan'))
from flask import Blueprint, redirect, url_for, render_template, request, session
import os
import json
from datetime import datetime

display = Blueprint('display', __name__, template_folder='templates', static_folder='../static')

def save_meal_plan(complete_ingredient_dict):
    """Saves created meal plan to the local saved_meal_plans directory
    
    Parameters
    -------
    complete_ingredient_dict: dict

    Returns
    ------
    file_path: string
    """
    if not os.path.exists('saved_meal_plans'):
        os.makedirs('saved_meal_plans')
    dt_string = datetime.now().strftime("%Y-%m-%d %H:%M")
    json_file = json.dumps(complete_ingredient_dict, indent=4)
    with open(f"saved_meal_plans/{dt_string}.json","w") as f:
        f.write(json_file)
        f.close()
    file_path = str(os.getcwd()) + f"/saved_meal_plans/{dt_string}.json"
    return file_path

def create_meal_info_table(meal_info_tuple):
    """Creates a nested list of meal information for rendering in display.html 
    
    Parameters
    -------
    meal_info_tuple: tuple

    Returns
    ------
    meal_list_dicts: list
    """
    meal_list_dicts = [meal for meal in meal_info_tuple]
    meal_info_list = [[meal['Name'], f"{meal['Book']}, page {meal['Page']}"] if meal['Website'] == "" else [meal['Name'], meal['Website']] for meal in meal_list_dicts]
    return meal_info_list


def append_ingredient_units(fresh_ingredients, tinned_ingredients, dry_ingredients, dairy_ingredients):
    """Appends unit ingredients (i.e. g or ml) to ingredients
    
    Parameters
    -------
    fresh_ingredients: list\n
    tinned_ingredients: list\n
    dry_ingredients: list\n
    dairy_ingredients: list\n

    Returns
    ------
    fresh_ingredients: list\n
    tinned_ingredients: list\n
    dry_ingredients: list\n
    dairy_ingredients: list\n
    """
    from ..variables import gram_list
    fresh_ingredients[1] = [str(fresh_ingredients[1][idx]) + " g" if fresh_ingredients[0][idx] in gram_list else str(fresh_ingredients[1][idx]) for idx, _ in enumerate(fresh_ingredients[1])]
    tinned_ingredients[1] = [str(tinned_ingredients[1][idx]) + " g" if tinned_ingredients[0][idx] in gram_list else str(tinned_ingredients[1][idx]) + " tin" if tinned_ingredients[1][idx] <= 1 else str(tinned_ingredients[1][idx]) + " tins" for idx, _ in enumerate(tinned_ingredients[1])]
    dry_ingredients[1] = [str(dry_ingredients[1][idx]) + " g" if dry_ingredients[0][idx] in gram_list else str(dry_ingredients[1][idx]) for idx, _ in enumerate(dry_ingredients[1])]
    dairy_ingredients[1] = [str(dairy_ingredients[1][idx]) + " g" if dairy_ingredients[0][idx] in gram_list else str(dairy_ingredients[1][idx]) + " ml" if str(dairy_ingredients[0][idx]) == 'Milk' else str(dairy_ingredients[1][idx]) for idx, _ in enumerate(dairy_ingredients[1])]
    return fresh_ingredients, tinned_ingredients, dry_ingredients, dairy_ingredients


@display.route('/display', methods=['GET', 'POST'])
def display_meal_plan():
    if request.method == "GET":
        from ..utilities import execute_mysql_query
        complete_ingredient_dict = session.pop('complete_ingredient_dict')
        session['complete_ingredient_dict'] = complete_ingredient_dict
        meal_list_string = str(complete_ingredient_dict['Meal_List']).strip("[]")
        query_string = f"SELECT Name, Book, Page, Website FROM MealsDatabase.MealsTable WHERE Name IN ({meal_list_string});"
        results = execute_mysql_query(query_string)
        info_meal_list = create_meal_info_table(results)
        fresh_ingredients = [list(complete_ingredient_dict["Fresh_Ingredients"].keys()), list(complete_ingredient_dict["Fresh_Ingredients"].values())]
        tinned_ingredients = [list(complete_ingredient_dict["Tinned_Ingredients"].keys()), list(complete_ingredient_dict["Tinned_Ingredients"].values())]
        dry_ingredients = [list(complete_ingredient_dict["Dry_Ingredients"].keys()), list(complete_ingredient_dict["Dry_Ingredients"].values())]
        dairy_ingredients = [list(complete_ingredient_dict["Dairy_Ingredients"].keys()), list(complete_ingredient_dict["Dairy_Ingredients"].values())]
        fresh_ingredients, tinned_ingredients, dry_ingredients, dairy_ingredients = append_ingredient_units(fresh_ingredients, tinned_ingredients, dry_ingredients, dairy_ingredients)
        return render_template('display.html',
                            len_meal_info_list = len(info_meal_list), meal_info_list=info_meal_list,
                            len_fresh_ingredients = len(fresh_ingredients[0]), fresh_ingredients_keys=fresh_ingredients[0], fresh_ingredients_values=fresh_ingredients[1],
                            len_tinned_ingredients = len(tinned_ingredients[0]), tinned_ingredients_keys=tinned_ingredients[0], tinned_ingredients_values=tinned_ingredients[1],
                            len_dry_ingredients = len(dry_ingredients[0]), dry_ingredients_keys=dry_ingredients[0], dry_ingredients_values=dry_ingredients[1],
                            len_dairy_ingredients = len(dairy_ingredients[0]), dairy_ingredients_keys=dairy_ingredients[0], dairy_ingredients_values=dairy_ingredients[1],
                            len_extra_ingredients = len(complete_ingredient_dict['Extra_Ingredients']), extra_ingredients=complete_ingredient_dict['Extra_Ingredients'])

    if request.method == "POST":
        complete_ingredient_dict = session.pop('complete_ingredient_dict')
        session['complete_ingredient_dict'] = complete_ingredient_dict
        if request.form['submit'] == 'Save':
            file_path = save_meal_plan(complete_ingredient_dict)
            return render_template('save_complete.html', file_path = file_path)
        if request.form['submit'] == 'Update Dates':
            from .. import mysql
            from datetime import datetime
            date_now = datetime.now().strftime("%Y-%-m-%d")
            meals = complete_ingredient_dict['Meal_List']
            for meal in meals:
                query_string = f"""UPDATE `MealsDatabase`.`MealsTable` SET `Last_Made` = '{date_now}' WHERE (`Name` = '{meal}');"""
                cur = mysql.connection.cursor()
                cur.execute(query_string)
                mysql.connection.commit()
                cur.close()
            return redirect(url_for('display.display_meal_plan'))
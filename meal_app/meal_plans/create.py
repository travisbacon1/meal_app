from flask import Blueprint, render_template, request, redirect, url_for, session
from ..utilities import execute_mysql_query
from ..variables import extras
import json
import os

create = Blueprint('create', __name__, template_folder='templates', static_folder='static')

def get_meal_info(meal_list, quantity_list) -> list[dict]:
    """Converts a list of meals into a string and uses this in an SQL query to get the information on these meals (ingredients not yet de-duped)

    Parameters
    ----------
    meal_list : list[dict]
    quantity_list : list[int]

    Returns
    -------
    list[dict]
        MySQL results
    """
    results = []
    for idx, meal in enumerate(meal_list):
        query_string = f"SELECT Fresh_Ingredients, Tinned_Ingredients, Dry_Ingredients, Dairy_Ingredients FROM {os.environ['MYSQL_DATABASE']}.{os.environ['MYSQL_TABLE']} WHERE Name = '{meal}';"
        ingredients = execute_mysql_query(query_string)
        for ingredient_type in list(ingredients[0].keys()):
            ingredients[0][ingredient_type] = json.loads(ingredients[0][ingredient_type])
        ingredients[0]['quantity'] = quantity_list[idx]
        results.append(ingredients[0])
    return results


def quantity_adjustment(meal_list_dict) -> list[dict]:
    """Adjusts each meal's ingredients by the associated quantities

    Parameters
    ----------
    meal_list_dict : list[dict]

    Returns
    -------
    list[dict]
        List of each meal's ingredients with the adjusted quantities
    """
    for meal in meal_list_dict:
        for ingredient_type in list(meal.keys()):
            if ingredient_type != 'quantity':
                meal[ingredient_type].update((k, float(v) * meal['quantity']) for k,v in meal[ingredient_type].items())
        del meal['quantity']
    return meal_list_dict


def build_ingredient_dictionary(meal_ingredient_dict, complete_ingredient_dict, ingredient_type) -> dict:
    """Adds together the quantities of all ingredients in a given deduped_ingredient_dict

    Parameters
    ----------
    meal_ingredient_dict : dict
    complete_ingredient_dict : dict
    ingredient_type : str

    Returns
    -------
    dict
        Single dictionary containing all ingredients for meal plan
    """
    for ingredient in meal_ingredient_dict:
        if ingredient in complete_ingredient_dict[ingredient_type]:
            complete_ingredient_dict[ingredient_type][ingredient] += float(meal_ingredient_dict[ingredient])
        else:
            complete_ingredient_dict[ingredient_type][ingredient] = float(meal_ingredient_dict[ingredient])
        complete_ingredient_dict[ingredient_type][ingredient] = int(complete_ingredient_dict[ingredient_type][ingredient]) if complete_ingredient_dict[ingredient_type][ingredient].is_integer() else complete_ingredient_dict[ingredient_type][ingredient]
    return complete_ingredient_dict


def collate_ingredients(meal_info_list) -> dict:
    """Collates all ingredients from all meals into a dictionary of required ingredients

    Parameters
    ----------
    meal_info_list : list[dict]

    Returns
    -------
    dict
        Single dictionary containing all ingredients for meal plan
    """
    complete_ingredient_dict = {ingredient_type: {} for ingredient_type in meal_info_list[0].keys()}
    for meal in meal_info_list:
        for ingredient_type in meal.keys():
            if meal[ingredient_type]:
                build_ingredient_dictionary(meal[ingredient_type], complete_ingredient_dict, ingredient_type)
    return complete_ingredient_dict


@create.route('/create', methods=['GET', 'POST'])
def create_meal_plan():
    query_string = f"SELECT GROUP_CONCAT(Name ORDER BY Name ASC) as Meals, Staple FROM {os.environ['MYSQL_DATABASE']}.{os.environ['MYSQL_TABLE']} GROUP BY Staple;"
    results = execute_mysql_query(query_string)
    staples_dict = {str(item['Staple']): list(item['Meals'].split(',')) for item in results}
    if request.method == "POST":
        details_dict = request.form.to_dict()
        meal_list = [value for key, value in details_dict.items() if 'Meal' in key and value != 'null']
        quantity_list = [int(value) for key, value in details_dict.items() if 'Quantity' in key and value != 'null']
        complete_ingredient_dict = collate_ingredients(quantity_adjustment(get_meal_info(meal_list, quantity_list)))
        complete_ingredient_dict['Extra_Ingredients'] = [value for key, value in details_dict.items() if 'Extra' in key]
        complete_ingredient_dict['Meal_List'] = [meal for meal in meal_list if meal != 'null']
        session['complete_ingredient_dict'] = complete_ingredient_dict
        return redirect(url_for('display.display_meal_plan'))
    return render_template('create.html', staples=list(staples_dict.keys()), staples_dict=staples_dict, extras=extras)
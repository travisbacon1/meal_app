from flask import Blueprint, render_template, request, redirect, url_for, session
from .. import mysql
import json

create = Blueprint('create', __name__, template_folder='templates', static_folder='static')

def parse_ingredients(ingredients_dict, filter_word):
    """Parses an ingredients dictionary to create a new dictionary based on the filter_word as the key
    
    Parameters
    -------
    ingredients_dict: dict\n
    filter_word: string

    Returns
    ------
    parsed_ingredient_dict: dict
    """
    parsed_ingredient_dict = {}
    for key in list(ingredients_dict.keys()):
        if filter_word in key and ingredients_dict[key] != '':
            new_key = key.removeprefix(filter_word)
            parsed_ingredient_dict[new_key] = ingredients_dict[key]
    return json.dumps(parsed_ingredient_dict)


def get_meal_info(meal_list):
    """Converts a list of meals into a string and uses this in an SQL query to get the information on these meals (ingredients not yet de-duped)
    
    Parameters
    -------
    meal_list: list\n

    Returns
    ------
    result: tuple
    """
    meal_list = str(meal_list).strip("[]")
    db_cursor = mysql.connection.cursor()
    query = f"SELECT Fresh_Ingredients, Tinned_Ingredients, Dry_Ingredients, Dairy_Ingredients FROM MealsDatabase.MealsTable WHERE Name IN ({meal_list});"
    db_cursor.execute(query)
    results = db_cursor.fetchall()
    return results


def quantity_adjustment(meal_list_dict, quantity_list):
    meal_list_dict_converted = []
    for meal in meal_list_dict:
        meal['Fresh_Ingredients'] = json.loads(meal['Fresh_Ingredients'])
        meal['Tinned_Ingredients'] = json.loads(meal['Tinned_Ingredients'])
        meal['Dry_Ingredients'] = json.loads(meal['Dry_Ingredients'])
        meal['Dairy_Ingredients'] = json.loads(meal['Dairy_Ingredients'])
        meal_list_dict_converted.append(meal)
    for idx, meal in enumerate(meal_list_dict_converted):
        meal['Fresh_Ingredients'].update((k, float(v) * quantity_list[idx]) for k,v in meal['Fresh_Ingredients'].items())
        meal['Tinned_Ingredients'].update((k, float(v) * quantity_list[idx]) for k,v in meal['Tinned_Ingredients'].items())
        meal['Dry_Ingredients'].update((k, float(v) * quantity_list[idx]) for k,v in meal['Dry_Ingredients'].items())
        meal['Dairy_Ingredients'].update((k, float(v) * quantity_list[idx]) for k,v in meal['Dairy_Ingredients'].items())
    return meal_list_dict_converted


def build_ingredient_dictionary(meal_ingredient_dict, deduped_ingredient_dict):
    """Adds together the quantities of all ingredients in a given deduped_ingredient_dict
    
    Parameters
    -------
    meal_ingredient_dict: dict\n
    deduped_ingredient_dict: dict\n

    Returns
    ------
    deduped_ingredient_dict: dict
    """
    for ingredient in list(meal_ingredient_dict.keys()):
        if ingredient in deduped_ingredient_dict:
            deduped_ingredient_dict[ingredient] += float(meal_ingredient_dict[ingredient])
            deduped_ingredient_dict[ingredient] = round(deduped_ingredient_dict[ingredient], 2)
            deduped_ingredient_dict[ingredient] = int(deduped_ingredient_dict[ingredient]) if deduped_ingredient_dict[ingredient].is_integer() else deduped_ingredient_dict[ingredient]
        else:
            deduped_ingredient_dict[ingredient] = float(meal_ingredient_dict[ingredient])
            deduped_ingredient_dict[ingredient] = round(deduped_ingredient_dict[ingredient], 2)
            deduped_ingredient_dict[ingredient] = int(deduped_ingredient_dict[ingredient]) if deduped_ingredient_dict[ingredient].is_integer() else deduped_ingredient_dict[ingredient]
    return deduped_ingredient_dict


def collate_ingredients(meal_info_list, quantity_list):
    """Collates all ingredients from all meals into a dictionary of required ingredients
    
    Parameters
    -------
    meal_info_list: list

    Returns
    ------
    complete_deduped_ingredient_dict: dict
    """
    complete_deduped_ingredient_dict = {}
    fresh_ingredient_dict = {}
    tinned_ingredient_dict = {}
    dry_ingredient_dict = {}
    dairy_ingredient_dict = {}
    for idx, meal in enumerate(meal_info_list):
        if meal["Fresh_Ingredients"] != None:
            build_ingredient_dictionary(meal["Fresh_Ingredients"], fresh_ingredient_dict)
    
        if meal["Tinned_Ingredients"] != None:
            build_ingredient_dictionary(meal["Tinned_Ingredients"], tinned_ingredient_dict)

        if meal["Dry_Ingredients"] != None:
            build_ingredient_dictionary(meal["Dry_Ingredients"], dry_ingredient_dict)

        if meal["Dairy_Ingredients"] != None:
            build_ingredient_dictionary(meal["Dairy_Ingredients"], dairy_ingredient_dict)

        if meal["Dairy_Ingredients"] != None:
            build_ingredient_dictionary(meal["Dairy_Ingredients"], dairy_ingredient_dict)
    complete_deduped_ingredient_dict["Fresh_Ingredients"] = fresh_ingredient_dict
    complete_deduped_ingredient_dict["Tinned_Ingredients"] = tinned_ingredient_dict
    complete_deduped_ingredient_dict["Dry_Ingredients"] = dry_ingredient_dict
    complete_deduped_ingredient_dict["Dairy_Ingredients"] = dairy_ingredient_dict
    return complete_deduped_ingredient_dict


@create.route('/create', methods=['GET', 'POST'])
def create_meal_plan():
    db_cursor = mysql.connection.cursor()
    query = f"SELECT GROUP_CONCAT(Name ORDER BY Name ASC) as Meals, Staple FROM MealsDatabase.MealsTable GROUP BY Staple;"
    db_cursor.execute(query)
    results = db_cursor.fetchall()
    staples_dict = {str(item['Staple']): list(item['Meals'].split(',')) for item in results}

    if request.method == "POST":
        details = request.form
        details_dict = details.to_dict()
        meal_list = [value for key, value in details_dict.items() if 'Meal' in key]
        quantity_list = [int(value) for key, value in details_dict.items() if 'Quantity' in key and value != 'null']
        meal_tuple = get_meal_info(meal_list)
        meal_list_dicts = [meal for meal in meal_tuple]
        meal_list_dicts = quantity_adjustment(meal_list_dicts, quantity_list)
        complete_ingredient_dict = collate_ingredients(meal_list_dicts, quantity_list)
        complete_ingredient_dict['Extra_Ingredients'] = [value for key, value in details_dict.items() if 'Extra' in key]
        complete_ingredient_dict['Meal_List'] = [meal for meal in meal_list if meal != 'null']
        session['complete_ingredient_dict'] = complete_ingredient_dict
        return redirect(url_for('display.display_meal_plan'))
    from ..variables import extras
    return render_template('create.html',
                            len_bean_meals=len(staples_dict['Beans']), bean_meals=staples_dict['Beans'],
                            len_bread_meals=len(staples_dict['Bread']), bread_meals=staples_dict['Bread'],
                            len_cereal_meals=len(staples_dict['Cereal']), cereal_meals=staples_dict['Cereal'],
                            len_cous_cous_meals=len(staples_dict['Cous Cous']), cous_cous_meals=staples_dict['Cous Cous'],
                            len_noodle_meals=len(staples_dict['Noodles']), noodle_meals=staples_dict['Noodles'],
                            len_orzo_meals=len(staples_dict['Orzo']), orzo_meals=staples_dict['Orzo'],
                            len_pasta_meals=len(staples_dict['Pasta']), pasta_meals=staples_dict['Pasta'],
                            len_potato_meals=len(staples_dict['Potato']), potato_meals=staples_dict['Potato'],
                            len_rice_meals=len(staples_dict['Rice']), rice_meals=staples_dict['Rice'],
                            len_risotto_meals=len(staples_dict['Risotto']), risotto_meals=staples_dict['Risotto'],
                            len_extras = len(extras), extras = extras)
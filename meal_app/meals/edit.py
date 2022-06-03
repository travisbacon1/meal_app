from flask import Blueprint, render_template, request, redirect, url_for
import json
from ..utilities import execute_mysql_query, parse_ingredients, get_tag_keys, get_tags
import os

edit = Blueprint('edit', __name__, template_folder='templates', static_folder='../static')

def append_current_ingredients(dict_1, dict_2):
    current_ingredients = list(dict_2.keys())
    for idx, ingredient_dict in enumerate(dict_1):
        try:
            current_ingredients.index(ingredient_dict['Ingredient'])
            dict_1[idx]['Quantity'] = (dict_2[ingredient_dict['Ingredient']])
        except ValueError:
            pass
    return dict_1

def unpack_ingredients(ingredients):
    current_ingredients = json.loads(ingredients)
    current_ingredients_keys = list(current_ingredients.keys())
    return current_ingredients, current_ingredients_keys


def unpack_ingredient_key_values(ingredients):
    # TODO: Combine this with unpack_ingredients method
    return [list(json.loads(ingredients).keys()), list(json.loads(ingredients).values())]


def get_ingredients() -> dict:
    """Appends unit ingredients (i.e. g or ml) to ingredient dictionary

    Parameters
    ----------
    ingredient_dict : dict

    Returns
    -------
    dict
        Ingredient dictionary containing units
    """
    ingredient_dict = {}
    for ingredient_type in ["Fresh", "Dairy", "Dry", "Tinned"]:
        query_string = f"SELECT Name, Unit FROM {os.environ['MYSQL_DATABASE']}.{os.environ['MYSQL_INGREDIENTS_TABLE']} WHERE Type = '{ingredient_type}');"
        results = execute_mysql_query(query_string)
        for ingredient in results:
            temp_dict = {ingredient['Name']: ingredient['Unit']}
            ingredient_dict[f'{ingredient_type}_Ingredients'].update(temp_dict)
    return ingredient_dict


@edit.route('/edit', methods=['GET', 'POST'])
def index():
    query_string = f"SELECT Name FROM {os.environ['MYSQL_DATABASE']}.{os.environ['MYSQL_TABLE']};"
    results = execute_mysql_query(query_string)
    meals = [result['Name'] for result in results]
    if request.method == "POST":
        details = request.form
        query_string = f"SELECT * FROM {os.environ['MYSQL_DATABASE']}.{os.environ['MYSQL_TABLE']} WHERE Name='{details['Meal']}';"
        results = execute_mysql_query(query_string)
        return redirect(url_for('edit.edit_meal', meal=results[0]['Name']))
    return render_template('edit_list.html', meals=meals)


@edit.route('/edit/<meal>', methods=['GET', 'POST'])
def edit_meal(meal):
    from ..variables import staples_list, book_list, fresh_ingredients, tinned_ingredients, dry_ingredients, dairy_ingredients, tag_list
    if request.method == "GET":
        query_string = f"SELECT * FROM {os.environ['MYSQL_DATABASE']}.{os.environ['MYSQL_TABLE']} WHERE Name = '{meal}';"
        results = execute_mysql_query(query_string)[0]
        current_meal_data = execute_mysql_query(query_string)[0]
        # query_string = f"SELECT Type, JSON_OBJECTAGG(Name, Unit)  AS Ingredients FROM {os.environ['MYSQL_DATABASE']}.{os.environ['MYSQL_INGREDIENTS_TABLE']} GROUP BY Type;"
        query_string = f"""
                        SELECT
                            Type,
                            JSON_ARRAYAGG(
                                JSON_OBJECT(
                                    'Ingredient', Name,
                                    'Unit', Unit,
                                    'Quantity', "")
                                )
                                AS Ingredient_data
                        FROM {os.environ['MYSQL_DATABASE']}.{os.environ['MYSQL_INGREDIENTS_TABLE']}
                        GROUP BY Type;"""
        all_ingredient_data = execute_mysql_query(query_string)
        current_ingredients = {}
        for ingredient_type in all_ingredient_data:
            current_ingredients[ingredient_type['Type']] = append_current_ingredients(json.loads(ingredient_type['Ingredient_data']), json.loads(current_meal_data[f'{ingredient_type["Type"]}_Ingredients']))
        current_fresh_ingredients, current_fresh_ingredients_keys = unpack_ingredients(results['Fresh_Ingredients'])
        current_tinned_ingredients, current_tinned_ingredients_keys = unpack_ingredients(results['Tinned_Ingredients'])
        current_dry_ingredients, current_dry_ingredients_keys = unpack_ingredients(results['Dry_Ingredients'])
        current_dairy_ingredients, current_dairy_ingredients_keys = unpack_ingredients(results['Dairy_Ingredients'])
        current_dairy_ingredients_keys = list(current_dairy_ingredients.keys())
        current_tags = [results['Spring_Summer'], results['Autumn_Winter'], results['Quick_Easy'], results['Special']]

        return render_template('edit_meal.html', meal_name = results['Name'], staple = results['Staple'], book = results['Book'], page = results['Page'], website = results['Website'],
            current_ingredients=current_ingredients,
            current_fresh_ingredients = current_fresh_ingredients, current_fresh_ingredients_keys = current_fresh_ingredients_keys, 
            current_tinned_ingredients = current_tinned_ingredients, current_tinned_ingredients_keys = current_tinned_ingredients_keys, 
            current_dry_ingredients = current_dry_ingredients, current_dry_ingredients_keys = current_dry_ingredients_keys, 
            current_dairy_ingredients = current_dairy_ingredients, current_dairy_ingredients_keys = current_dairy_ingredients_keys, 
            staples = staples_list,
            books = book_list,
            fresh_ingredients = [ingredient[0] for ingredient in fresh_ingredients], fresh_ingredients_units = [ingredient[1] for ingredient in fresh_ingredients],
            tinned_ingredients = [ingredient[0] for ingredient in tinned_ingredients], tinned_ingredients_units = [ingredient[1] for ingredient in tinned_ingredients],
            dry_ingredients = [ingredient[0] for ingredient in dry_ingredients], dry_ingredients_units = [ingredient[1] for ingredient in dry_ingredients],
            dairy_ingredients = [ingredient[0] for ingredient in dairy_ingredients], dairy_ingredients_units = [ingredient[1] for ingredient in dairy_ingredients],
            tags = tag_list,
            current_tags = current_tags)
    if request.method == "POST":
        details = request.form
        details_dict = details.to_dict()
        fresh_ing = parse_ingredients(details_dict, "Fresh ")
        tinned_ing = parse_ingredients(details_dict, "Tinned ")
        dry_ing = parse_ingredients(details_dict, "Dry ")
        dairy_ing = parse_ingredients(details_dict, "Dairy ")
        tag_list = []
        for key in list(details_dict.keys()):
            if 'Tag' in key:
                tag_list.append(details_dict[key])
        tags = get_tags(tag_list)
        query_string = f"UPDATE {os.environ['MYSQL_DATABASE']}.{os.environ['MYSQL_TABLE']} SET Name = '{details['Name']}', Staple = '{details['Staple']}', Book = '{details['Book']}', Page = '{details['Page']}', Website = '{details['Website']}', Fresh_Ingredients = '{fresh_ing}', Tinned_Ingredients = '{tinned_ing}', Dry_Ingredients = '{dry_ing}', Dairy_Ingredients = '{dairy_ing}', Spring_Summer = {tags['Spring_Summer']}, Autumn_Winter = {tags['Autumn_Winter']}, Quick_Easy = {tags['Quick_Easy']}, Special = {tags['Special']} WHERE (Name = '{details['Name']}');"
        print(query_string)
        execute_mysql_query(query_string, fetch_results=False, commit=True)
        return redirect(url_for('edit.confirmation', meal=meal))


@edit.route('/edit_confirmation/<meal>', methods=['GET', 'POST'])
def confirmation(meal):
    if request.method == "GET":
        query_string = f"SELECT * FROM {os.environ['MYSQL_DATABASE']}.{os.environ['MYSQL_TABLE']} WHERE Name='{meal}';"
        result = execute_mysql_query(query_string)[0]
        print(result)
        location_details = {}
        if result['Website'] == None or result['Website'] == '':
            location_details['Book'] = result['Book']
            location_details['Page'] = result['Page']
        else:
            location_details['Website'] = result['Website']
        fresh_ingredients = unpack_ingredient_key_values(result['Fresh_Ingredients'])
        tinned_ingredients = unpack_ingredient_key_values(result['Tinned_Ingredients'])
        dry_ingredients = unpack_ingredient_key_values(result['Dry_Ingredients'])
        dairy_ingredients = unpack_ingredient_key_values(result['Dairy_Ingredients'])
        tags = [{"Spring/Summer": result['Spring_Summer']}, {"Autumn/Winter": result['Autumn_Winter']}, {"Quick/Easy": result['Quick_Easy']}, {"Special": result['Special']}]
        tags = get_tag_keys(tags)
        return render_template('edit_confirmation.html', meal_name=meal,
                                location_details=location_details, location_keys=location_details.keys(),
                                staple=result['Staple'],
                                len_fresh_ingredients=len(fresh_ingredients[0]), fresh_ingredients_keys=fresh_ingredients[0], fresh_ingredients_values=fresh_ingredients[1],
                                len_tinned_ingredients=len(tinned_ingredients[0]), tinned_ingredients_keys=tinned_ingredients[0], tinned_ingredients_values=tinned_ingredients[1],
                                len_dry_ingredients=len(dry_ingredients[0]), dry_ingredients_keys=dry_ingredients[0], dry_ingredients_values=dry_ingredients[1],
                                len_dairy_ingredients=len(dairy_ingredients[0]), dairy_ingredients_keys=dairy_ingredients[0], dairy_ingredients_values=dairy_ingredients[1],
                                len_tags=len(tags), tags=tags)
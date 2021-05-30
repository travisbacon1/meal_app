from flask import Blueprint, render_template, request, redirect, url_for
import json
from ..utilities import execute_mysql_query

edit = Blueprint('edit', __name__, template_folder='templates', static_folder='../static')

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
            new_key = key.strip(filter_word)
            parsed_ingredient_dict[new_key] = ingredients_dict[key]
    return json.dumps(parsed_ingredient_dict)


def get_tag_keys(tags):
    tag_list = []
    for tag_dict in tags:
        if list(tag_dict.values())[0] == 1:
            tag_list.append(list(tag_dict.keys())[0])
    return tag_list


def get_tags(tags):
    from ..variables import tag_list, tag_list_backend
    parsed_tags = {}
    for tag in tag_list:
        if tag in tags:
            parsed_tags[tag.replace('/', '_')] = "1"
        else:
            parsed_tags[tag.replace('/', '_')] = "0"
    return parsed_tags


@edit.route('/edit', methods=['GET', 'POST'])
def index():
    from .. import mysql
    query_string = f"SELECT Name FROM MealsDatabase.MealsTable;"
    results = execute_mysql_query(query_string)
    meals = [result['Name'] for result in results]
    if request.method == "POST":
        details = request.form
        query_string = f"SELECT * FROM MealsDatabase.MealsTable WHERE Name='{details['Meal']}';"
        results = execute_mysql_query(query_string)
        return redirect(url_for('edit.edit_meal', meal = results[0]['Name']))
    return render_template('edit_list.html',
                            len_meals = len(meals), meals = meals)


@edit.route('/edit/<meal>', methods=['GET', 'POST'])
def edit_meal(meal):
    from .. import mysql
    from ..variables import staples_list, book_list, fresh_ingredients, tinned_ingredients, dry_ingredients, dairy_ingredients, tag_list
    if request.method == "GET":
        query_string = f"SELECT * FROM MealsDatabase.MealsTable WHERE Name = '{meal}';"
        results = execute_mysql_query(query_string)
        current_fresh_ingredients = json.loads(results[0]['Fresh_Ingredients'])
        current_fresh_ingredients_keys = list(current_fresh_ingredients.keys())
        current_tinned_ingredients = json.loads(results[0]['Tinned_Ingredients'])
        current_tinned_ingredients_keys = list(current_tinned_ingredients.keys())
        current_dry_ingredients = json.loads(results[0]['Dry_Ingredients'])
        current_dry_ingredients_keys = list(current_dry_ingredients.keys())
        current_dairy_ingredients = json.loads(results[0]['Dairy_Ingredients'])
        current_dairy_ingredients_keys = list(current_dairy_ingredients.keys())
        current_tags = [results[0]['Spring_Summer'], results[0]['Autumn_Winter'], results[0]['Quick_Easy'], results[0]['Special']]
        print(book_list)

        return render_template('edit_meal.html', meal_name = results[0]['Name'], staple = results[0]['Staple'], book = results[0]['Book'], page = results[0]['Page'], website = results[0]['Website'],
            current_fresh_ingredients = current_fresh_ingredients, current_fresh_ingredients_keys = current_fresh_ingredients_keys, 
            current_tinned_ingredients = current_tinned_ingredients, current_tinned_ingredients_keys = current_tinned_ingredients_keys, 
            current_dry_ingredients = current_dry_ingredients, current_dry_ingredients_keys = current_dry_ingredients_keys, 
            current_dairy_ingredients = current_dairy_ingredients, current_dairy_ingredients_keys = current_dairy_ingredients_keys, 
            len_staples = len(staples_list), staples = staples_list,
            len_books = len(book_list), books = book_list,
            len_fresh_ingredients = len(fresh_ingredients), fresh_ingredients = [ingredient[0] for ingredient in fresh_ingredients], fresh_ingredients_units = [ingredient[1] for ingredient in fresh_ingredients],
            len_tinned_ingredients = len(tinned_ingredients), tinned_ingredients = [ingredient[0] for ingredient in tinned_ingredients], tinned_ingredients_units = [ingredient[1] for ingredient in tinned_ingredients],
            len_dry_ingredients = len(dry_ingredients), dry_ingredients = [ingredient[0] for ingredient in dry_ingredients], dry_ingredients_units = [ingredient[1] for ingredient in dry_ingredients],
            len_dairy_ingredients = len(dairy_ingredients), dairy_ingredients = [ingredient[0] for ingredient in dairy_ingredients], dairy_ingredients_units = [ingredient[1] for ingredient in dairy_ingredients],
            len_tags = len(tag_list), tags = tag_list,
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
        cur = mysql.connection.cursor()
        cur.execute(
            f"UPDATE MealsDatabase.MealsTable SET Name = '{details['Name']}', Staple = '{details['Staple']}', Book = '{details['Book']}', Page = '{details['Page']}', Website = '{details['Website']}', Fresh_Ingredients = '{fresh_ing}', Tinned_Ingredients = '{tinned_ing}', Dry_Ingredients = '{dry_ing}', Dairy_Ingredients = '{dairy_ing}', Spring_Summer = {tags['Spring_Summer']}, Autumn_Winter = {tags['Autumn_Winter']}, Quick_Easy = {tags['Quick_Easy']}, Special = {tags['Special']} WHERE (Name = '{details['Name']}');")
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('edit.confirmation', meal = meal))


@edit.route('/edit_confirmation/<meal>', methods=['GET', 'POST'])
def confirmation(meal):
    if request.method == "GET":
        query_string = f"SELECT * FROM MealsDatabase.MealsTable WHERE Name='{meal}';"
        result = execute_mysql_query(query_string)
        location_details = {}
        if result[0]['Website'] == None or result[0]['Website'] == '':
            location_details['Book'] = result[0]['Book']
            location_details['Page'] = result[0]['Page']
        else:
            location_details['Website'] = result[0]['Website']
        fresh_ingredients = [list(json.loads(result[0]['Fresh_Ingredients']).keys()), list(json.loads(result[0]['Fresh_Ingredients']).values())]
        tinned_ingredients = [list(json.loads(result[0]['Tinned_Ingredients']).keys()), list(json.loads(result[0]['Tinned_Ingredients']).values())]
        dry_ingredients = [list(json.loads(result[0]['Dry_Ingredients']).keys()), list(json.loads(result[0]['Dry_Ingredients']).values())]
        dairy_ingredients = [list(json.loads(result[0]['Dairy_Ingredients']).keys()), list(json.loads(result[0]['Dairy_Ingredients']).values())]
        tags = [{"Spring/Summer": result[0]['Spring_Summer']}, {"Autumn/Winter": result[0]['Autumn_Winter']}, {"Quick/Easy": result[0]['Quick_Easy']}, {"Special": result[0]['Special']}]
        tags = get_tag_keys(tags)
        return render_template('edit_confirmation.html', meal_name=meal,
                                location_details = location_details, location_keys = location_details.keys(),
                                staple = result[0]['Staple'],
                                len_fresh_ingredients = len(fresh_ingredients[0]), fresh_ingredients_keys=fresh_ingredients[0], fresh_ingredients_values=fresh_ingredients[1],
                                len_tinned_ingredients = len(tinned_ingredients[0]), tinned_ingredients_keys=tinned_ingredients[0], tinned_ingredients_values=tinned_ingredients[1],
                                len_dry_ingredients = len(dry_ingredients[0]), dry_ingredients_keys=dry_ingredients[0], dry_ingredients_values=dry_ingredients[1],
                                len_dairy_ingredients = len(dairy_ingredients[0]), dairy_ingredients_keys=dairy_ingredients[0], dairy_ingredients_values=dairy_ingredients[1],
                                len_tags = len(tags), tags = tags)
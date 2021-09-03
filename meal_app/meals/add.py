from flask import Blueprint, render_template, request, redirect, url_for
import json
from ..utilities import execute_mysql_query

add = Blueprint('add', __name__, template_folder='templates', static_folder='../static')

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
            new_key = key.replace(filter_word, '')
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


@add.route('/add', methods=['GET', 'POST'])
def index():
    from .. import mysql
    from ..variables import staples_list, book_list, fresh_ingredients, tinned_ingredients, dry_ingredients, dairy_ingredients, tag_list
    if request.method == "POST":
        details = request.form
        details_dict = details.to_dict()
        tag_list = []
        for key in list(details_dict.keys()):
            if 'Tag' in key:
                tag_list.append(details_dict[key])
        print(details['Name'].replace("'", "\'"))
        tags = get_tags(tag_list)
        cur = mysql.connection.cursor()
        # query = "INSERT INTO MealsTable(Name, Staple, Book, Page, Website, Fresh_Ingredients, Tinned_Ingredients, Dry_Ingredients, Dairy_Ingredients, Last_Made, Spring_Summer, Autumn_Winter, Quick_Easy, Special) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        query = f"""INSERT INTO MealsTable (Name, Staple, Book, Page, Website, Fresh_Ingredients, Tinned_Ingredients, Dry_Ingredients, Dairy_Ingredients, Last_Made, Spring_Summer, Autumn_Winter, Quick_Easy, Special) VALUES ('{details["Name"]}', '{details["Staple"]}', '{details["Book"]}', '{details["Page"]}', '{details["Website"]}', '{parse_ingredients(details_dict, "Fresh ")}', '{parse_ingredients(details_dict, "Tinned ")}', '{parse_ingredients(details_dict, "Dry ")}', '{parse_ingredients(details_dict, "Dairy ")}', '{"2021-01-01"}', '{tags["Spring_Summer"]}', '{tags["Autumn_Winter"]}', '{tags["Quick_Easy"]}', '{tags["Special"]}');"""
        print(query)
        # cur.execute(query,
        #     (details['Name'], details['Staple'], details['Book'], details['Page'], details['Website'], parse_ingredients(details_dict, "Fresh "), parse_ingredients(details_dict, "Tinned "), parse_ingredients(details_dict, "Dry "), parse_ingredients(details_dict, "Dairy "), "2021-01-01", tags['Spring_Summer'], tags['Autumn_Winter'], tags['Quick_Easy'], tags['Special'])
        #     )
        cur.execute(query)
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('add.confirmation', meal = details['Name']))
    return render_template('add.html', 
        len_staples = len(staples_list), staples = staples_list,
        len_books = len(book_list), books = book_list,
        len_fresh_ingredients = len(fresh_ingredients), fresh_ingredients = [ingredient[0] for ingredient in fresh_ingredients], fresh_ingredients_units = [ingredient[1] for ingredient in fresh_ingredients],
        len_tinned_ingredients = len(tinned_ingredients), tinned_ingredients = [ingredient[0] for ingredient in tinned_ingredients], tinned_ingredients_units = [ingredient[1] for ingredient in tinned_ingredients],
        len_dry_ingredients = len(dry_ingredients), dry_ingredients = [ingredient[0] for ingredient in dry_ingredients], dry_ingredients_units = [ingredient[1] for ingredient in dry_ingredients],
        len_dairy_ingredients = len(dairy_ingredients), dairy_ingredients = [ingredient[0] for ingredient in dairy_ingredients], dairy_ingredients_units = [ingredient[1] for ingredient in dairy_ingredients],
        len_tags = len(tag_list), tags = tag_list)


@add.route('/add_confirmation/<meal>', methods=['GET', 'POST'])
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
        return render_template('add_confirmation.html', meal_name=meal,
                                location_details = location_details, location_keys = location_details.keys(),
                                staple = result[0]['Staple'],
                                len_fresh_ingredients = len(fresh_ingredients[0]), fresh_ingredients_keys=fresh_ingredients[0], fresh_ingredients_values=fresh_ingredients[1],
                                len_tinned_ingredients = len(tinned_ingredients[0]), tinned_ingredients_keys=tinned_ingredients[0], tinned_ingredients_values=tinned_ingredients[1],
                                len_dry_ingredients = len(dry_ingredients[0]), dry_ingredients_keys=dry_ingredients[0], dry_ingredients_values=dry_ingredients[1],
                                len_dairy_ingredients = len(dairy_ingredients[0]), dairy_ingredients_keys=dairy_ingredients[0], dairy_ingredients_values=dairy_ingredients[1],
                                len_tags = len(tags), tags = tags)
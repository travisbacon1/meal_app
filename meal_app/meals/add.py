from flask import Blueprint, render_template, request, redirect, url_for
import json

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
            new_key = key.removeprefix(filter_word)
            parsed_ingredient_dict[new_key] = ingredients_dict[key]
    return json.dumps(parsed_ingredient_dict)

@add.route('/add', methods=['GET', 'POST'])
def index():
    from .. import mysql
    from ..variables import staples_list, book_list, fresh_ingredients, tinned_ingredients, dry_ingredients, dairy_ingredients
    if request.method == "POST":
        details = request.form
        details_dict = details.to_dict()
        cur = mysql.connection.cursor()
        cur.execute(
            "INSERT INTO MealsTable(Name, Staple, Book, Page, Website, Fresh_Ingredients, Tinned_Ingredients, Dry_Ingredients, Dairy_Ingredients) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
            (details['Name'], details['Staple'], details['Book'], details['Page'], details['Website'], parse_ingredients(details_dict, "Fresh "), parse_ingredients(details_dict, "Tinned "), parse_ingredients(details_dict, "Dry "), parse_ingredients(details_dict, "Dairy "))
            )
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('add.index'))
    return render_template('add.html', 
        len_staples = len(staples_list), staples = staples_list,
        len_books = len(book_list), books = book_list,
        len_fresh_ingredients = len(fresh_ingredients), fresh_ingredients = fresh_ingredients,
        len_tinned_ingredients = len(tinned_ingredients), tinned_ingredients = tinned_ingredients,
        len_dry_ingredients = len(dry_ingredients), dry_ingredients = dry_ingredients,
        len_dairy_ingredients = len(dairy_ingredients), dairy_ingredients = dairy_ingredients)
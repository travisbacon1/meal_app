from flask import Blueprint, render_template, request, redirect, url_for, session
from .. import mysql
import json

search = Blueprint('search', __name__, template_folder='templates', static_folder='static')

@search.route('/search', methods=['GET', 'POST'])
def index():
    db_cursor = mysql.connection.cursor()
    query = f"SELECT Fresh_Ingredients, Tinned_Ingredients, Dry_Ingredients, Dairy_Ingredients FROM MealsDatabase.MealsTable WHERE json_length(Fresh_Ingredients) > 0;;"
    db_cursor.execute(query)
    results = db_cursor.fetchall()
    json_results = [json.loads(result['Fresh_Ingredients']) for result in results]
    fresh_ingredients = sorted(list(set(key for i in json_results for key in i.keys())))
    json_results = [json.loads(result['Tinned_Ingredients']) for result in results]
    tinned_ingredients = sorted(list(set(key for i in json_results for key in i.keys())))
    json_results = [json.loads(result['Dry_Ingredients']) for result in results]
    dry_ingredients = sorted(list(set(key for i in json_results for key in i.keys())))
    json_results = [json.loads(result['Dairy_Ingredients']) for result in results]
    dairy_ingredients = sorted(list(set(key for i in json_results for key in i.keys())))

    if request.method == "POST":
        details = request.form
        details_dict = details.to_dict()
        if "null" not in request.form["Fresh_Ingredients"]:
            json_key = "Fresh_Ingredients"
            ingredient = details_dict[json_key]
        elif "null" not in request.form["Tinned_Ingredients"]:
            json_key = "Tinned_Ingredients"
            ingredient = details_dict[json_key]
        elif "null" not in request.form["Dry_Ingredients"]:
            json_key = "Dry_Ingredients"
            ingredient = details_dict[json_key]
        elif "null" not in request.form["Dairy_Ingredients"]:
            json_key = "Dairy_Ingredients"
            ingredient = details_dict[json_key]
        db_cursor = mysql.connection.cursor()
        query = f"""SELECT * FROM MealsDatabase.MealsTable
                WHERE JSON_EXTRACT({json_key}, '$."{ingredient}"');"""
        db_cursor.execute(query)
        results = db_cursor.fetchall()
        session['meal_list'] = [result['Name'] for result in results]
        return redirect(url_for('search.search_results', ingredient = ingredient))
    return render_template('search.html', 
                            len_fresh_ingredients = len(fresh_ingredients), fresh_ingredients = fresh_ingredients,
                            len_tinned_ingredients = len(tinned_ingredients), tinned_ingredients = tinned_ingredients,
                            len_dry_ingredients = len(dry_ingredients), dry_ingredients = dry_ingredients,
                            len_dairy_ingredients = len(dairy_ingredients), dairy_ingredients = dairy_ingredients)


@search.route('/search/<ingredient>', methods=['GET', 'POST'])
def search_results(ingredient):
    if request.method == "GET":
        meals = session.pop('meal_list', [])
        return render_template('search_results.html', ingredient = ingredient, len_meals = len(meals), meals = meals)
    else:
        return redirect(url_for('search'))
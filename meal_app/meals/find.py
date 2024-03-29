from flask import Blueprint, render_template, request, redirect, url_for
import json
from .. import mysql
from ..utilities import execute_mysql_query

find = Blueprint('find', __name__, template_folder='templates', static_folder='../static')

@find.route('/find', methods=['GET', 'POST'])
def index():
    query_string = f"SELECT Name FROM MealsDatabase.MealsTable;"
    results = execute_mysql_query(query_string)
    meals = [result['Name'] for result in results]
    if request.method == "POST":
        details = request.form
        query_string = f"SELECT * FROM MealsDatabase.MealsTable WHERE Name='{details['Meal']}';"
        results = execute_mysql_query(query_string)
        return redirect(url_for('find.some_meal_page', meal = results[0]['Name']))
    return render_template('find.html',
                            len_meals = len(meals), meals = meals)


@find.route('/find/<meal>', methods=['GET', 'POST'])
def some_meal_page(meal):
    if request.method == "GET":
        db_cursor = mysql.connection.cursor()
        query = f"SELECT * FROM MealsDatabase.MealsTable WHERE Name='{meal}';"
        db_cursor.execute(query)
        result = db_cursor.fetchall()
        location_details = {}
        if result[0].get('Website') == None or result[0].get('Website') == '':
            location_details['Book'] = result[0].get('Book')
            location_details['Page'] = result[0].get('Page')
        else:
            location_details['Website'] = result[0].get('Website')
        fresh_ingredients = [list(json.loads(result[0]['Fresh_Ingredients']).keys()), list(json.loads(result[0]['Fresh_Ingredients']).values())]
        tinned_ingredients = [list(json.loads(result[0]['Tinned_Ingredients']).keys()), list(json.loads(result[0]['Tinned_Ingredients']).values())]
        dry_ingredients = [list(json.loads(result[0]['Dry_Ingredients']).keys()), list(json.loads(result[0]['Dry_Ingredients']).values())]
        dairy_ingredients = [list(json.loads(result[0]['Dairy_Ingredients']).keys()), list(json.loads(result[0]['Dairy_Ingredients']).values())]
        return render_template('find_results.html', meal_name=meal,
                                location_details = location_details, location_keys = location_details.keys(),
                                staple = result[0].get('Staple'),
                                len_fresh_ingredients = len(fresh_ingredients[0]), fresh_ingredients_keys=fresh_ingredients[0], fresh_ingredients_values=fresh_ingredients[1],
                                len_tinned_ingredients = len(tinned_ingredients[0]), tinned_ingredients_keys=tinned_ingredients[0], tinned_ingredients_values=tinned_ingredients[1],
                                len_dry_ingredients = len(dry_ingredients[0]), dry_ingredients_keys=dry_ingredients[0], dry_ingredients_values=dry_ingredients[1],
                                len_dairy_ingredients = len(dairy_ingredients[0]), dairy_ingredients_keys=dairy_ingredients[0], dairy_ingredients_values=dairy_ingredients[1])
    else:
        return redirect(url_for('find'))
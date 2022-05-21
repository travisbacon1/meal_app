from flask import Blueprint, render_template, request, redirect, url_for
import json
from ..utilities import execute_mysql_query
import os

find = Blueprint('find', __name__, template_folder='templates', static_folder='../static')

@find.route('/find', methods=['GET', 'POST'])
def index():
    query_string = f"SELECT Name FROM {os.environ['MYSQL_DATABASE']}.{os.environ['MYSQL_TABLE']};"
    results = execute_mysql_query(query_string)
    meals = [result['Name'] for result in results]
    if request.method == "POST":
        details = request.form
        query_string = f"SELECT * FROM {os.environ['MYSQL_DATABASE']}.{os.environ['MYSQL_TABLE']} WHERE Name='{details['Meal']}';"
        results = execute_mysql_query(query_string)
        return redirect(url_for('find.some_meal_page', meal=results[0]['Name']))
    return render_template('find.html', meals=meals)


@find.route('/find/<meal>', methods=['GET', 'POST'])
def some_meal_page(meal):
    if request.method == "GET":
        query_string = f"SELECT * FROM {os.environ['MYSQL_DATABASE']}.{os.environ['MYSQL_TABLE']} WHERE Name='{meal}';"
        result = execute_mysql_query(query_string)
        location_details = f"{result[0].get('Book')}, page {result[0].get('Page')}" if result[0].get('Website') == None or result[0].get('Website') == "" else result[0].get('Website')
        fresh_ingredients = [list(json.loads(result[0]['Fresh_Ingredients']).keys()), list(json.loads(result[0]['Fresh_Ingredients']).values())]
        tinned_ingredients = [list(json.loads(result[0]['Tinned_Ingredients']).keys()), list(json.loads(result[0]['Tinned_Ingredients']).values())]
        dry_ingredients = [list(json.loads(result[0]['Dry_Ingredients']).keys()), list(json.loads(result[0]['Dry_Ingredients']).values())]
        dairy_ingredients = [list(json.loads(result[0]['Dairy_Ingredients']).keys()), list(json.loads(result[0]['Dairy_Ingredients']).values())]
        return render_template('find_results.html', meal_name=meal,
                                location_details = location_details,
                                staple = result[0].get('Staple'),
                                len_fresh_ingredients = len(fresh_ingredients[0]), fresh_ingredients_keys=fresh_ingredients[0], fresh_ingredients_values=fresh_ingredients[1],
                                len_tinned_ingredients = len(tinned_ingredients[0]), tinned_ingredients_keys=tinned_ingredients[0], tinned_ingredients_values=tinned_ingredients[1],
                                len_dry_ingredients = len(dry_ingredients[0]), dry_ingredients_keys=dry_ingredients[0], dry_ingredients_values=dry_ingredients[1],
                                len_dairy_ingredients = len(dairy_ingredients[0]), dairy_ingredients_keys=dairy_ingredients[0], dairy_ingredients_values=dairy_ingredients[1])
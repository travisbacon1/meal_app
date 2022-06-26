from flask import Blueprint, render_template, request, redirect, url_for
from ..utilities import execute_mysql_query, meal_information
import os

find_meal = Blueprint('find_meal', __name__, template_folder='templates', static_folder='../static')

@find_meal.route('/find_meal', methods=['GET', 'POST'])
def main():
    query_string = f"SELECT Name FROM {os.environ['MYSQL_DATABASE']}.{os.environ['MYSQL_TABLE']};"
    results = execute_mysql_query(query_string)
    meals = [result['Name'] for result in results]
    if request.method == "POST":
        details = request.form
        query_string = f"SELECT * FROM {os.environ['MYSQL_DATABASE']}.{os.environ['MYSQL_TABLE']} WHERE Name='{details['Meal']}';"
        results = execute_mysql_query(query_string)
        return redirect(url_for('find.meal_info', meal=results[0]['Name']))
    return render_template('find_meal.html', meals=meals)


@find_meal.route('/find_meal/<meal>', methods=['GET'])
def meal_info(meal):
    template = meal_information(meal)
    return template
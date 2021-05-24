from flask import Blueprint, render_template, request, redirect, url_for
from .. import mysql
import json
from ..utilities import execute_mysql_query

list_meals = Blueprint('list_meals', __name__, template_folder='templates', static_folder='../static')

@list_meals.route('/list_meals', methods=['GET', 'POST'])
def index():
    if request.method == "GET":
        from datetime import datetime
        query_string = "SELECT *, CAST(Page AS SIGNED) AS Page FROM MealsDatabase.MealsTable ORDER BY Book, Page;"
        results = execute_mysql_query(query_string)
        results = [result for result in results]
        meal_names = [meal['Name'] for meal in results]
        staples = [meal['Staple'] for meal in results]
        books = [meal['Book'] for meal in results]
        page = [meal['Page'] for meal in results]
        website = [meal['Website'] for meal in results]
        last_date = [datetime.strftime(meal['Last_Made'], "%d-%m-%Y") for meal in results]
        return render_template('list_meals.html', len_meals = len(meal_names),
                                meal_names = meal_names, staples=staples,
                                books=books, page=page, website=website,
                                last_date=last_date)
    elif request.method == "POST" and (request.form['submit']):
        details_dict = request.form.to_dict()
        meal = json.dumps(details_dict['submit']).replace('"', '')
        return redirect(url_for('find.some_meal_page', meal = meal))
from flask import Blueprint, render_template, request, redirect, url_for
from .. import mysql
import json
from ..utilities import execute_mysql_query
import os

inspire = Blueprint('inspire', __name__, template_folder='templates', static_folder='../static')

@inspire.route('/inspire', methods=['GET', 'POST'])
def index():
    from ..variables import tag_list
    from datetime import datetime
    if request.method == "POST":
        details = request.form
        tag = details['Tag'].replace('/', '_')
        query_string = f"SELECT Name, Staple, Last_Made FROM {os.environ['MYSQL_DATABASE']}.{os.environ['MYSQL_TABLE']} WHERE {tag}=1 ORDER BY Name;"
        results = execute_mysql_query(query_string)
        meal_names = [meal['Name'] for meal in results]
        staples = [meal['Staple'] for meal in results]
        last_date = [datetime.strftime(meal['Last_Made'], "%d-%m-%Y") for meal in results]
        return render_template('inspire_results.html',
                            tag = details['Tag'],
                            len_meals = len(meal_names),
                            meal_names = meal_names,
                            staples=staples,
                            last_date=last_date)
    return render_template('inspire.html',
                                len_tags = len(tag_list), tags = tag_list)
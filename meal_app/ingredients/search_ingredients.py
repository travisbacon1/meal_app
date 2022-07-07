from flask import Blueprint, render_template, request, redirect, url_for, session
from ..utilities import execute_mysql_query
import os
from models import IngredientsTable
from app import engine
from sqlmodel import Session, select, func

search_ingredients = Blueprint('search_ingredients', __name__, template_folder='templates', static_folder='../static')

@search_ingredients.route('/search_ingredients', methods=['GET', 'POST'])
def main():
    with Session(engine) as sql_session:
        statement = select(IngredientsTable.Type, func.group_concat((IngredientsTable.Name).distinct())).group_by(IngredientsTable.Type)
        sql_results = dict(sql_session.exec(statement).fetchall())
        unpacked_results = {key: value.split(',') for key, value in sql_results.items()}

    if request.method == "POST":
        details = request.form
        details_dict = details.to_dict()
        for key, value in details_dict.items():
            if value != "null":
                json_key, ingredient = key, value
        query_string = f"""SELECT * FROM {os.environ['MYSQL_DATABASE']}.{os.environ['MYSQL_TABLE']}
                WHERE JSON_EXTRACT({json_key}, '$."{ingredient}"');"""
        results = execute_mysql_query(query_string)
        session['meal_list'] = [result['Name'] for result in results]
        return redirect(url_for('search_ingredients.search_results', ingredient = ingredient))
    return render_template('search_ingredients.html', 
                            ingredient_types = ["Fresh", "Dairy", "Dry", "Tinned"], ingredients=unpacked_results)


@search_ingredients.route('/search_ingredients/<ingredient>', methods=['GET', 'POST'])
def search_results(ingredient):
    if request.method == "GET":
        meals = session.pop('meal_list', [])
        return render_template('search_results.html', ingredient = ingredient, len_meals = len(meals), meals = meals)
    else:
        return redirect(url_for('search.index'))
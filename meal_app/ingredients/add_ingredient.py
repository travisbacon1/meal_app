from flask import Blueprint, render_template, request, redirect, url_for
from ..utilities import execute_mysql_query
import os

add_ingredient = Blueprint('add_ingredient', __name__, template_folder='templates', static_folder='../static')

@add_ingredient.route('/add_ingredient', methods=['GET', 'POST'])
def index():
    ingredient_types = [
        "",
        "Fresh",
        "Dairy",
        "Dry",
        "Tinned"
    ]
    if request.method == "POST":
        details = request.form
        details_dict = details.to_dict()
        query_string = f"""INSERT INTO {os.environ['MYSQL_INGREDIENTS_TABLE']} (Name, Unit, Type) VALUES ('{details_dict["Name"]}', '{details_dict["Unit"]}', '{details_dict["Type"]}');"""
        execute_mysql_query(query_string, fetch_results=False, commit=True)
        return redirect(url_for('add_ingredient.confirmation', ingredient=details_dict["Name"]))
    return render_template('add_ingredient.html', ingredient_types=ingredient_types)


@add_ingredient.route('/add_ingredient_confirmation/<ingredient>', methods=['GET', 'POST'])
def confirmation(ingredient):
    if request.method == "GET":
        query_string = f"SELECT * FROM {os.environ['MYSQL_INGREDIENTS_TABLE']} WHERE Name='{ingredient}';"
        result = execute_mysql_query(query_string)[0]
        return render_template('add_ingredient_confirmation.html', ingredient_name=result['Name'],
                                ingredient_unit=result['Unit'], ingredient_type=result['Type'])
from flask import Blueprint, render_template, request, redirect, url_for
from ..utilities import execute_mysql_query, parse_ingredients, get_tags, meal_information
import os
from app import engine
from sqlmodel import Session, select, func
from models import MealsTable, IngredientsTable
import json

add_meal = Blueprint('add_meal', __name__, template_folder='templates', static_folder='../static')

@add_meal.route('/add_meal', methods=['GET', 'POST'])
def main():
    from ..variables import tag_list
    with Session(engine) as sql_session:
        statement = select(MealsTable.Staple).distinct()
        staples_list = sorted(sql_session.exec(statement).fetchall())
        staples_list.insert(0,"")
        statement = select(MealsTable.Book).distinct()
        book_list = sorted(sql_session.exec(statement).fetchall())
        statement = select(
            IngredientsTable.Type,
            func.json_arrayagg(
                func.json_object(
                    "Ingredient", IngredientsTable.Name,
                    "Unit", IngredientsTable.Unit))).group_by(IngredientsTable.Type)
        sql_results = dict(sql_session.exec(statement).fetchall())
    ingredient_dict = {}
    for ingredient_type in ['Fresh', 'Dairy', 'Dry', 'Tinned']:
        ingredient_dict[ingredient_type] = sorted(json.loads(sql_results[ingredient_type]), key=lambda d: d['Ingredient'])

    if request.method == "POST":
        details = request.form
        details_dict = details.to_dict()
        tag_list = []
        for key in list(details_dict.keys()):
            if 'Tag' in key:
                tag_list.append(details_dict[key])
        tags = get_tags(tag_list)
        query_string = f"""INSERT INTO {os.environ['MYSQL_TABLE']} (Name, Staple, Book, Page, Website, Fresh_Ingredients, Tinned_Ingredients, Dry_Ingredients, Dairy_Ingredients, Last_Made, Spring_Summer, Autumn_Winter, Quick_Easy, Special) VALUES ('{details["Name"]}', '{details["Staple"]}', '{details["Book"]}', '{details["Page"]}', '{details["Website"]}', '{parse_ingredients(details_dict, "Fresh ")}', '{parse_ingredients(details_dict, "Tinned ")}', '{parse_ingredients(details_dict, "Dry ")}', '{parse_ingredients(details_dict, "Dairy ")}', '{"2021-01-01"}', '{tags["Spring_Summer"]}', '{tags["Autumn_Winter"]}', '{tags["Quick_Easy"]}', '{tags["Special"]}');"""
        execute_mysql_query(query_string, fetch_results=False, commit=True)
        print(query_string)
        return redirect(url_for('add.confirmation', meal=details['Name']))
    return render_template('add_meal.html', 
        staples=staples_list, books=book_list,
        ingredients=ingredient_dict, tags=tag_list)


@add_meal.route('/confirmation/<meal>', methods=['GET'])
def confirmation(meal):
    template = meal_information(meal)
    return template
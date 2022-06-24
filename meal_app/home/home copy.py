from flask import Blueprint, render_template, request, redirect, url_for
from app import TestTable2, engine
from sqlmodel import SQLModel, Session, create_engine, select
# from sqlalchemy import create_engine, select
# from sqlalchemy.orm import Session
# import sqlalchemy
import os
import json

home = Blueprint('home', __name__, template_folder="templates", static_folder='../static')

@home.route("/", methods=['GET', 'POST'])
def index():
    # bla = TestTable2(Name = "bla")
    # bla2 = MealNew2(
    #     Name = "bla",
    #     Staple = "Bla",
    #     Tinned_Ingredients = {"Apple": 1}
    #     )
    # engine = create_engine(f'mysql+mysqldb://{os.environ["MYSQL_USER"]}:{os.environ["MYSQL_PASSWORD"]}@{os.environ["MYSQL_HOSTNAME"]}/{os.environ["MYSQL_DATABASE"]}', echo=True)
    # print(sqlalchemy.inspect(engine).has_table("TestTable2"))
    # with Session(engine) as session:
    #     statement = select(TestTable2.Name)
    #     results = [dict(row) for row in session.execute(statement).fetchall()]
    #     print(results)

    with Session(engine) as session:
        statement = select(TestTable2)
        results = [row for row in session.exec(statement).fetchall()]
        print(results[0].Name)
        # session.query(MealNew2.Name)
        # statement = select(MealNew2)
        # orgs = session.exec(statement)
        # print(f"orgs::{orgs}")
        # org_list = orgs.fetchall()
    # bla2.Book = "bla"

    # print(bla2)
    # print(dir(MealNew2))
    # db.session.query(MealNew2.Name)
    # db.session.add(bla2)

    buttons = [
        "Add Ingredient",
        "Add Meal",
        "Edit Meal",
        "Get Meal Info",
        "Search Ingredients",
        "List Meals",
        "Create Meal Plan",
        "Load Meal Plan",
        "Delete Meal Plan"
    ]
    if request.method == "POST":
        if request.form['submit'] == 'Add Ingredient':
            return redirect(url_for('add_ingredient.index'))
        elif request.form['submit'] == 'Add Meal':
            return redirect(url_for('add.index'))
        elif request.form['submit'] == 'Edit Meal':
            return redirect(url_for('edit.index'))
        elif request.form['submit'] == 'Get Meal Info':
            return redirect(url_for('find.index'))
        elif request.form['submit'] == 'Search Ingredients':
            return redirect(url_for('search.index'))
        elif request.form['submit'] == 'List Meals':
            return redirect(url_for('list_meals.index'))
        elif request.form['submit'] == 'Create Meal Plan':
            return redirect(url_for('create.create_meal_plan'))
        elif request.form['submit'] == 'Load Meal Plan':
            return redirect(url_for('load.choose_meal_plan'))
        elif request.form['submit'] == 'Delete Meal Plan':
            return redirect(url_for('delete.delete_meal_plan'))
    return render_template('index.html', buttons=buttons)
from flask import Blueprint, render_template, request, redirect, url_for
from ..utilities import meal_information
import os
from models import MealsTable
from sqlmodel import Session, select
from app import engine

find_meal = Blueprint('find_meal', __name__, template_folder='templates', static_folder='../static')

@find_meal.route('/find_meal', methods=['GET', 'POST'])
def main():
    with Session(engine) as session:
        statement = select(MealsTable)
        results = session.exec(statement).fetchall()
        meals = [result.Name for result in results]
    if request.method == "POST":
        details = request.form
        with Session(engine) as session:
            statement = select(MealsTable).where(MealsTable.Name == details['Meal'])
            result = session.exec(statement).first()
        return redirect(url_for('find_meal.meal_info', meal=result.Name))
    return render_template('find_meal.html', meals=meals)


@find_meal.route('/find_meal/<meal>', methods=['GET'])
def meal_info(meal):
    template = meal_information(meal)
    return template
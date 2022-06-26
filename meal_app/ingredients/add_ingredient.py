from flask import Blueprint, render_template, request, redirect, url_for
from models import IngredientsTestTable
from app import engine
from sqlmodel import Session, select

add_ingredient = Blueprint('add_ingredient', __name__, template_folder='templates', static_folder='../static')

@add_ingredient.route('/add_ingredient', methods=['GET', 'POST'])
def main():
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
        ingredient = IngredientsTestTable(
            Name = details_dict["Name"],
            Unit = details_dict["Unit"],
            Type = details_dict["Type"]
            )

        with Session(engine) as session:
            session.add(ingredient)
            session.commit()
        return redirect(url_for('add_ingredient.confirmation', ingredient=details_dict["Name"]))
    return render_template('add_ingredient.html', ingredient_types=ingredient_types)


@add_ingredient.route('/add_ingredient_confirmation/<ingredient>', methods=['GET', 'POST'])
def confirmation(ingredient):
    if request.method == "GET":
        with Session(engine) as session:
            statement = select(IngredientsTestTable).where(IngredientsTestTable.Name == ingredient)
            result = session.exec(statement).first()
        return render_template('add_ingredient_confirmation.html', ingredient_name=result.Name,
                                ingredient_unit=result.Unit, ingredient_type=result.Type)
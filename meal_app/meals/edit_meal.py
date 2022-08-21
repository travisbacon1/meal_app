from flask import Blueprint, render_template, request, redirect, url_for
import json
from ..utilities import execute_mysql_query, parse_ingredients, append_current_ingredients, meal_information
import os
from app import engine
from sqlmodel import Session, select, func
from models import MealsTable, IngredientsTable

edit_meal = Blueprint('edit_meal', __name__, template_folder='templates', static_folder='../static')

def update_tags(results):
    tag_list = ['Spring_Summer', 'Autumn_Winter', 'Quick_Easy', 'Special']
    for tag in tag_list:
        if tag in results:
            results[tag] = 1
        else:
            results[tag] = 0
    return results


@edit_meal.route('/edit_meal', methods=['GET', 'POST'])
def main():
    with Session(engine) as sql_session:
        statement = select(MealsTable.Name)
        meals = sql_session.exec(statement).fetchall()
    if request.method == "POST":
        with Session(engine) as sql_session:
            statement = select(MealsTable.Name).where(MealsTable.Name==request.form['Meal'])
            meal = sql_session.exec(statement).first()
        return redirect(url_for('edit_meal.edit', meal=meal))
    else:
        return render_template('edit_list.html', meals=meals)

# TODO: BUG: Need to capture current name as updating name doesn't work
@edit_meal.route('/edit/<meal>', methods=['GET', 'POST'])
def edit(meal):
    from ..variables import book_list
    if request.method == "GET":
        with Session(engine) as sql_session:
            statement = select(
                MealsTable.Name,
                MealsTable.Staple,
                MealsTable.Book,
                MealsTable.Page,
                MealsTable.Website,
                MealsTable.Fresh_Ingredients,
                MealsTable.Tinned_Ingredients,
                MealsTable.Dry_Ingredients,
                MealsTable.Dairy_Ingredients,
                func.json_arrayagg(
                    func.json_object(
                        "Spring_Summer", MealsTable.Spring_Summer,
                        "Autumn_Winter", MealsTable.Autumn_Winter,
                        "Quick_Easy", MealsTable.Quick_Easy,
                        "Special", MealsTable.Special
                        )
                    ).label("Tags")
                ).where(MealsTable.Name==meal)
            results = dict(sql_session.exec(statement).first())

            statement = select(
                IngredientsTable.Type,
                func.json_arrayagg(
                    func.json_object(
                        "Ingredient", IngredientsTable.Name,
                        "Unit", IngredientsTable.Unit,
                        "Quantity", ""
                        )
                    ).label("Ingredient_data")
                ).group_by(IngredientsTable.Type)
            all_ingredient_data = dict(sql_session.exec(statement).fetchall())

        current_ingredients = {}
        for ingredient_type in list(all_ingredient_data.keys()):
            current_ingredients[ingredient_type] = append_current_ingredients(json.loads(all_ingredient_data[f'{ingredient_type}']), results[f'{ingredient_type}_Ingredients'])

        query_string = f"""SELECT DISTINCT(Staple) FROM {os.environ['MYSQL_DATABASE']}.{os.environ['MYSQL_TABLE']} ORDER BY Staple ASC;"""
        staples = execute_mysql_query(query_string)
        return render_template('edit_meal.html', meal_name=results['Name'], current_staple=results['Staple'],
                                book=results['Book'], page=results['Page'], website=results['Website'],
                                current_ingredients=current_ingredients, staples=staples,
                                books=book_list, current_tags=json.loads(results['Tags'])[0])

    if request.method == "POST":
        details_dict = request.form.to_dict()
        fresh_ing = parse_ingredients(details_dict, "Fresh ")
        tinned_ing = parse_ingredients(details_dict, "Tinned ")
        dry_ing = parse_ingredients(details_dict, "Dry ")
        dairy_ing = parse_ingredients(details_dict, "Dairy ")
        details_dict = update_tags(details_dict)
        query_string = f"""UPDATE {os.environ['MYSQL_DATABASE']}.{os.environ['MYSQL_TABLE']}
                            SET 
                                Name = '{details_dict['Name']}',
                                Staple = '{details_dict['Staple']}',
                                Book = '{details_dict['Book']}',
                                Page = '{details_dict['Page']}',
                                Website = '{details_dict['Website']}',
                                Fresh_Ingredients = '{fresh_ing}',
                                Tinned_Ingredients = '{tinned_ing}',
                                Dry_Ingredients = '{dry_ing}',
                                Dairy_Ingredients = '{dairy_ing}',
                                Spring_Summer = {details_dict['Spring_Summer']},
                                Autumn_Winter = {details_dict['Autumn_Winter']},
                                Quick_Easy = {details_dict['Quick_Easy']},
                                Special = {details_dict['Special']}
                            WHERE (Name = '{details_dict['Name']}');"""
        print(query_string)
        with Session(engine) as session:
            statement = select(MealsTable).where(MealsTable.Name == details_dict['Name'])
            meal = session.exec(statement).one()
            meal.Name = details_dict['Name']
            meal.Staple = details_dict['Staple']
            meal.Book = details_dict['Book']
            meal.Page = details_dict['Page']
            meal.Website = details_dict['Website']
            meal.Fresh_Ingredients = json.dumps(fresh_ing)
            meal.Tinned_Ingredients = json.dumps(tinned_ing)
            meal.Dry_Ingredients = json.dumps(dry_ing)
            meal.Dairy_Ingredients = json.dumps(dairy_ing)
            meal.Spring_Summer = details_dict['Spring_Summer']
            meal.Autumn_Winter = details_dict['Autumn_Winter']
            meal.Quick_Easy = details_dict['Quick_Easy']
            meal.Special = details_dict['Special']
            session.add(meal)
            session.commit()
            session.refresh(meal)
        # execute_mysql_query(query_string, fetch_results=False, commit=True)
        return redirect(url_for('edit_meal.confirmation', meal=details_dict['Name']))


@edit_meal.route('/edit_confirmation/<meal>', methods=['GET'])
def confirmation(meal):
    print(f"{meal=}")
    print(f"{type(meal)=}")
    template = meal_information(meal)
    return template
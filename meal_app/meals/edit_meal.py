from flask import Blueprint, render_template, request, redirect, url_for
import json
from ..utilities import execute_mysql_query, parse_ingredients, append_current_ingredients, meal_information
import os

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
    query_string = f"SELECT Name FROM {os.environ['MYSQL_DATABASE']}.{os.environ['MYSQL_TABLE']};"
    results = execute_mysql_query(query_string)
    meals = [result['Name'] for result in results]
    if request.method == "POST":
        details = request.form
        query_string = f"SELECT * FROM {os.environ['MYSQL_DATABASE']}.{os.environ['MYSQL_TABLE']} WHERE Name='{details['Meal']}';"
        results = execute_mysql_query(query_string)
        return redirect(url_for('edit_meal.edit', meal=results[0]['Name']))
    else:
        return render_template('edit_list.html', meals=meals)

# TODO: BUG: Need to capture current name as updating name doesn't work
@edit_meal.route('/edit/<meal>', methods=['GET', 'POST'])
def edit(meal):
    from ..variables import book_list
    if request.method == "GET":
        query_string = f"""
                        SELECT
                            Name,
                            Staple,
                            Book,
                            Page,
                            Website,
                            Fresh_Ingredients,
                            Tinned_Ingredients,
                            Dry_Ingredients,
                            Dairy_Ingredients,
                            JSON_OBJECT(
                                'Spring_Summer', Spring_Summer,
                                'Autumn_Winter', Autumn_Winter,
                                'Quick_Easy', Quick_Easy,
                                'Special', Special)
                            AS Tags
                        FROM {os.environ['MYSQL_DATABASE']}.{os.environ['MYSQL_TABLE']} WHERE Name = '{meal}';"""
        results = execute_mysql_query(query_string)[0]
        current_meal_data = execute_mysql_query(query_string)[0]
        query_string = f"""
                        SELECT
                            Type,
                            JSON_ARRAYAGG(
                                JSON_OBJECT(
                                    'Ingredient', Name,
                                    'Unit', Unit,
                                    'Quantity', "")
                                )
                                AS Ingredient_data
                        FROM {os.environ['MYSQL_DATABASE']}.{os.environ['MYSQL_INGREDIENTS_TABLE']}
                        GROUP BY Type;"""
        all_ingredient_data = execute_mysql_query(query_string)
        current_ingredients = {}
        for ingredient_type in all_ingredient_data:
            current_ingredients[ingredient_type['Type']] = append_current_ingredients(json.loads(ingredient_type['Ingredient_data']), json.loads(current_meal_data[f'{ingredient_type["Type"]}_Ingredients']))

        query_string = f"""SELECT DISTINCT(Staple) FROM {os.environ['MYSQL_DATABASE']}.{os.environ['MYSQL_TABLE']} ORDER BY Staple ASC;"""
        staples = execute_mysql_query(query_string)
        return render_template('edit_meal.html', meal_name=results['Name'], current_staple=results['Staple'],
                                book=results['Book'], page=results['Page'], website=results['Website'],
                                current_ingredients=current_ingredients, staples=staples,
                                books=book_list, current_tags=json.loads(results['Tags']))

    if request.method == "POST":
        details = request.form
        details_dict = details.to_dict()
        fresh_ing = parse_ingredients(details_dict, "Fresh ")
        tinned_ing = parse_ingredients(details_dict, "Tinned ")
        dry_ing = parse_ingredients(details_dict, "Dry ")
        dairy_ing = parse_ingredients(details_dict, "Dairy ")
        details_dict = update_tags(details_dict)
        query_string = f"UPDATE {os.environ['MYSQL_DATABASE']}.{os.environ['MYSQL_TABLE']} SET Name = '{details['Name']}', Staple = '{details['Staple']}', Book = '{details['Book']}', Page = '{details['Page']}', Website = '{details['Website']}', Fresh_Ingredients = '{fresh_ing}', Tinned_Ingredients = '{tinned_ing}', Dry_Ingredients = '{dry_ing}', Dairy_Ingredients = '{dairy_ing}', Spring_Summer = {details_dict['Spring_Summer']}, Autumn_Winter = {details_dict['Autumn_Winter']}, Quick_Easy = {details_dict['Quick_Easy']}, Special = {details_dict['Special']} WHERE (Name = '{details['Name']}');"
        print(query_string)
        execute_mysql_query(query_string, fetch_results=False, commit=True)
        return redirect(url_for('edit_meal.confirmation', meal=meal))


@edit_meal.route('/edit_confirmation/<meal>', methods=['GET'])
def confirmation(meal):
    template = meal_information(meal)
    return template
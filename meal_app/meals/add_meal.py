from flask import Blueprint, render_template, request, redirect, url_for
from ..utilities import execute_mysql_query, parse_ingredients, get_tags, meal_information
import os

add_meal = Blueprint('add_meal', __name__, template_folder='templates', static_folder='../static')

@add_meal.route('/add_meal', methods=['GET', 'POST'])
def main():
    from ..variables import staples_list, book_list, fresh_ingredients, tinned_ingredients, dry_ingredients, dairy_ingredients, tag_list
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
        return redirect(url_for('add.confirmation', meal = details['Name']))
    return render_template('add_meal.html', 
        len_staples = len(staples_list), staples = staples_list,
        len_books = len(book_list), books = book_list,
        len_fresh_ingredients = len(fresh_ingredients), fresh_ingredients = [ingredient[0] for ingredient in fresh_ingredients], fresh_ingredients_units = [ingredient[1] for ingredient in fresh_ingredients],
        len_tinned_ingredients = len(tinned_ingredients), tinned_ingredients = [ingredient[0] for ingredient in tinned_ingredients], tinned_ingredients_units = [ingredient[1] for ingredient in tinned_ingredients],
        len_dry_ingredients = len(dry_ingredients), dry_ingredients = [ingredient[0] for ingredient in dry_ingredients], dry_ingredients_units = [ingredient[1] for ingredient in dry_ingredients],
        len_dairy_ingredients = len(dairy_ingredients), dairy_ingredients = [ingredient[0] for ingredient in dairy_ingredients], dairy_ingredients_units = [ingredient[1] for ingredient in dairy_ingredients],
        len_tags = len(tag_list), tags = tag_list)


@add_meal.route('/confirmation/<meal>', methods=['GET'])
def confirmation(meal):
    template = meal_information(meal)
    return template
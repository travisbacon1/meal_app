from flask import Blueprint, render_template, request, redirect, url_for
from ..utilities import parse_ingredients
import os

add = Blueprint('add', __name__, template_folder='templates', static_folder='../static')

@add.route('/add', methods=['GET', 'POST'])
def index():
    from .. import mysql
    from .variables import staples_list, book_list, fresh_ingredients, tinned_ingredients, dry_ingredients, dairy_ingredients
    if request.method == "POST":
        details = request.form
        details_dict = details.to_dict()
        cur = mysql.connection.cursor()
        cur.execute(
            f"INSERT INTO {os.environ['MYSQL_TABLE']}(Name, Staple, Book, Page, Website, Fresh_Ingredients, Tinned_Ingredients, Dry_Ingredients, Dairy_Ingredients) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
            (details['Name'], details['Staple'], details['Book'], details['Page'], details['Website'], parse_ingredients(details_dict, "Fresh ", remove_prefix=True), parse_ingredients(details_dict, "Tinned ", remove_prefix=True), parse_ingredients(details_dict, "Dry ", remove_prefix=True), parse_ingredients(details_dict, "Dairy ", remove_prefix=True))
            )
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('add.index'))
    return render_template('add.html', 
        len_staples = len(staples_list), staples = staples_list,
        len_books = len(book_list), books = book_list,
        len_fresh_ingredients = len(fresh_ingredients), fresh_ingredients = fresh_ingredients,
        len_tinned_ingredients = len(tinned_ingredients), tinned_ingredients = tinned_ingredients,
        len_dry_ingredients = len(dry_ingredients), dry_ingredients = dry_ingredients,
        len_dairy_ingredients = len(dairy_ingredients), dairy_ingredients = dairy_ingredients)
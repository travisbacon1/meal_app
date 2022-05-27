from flask import Blueprint, render_template, request, redirect, url_for

home = Blueprint('home', __name__, template_folder="templates", static_folder='../static')

@home.route("/", methods=['GET', 'POST'])
def index():
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
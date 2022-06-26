from flask import Blueprint, render_template, request, redirect, url_for

home = Blueprint('home', __name__, template_folder="templates", static_folder='../static')

@home.route("/", methods=['GET', 'POST'])
def index():
    buttons = [
        "Add Ingredient",
        "Add Meal",
        "Edit Meal",
        "Find Meal",
        "Search Ingredients",
        "List Meals",
        "Create Meal Plan",
        "Load Meal Plan",
        "Delete Meal Plan"
    ]
    if request.method == "POST":
        url = request.form['submit'].lower().replace(' ', '_')
        return redirect(url_for(f'{url}.main'))

        # if request.form['submit'] == 'Add Ingredient':
        #     return redirect(url_for('add_ingredient.main'))
        # elif request.form['submit'] == 'Add Meal':
        #     return redirect(url_for('add_meal.main'))
        # elif request.form['submit'] == 'Edit Meal':
        #     return redirect(url_for('edit_meal.main'))
        # elif request.form['submit'] == 'Get Meal Info':
        #     return redirect(url_for('find_meal.main'))
        # elif request.form['submit'] == 'Search Ingredients':
        #     return redirect(url_for('search_ingredients.main'))
        # elif request.form['submit'] == 'List Meals':
        #     return redirect(url_for('list_meals.main'))
        # elif request.form['submit'] == 'Create Meal Plan':
        #     return redirect(url_for('create_meal_plan.main'))
        # elif request.form['submit'] == 'Load Meal Plan':
        #     return redirect(url_for('load_meal_plan.main'))
        # elif request.form['submit'] == 'Delete Meal Plan':
        #     return redirect(url_for('delete_meal_plan.main'))
    return render_template('index.html', buttons=buttons)
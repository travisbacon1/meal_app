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
    return render_template('index.html', buttons=buttons)
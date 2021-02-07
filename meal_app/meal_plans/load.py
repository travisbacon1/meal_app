from flask import Blueprint, render_template, request, redirect, url_for, session
import json

load = Blueprint('load', __name__, template_folder='templates', static_folder='static')

@load.route('/load', methods=['GET', 'POST'])
def choose_meal_plan():
    from glob import glob
    meal_plans = sorted([f.replace('.json', '').split('/')[1] for f in glob("saved_meal_plans/*.json")])
    if len(meal_plans) == 0:
        return render_template('no_meal_plans.html')
    if request.method == "POST":
        details = request.form
        return redirect(url_for('load.load_meal_plan', meal_plan = details['Meal Plan']))
    return render_template('load.html',
                            len_meal_plans = len(meal_plans), meal_plans = meal_plans)


@load.route('/load/<meal_plan>', methods=['GET', 'POST'])
def load_meal_plan(meal_plan):
    if request.method == "GET":
        with open(f"saved_meal_plans/{meal_plan}.json","r") as f:
            session['complete_ingredient_dict'] = json.load(f)
            f.close()
        return redirect(url_for('display.display_meal_plan'))
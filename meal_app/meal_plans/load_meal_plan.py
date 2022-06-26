from flask import Blueprint, render_template, request, redirect, url_for, session
import json
from glob import glob

load_meal_plan = Blueprint('load_meal_plan', __name__, template_folder='templates', static_folder='../static')

@load_meal_plan.route('/load_meal_plan', methods=['GET', 'POST'])
def main():
    meal_plans = sorted([f.replace('.json', '').split('/')[1] for f in glob("saved_meal_plans/*.json")])
    if len(meal_plans) == 0:
        return render_template('no_meal_plans.html')
    if request.method == "POST":
        details = request.form
        return redirect(url_for('load_meal_plan.load', meal_plan=details['Meal Plan']))
    return render_template('load_meal_plan.html',len_meal_plans=len(meal_plans), meal_plans=meal_plans)


@load_meal_plan.route('/load_meal_plan/<meal_plan>', methods=['GET'])
def load(meal_plan):
    if request.method == "GET":
        with open(f"saved_meal_plans/{meal_plan}.json","r") as f:
            session['complete_ingredient_dict'] = json.load(f)
        return redirect(url_for('display_meal_plan.main'))
from flask import Blueprint, render_template, request
from glob import glob
import os

delete = Blueprint('delete', __name__, template_folder='templates', static_folder='../static')

def delete_plans(meal_plan_list) -> None:
    """Deletes the selected meal plans from the local saved_meal_plans directory
    
    Parameters
    -------
    meal_plan_list: list

    Returns
    ------
    None
    """
    for meal_plan in meal_plan_list:
        os.remove(f"saved_meal_plans/{meal_plan}.json")
    print("All selected meal plans deleted")


@delete.route('/delete', methods=['GET', 'POST'])
def delete_meal_plan():
    meal_plans = [f.replace('.json', '').split('/')[1] for f in glob("saved_meal_plans/*.json")]
    if len(meal_plans) == 0:
        return render_template('no_meal_plans.html')
    if request.method == "POST":
        details_dict = request.form.to_dict()
        meal_plans_to_delete = [value for key, value in details_dict.items() if 'Meal Plan' in key]
        delete_plans(meal_plans_to_delete)
        return render_template('delete_complete.html')
    return render_template('delete.html', meal_plans = meal_plans)
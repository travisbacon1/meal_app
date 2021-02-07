from flask import Blueprint, render_template, request, session
import os
import json
from datetime import datetime

display = Blueprint('display', __name__, template_folder='templates', static_folder='../static')

def save_meal_plan(complete_ingredient_dict):
    """Saves created meal plan to the local saved_meal_plans directory
    
    Parameters
    -------
    complete_ingredient_dict: dict

    Returns
    ------
    file_path: string
    """
    if not os.path.exists('saved_meal_plans'):
        os.makedirs('saved_meal_plans')
    dt_string = datetime.now().strftime("%Y-%m-%d %H:%M")
    json_file = json.dumps(complete_ingredient_dict, indent=4)
    with open(f"saved_meal_plans/{dt_string}.json","w") as f:
        f.write(json_file)
        f.close()
    file_path = str(os.getcwd()) + f"/saved_meal_plans/{dt_string}.json"
    return file_path


@display.route('/display', methods=['GET', 'POST'])
def display_meal_plan():
    if request.method == "GET":
        complete_ingredient_dict = session.pop('complete_ingredient_dict')
        session['complete_ingredient_dict'] = complete_ingredient_dict
        fresh_ingredients = [list(complete_ingredient_dict["Fresh_Ingredients"].keys()), list(complete_ingredient_dict["Fresh_Ingredients"].values())]
        tinned_ingredients = [list(complete_ingredient_dict["Tinned_Ingredients"].keys()), list(complete_ingredient_dict["Tinned_Ingredients"].values())]
        dry_ingredients = [list(complete_ingredient_dict["Dry_Ingredients"].keys()), list(complete_ingredient_dict["Dry_Ingredients"].values())]
        dairy_ingredients = [list(complete_ingredient_dict["Dairy_Ingredients"].keys()), list(complete_ingredient_dict["Dairy_Ingredients"].values())]
        return render_template('display.html',
                            len_meal_list = len(complete_ingredient_dict['Meal_List']), meal_list=complete_ingredient_dict['Meal_List'],
                            len_fresh_ingredients = len(fresh_ingredients[0]), fresh_ingredients_keys=fresh_ingredients[0], fresh_ingredients_values=fresh_ingredients[1],
                            len_tinned_ingredients = len(tinned_ingredients[0]), tinned_ingredients_keys=tinned_ingredients[0], tinned_ingredients_values=tinned_ingredients[1],
                            len_dry_ingredients = len(dry_ingredients[0]), dry_ingredients_keys=dry_ingredients[0], dry_ingredients_values=dry_ingredients[1],
                            len_dairy_ingredients = len(dairy_ingredients[0]), dairy_ingredients_keys=dairy_ingredients[0], dairy_ingredients_values=dairy_ingredients[1],
                            len_extra_ingredients = len(complete_ingredient_dict['Extra_Ingredients']), extra_ingredients=complete_ingredient_dict['Extra_Ingredients'])

    if request.method == "POST" and request.form['submit'] == 'Save':
        complete_ingredient_dict = session.pop('complete_ingredient_dict')
        file_path = save_meal_plan(complete_ingredient_dict)
        return render_template('save_complete.html', file_path = file_path)
from flask import Flask, render_template, session, request, jsonify, url_for, redirect
from flask_mysqldb import MySQL
import json
import os
from string import Template
from tabulate import _table_formats, tabulate
import subprocess
from datetime import datetime
from glob import glob


app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


if os.path.isfile('credentials.txt'):
    with open("credentials.txt", "r") as reader:
        credentials = reader.readlines()
        credentials = [credential.strip("\n") for credential in credentials]
        reader.close()
    username = credentials[0]
    password = credentials[1]

else:
    username = input("Enter database user: ")
    password = input("Enter database password: ")

app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_PORT'] = 3306
app.config['MYSQL_USER'] = username
app.config['MYSQL_PASSWORD'] = password
app.config['MYSQL_DB'] = 'MealsDatabase'

mysql = MySQL(app)

def variable_printer(variable_name, variable):
    """Prints the name, type and contents of a variable to aid debugging
    
    Parameters
    -------
    variable_name: string\n
    variable: any

    Returns
    ------
    None
    """
    print(variable_name, "type:", type(variable), "content:")
    print(variable)


def parse_ingredients(ingredients_dict, filter_word):
    """Parses an ingredients dictionary to create a new dictionary based on the filter_word as the key
    
    Parameters
    -------
    ingredients_dict: dict\n
    filter_word: string

    Returns
    ------
    parsed_ingredient_dict: dict
    """
    parsed_ingredient_dict = {}
    for key in list(ingredients_dict.keys()):
        if filter_word in key and ingredients_dict[key] != '':
            new_key = key.removeprefix(filter_word)
            parsed_ingredient_dict[new_key] = ingredients_dict[key]
    return json.dumps(parsed_ingredient_dict)


def get_meal_info(meal_list):
    """Converts a list of meals into a string and uses this in an SQL query to get the information on these meals
    
    Parameters
    -------
    meal_list: list\n

    Returns
    ------
    result: tuple
    """
    meal_list = str(meal_list).strip("[]")
    db_cursor = mysql.connection.cursor()
    query = f"SELECT Fresh_Ingredients, Tinned_Ingredients, Dry_Ingredients, Dairy_Ingredients FROM MealsDatabase.MealsTable WHERE Name IN ({meal_list});"
    db_cursor.execute(query)
    results = db_cursor.fetchall()
    return results


def build_ingredient_dictionary(meal_ingredient_dict, deduped_ingredient_dict):
    """Adds together the quantities of all ingredients in a given deduped_ingredient_dict
    
    Parameters
    -------
    meal_ingredient_dict: dict\n
    deduped_ingredient_dict: dict

    Returns
    ------
    deduped_ingredient_dict: dict
    """
    ingredient_list = json.loads(meal_ingredient_dict)
    for ingredient in list(ingredient_list.keys()):
        if ingredient in deduped_ingredient_dict:
            deduped_ingredient_dict[ingredient] += float(ingredient_list[ingredient])
        else:
            deduped_ingredient_dict[ingredient] = float(ingredient_list[ingredient])
    return deduped_ingredient_dict


def collate_ingredients(meal_info_list):
    """Collates all ingredients from all meals into a dictionary of required ingredients
    
    Parameters
    -------
    meal_info_list: list

    Returns
    ------
    complete_deduped_ingredient_dict: dict
    """
    complete_deduped_ingredient_dict = {}
    fresh_ingredient_dict = {}
    tinned_ingredient_dict = {}
    dry_ingredient_dict = {}
    dairy_ingredient_dict = {}
    for meal in meal_info_list:
        if meal["Fresh_Ingredients"] != None:
            build_ingredient_dictionary(meal["Fresh_Ingredients"], fresh_ingredient_dict)
    
        if meal["Tinned_Ingredients"] != None:
            build_ingredient_dictionary(meal["Tinned_Ingredients"], tinned_ingredient_dict)

        if meal["Dry_Ingredients"] != None:
            build_ingredient_dictionary(meal["Dry_Ingredients"], dry_ingredient_dict)

        if meal["Dairy_Ingredients"] != None:
            build_ingredient_dictionary(meal["Dairy_Ingredients"], dairy_ingredient_dict)

        if meal["Dairy_Ingredients"] != None:
            build_ingredient_dictionary(meal["Dairy_Ingredients"], dairy_ingredient_dict)
    complete_deduped_ingredient_dict["Fresh_Ingredients"] = fresh_ingredient_dict
    complete_deduped_ingredient_dict["Tinned_Ingredients"] = tinned_ingredient_dict
    complete_deduped_ingredient_dict["Dry_Ingredients"] = dry_ingredient_dict
    complete_deduped_ingredient_dict["Dairy_Ingredients"] = dairy_ingredient_dict
    return complete_deduped_ingredient_dict


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
    dt_string = datetime.now().strftime("%d-%m-%Y %H:%M")
    json_file = json.dumps(complete_ingredient_dict, indent=4)
    with open(f"saved_meal_plans/{dt_string}.json","w") as f:
        f.write(json_file)
        f.close()
    file_path = str(os.getcwd()) + f"/saved_meal_plans/{dt_string}.json"
    return file_path


def delete_plans(meal_plan_list):
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


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == "POST":
        if request.form['submit'] == 'Add Meal':
            return redirect(url_for('add'))
        elif request.form['submit'] == 'Get Meal Info':
            return redirect(url_for('find'))
        elif request.form['submit'] == 'Search Ingredients':
            return redirect(url_for('search'))
        elif request.form['submit'] == 'List Meals':
            return redirect(url_for('list_meals'))
        elif request.form['submit'] == 'Create Meal Plan':
            return redirect(url_for('create_meal_plan'))
        elif request.form['submit'] == 'Load Meal Plan':
            return redirect(url_for('choose_meal_plan'))
        elif request.form['submit'] == 'Delete Meal Plan':
            return redirect(url_for('delete_meal_plan'))
    return render_template('index.html')


@app.route('/add', methods=['GET', 'POST'])
def add():
    from variables import staples_list, book_list, fresh_ingredients, tinned_ingredients, dry_ingredients, dairy_ingredients
    if request.method == "POST":
        details = request.form
        details_dict = details.to_dict()
        cur = mysql.connection.cursor()
        cur.execute(
            "INSERT INTO MealsTable(Name, Staple, Book, Page, Website, Fresh_Ingredients, Tinned_Ingredients, Dry_Ingredients, Dairy_Ingredients) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
            (details['Name'], details['Staple'], details['Book'], details['Page'], details['Website'], parse_ingredients(details_dict, "Fresh "), parse_ingredients(details_dict, "Tinned "), parse_ingredients(details_dict, "Dry "), parse_ingredients(details_dict, "Dairy "))
            )
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('add'))
    return render_template('add.html', 
        len_staples = len(staples_list), staples = staples_list,
        len_books = len(book_list), books = book_list,
        len_fresh_ingredients = len(fresh_ingredients), fresh_ingredients = fresh_ingredients,
        len_tinned_ingredients = len(tinned_ingredients), tinned_ingredients = tinned_ingredients,
        len_dry_ingredients = len(dry_ingredients), dry_ingredients = dry_ingredients,
        len_dairy_ingredients = len(dairy_ingredients), dairy_ingredients = dairy_ingredients)


@app.route('/find', methods=['GET', 'POST'])
def find():
    app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
    db_cursor = mysql.connection.cursor()
    query = f"SELECT Name FROM MealsDatabase.MealsTable;"
    db_cursor.execute(query)
    results = db_cursor.fetchall()
    meals = [result['Name'] for result in results]
    if request.method == "POST":
        details = request.form
        app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
        db_cursor = mysql.connection.cursor()
        query = f"SELECT * FROM MealsDatabase.MealsTable WHERE Name='{details['Meal']}';"
        db_cursor.execute(query)
        result = db_cursor.fetchall()
        return redirect(url_for('some_meal_page', meal = result[0]['Name']))
    return render_template('find.html',
                            len_meals = len(meals), meals = meals)


@app.route('/find/<meal>', methods=['GET', 'POST'])
def some_meal_page(meal):
    if request.method == "GET":
        app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
        db_cursor = mysql.connection.cursor()
        query = f"SELECT * FROM MealsDatabase.MealsTable WHERE Name='{meal}';"
        db_cursor.execute(query)
        result = db_cursor.fetchall()
        location_details = {}
        if result[0]['Website'] == None or result[0]['Website'] == '':
            location_details['Book'] = result[0]['Book']
            location_details['Page'] = result[0]['Page']
        else:
            location_details['Website'] = result[0]['Website']
        fresh_ingredients = [list(json.loads(result[0]['Fresh_Ingredients']).keys()), list(json.loads(result[0]['Fresh_Ingredients']).values())]
        tinned_ingredients = [list(json.loads(result[0]['Tinned_Ingredients']).keys()), list(json.loads(result[0]['Tinned_Ingredients']).values())]
        dry_ingredients = [list(json.loads(result[0]['Dry_Ingredients']).keys()), list(json.loads(result[0]['Dry_Ingredients']).values())]
        dairy_ingredients = [list(json.loads(result[0]['Dairy_Ingredients']).keys()), list(json.loads(result[0]['Dairy_Ingredients']).values())]
        return render_template('find_results.html', meal_name=meal,
                                location_details = location_details, location_keys = location_details.keys(),
                                staple = result[0]['Staple'],
                                len_fresh_ingredients = len(fresh_ingredients[0]), fresh_ingredients_keys=fresh_ingredients[0], fresh_ingredients_values=fresh_ingredients[1],
                                len_tinned_ingredients = len(tinned_ingredients[0]), tinned_ingredients_keys=tinned_ingredients[0], tinned_ingredients_values=tinned_ingredients[1],
                                len_dry_ingredients = len(dry_ingredients[0]), dry_ingredients_keys=dry_ingredients[0], dry_ingredients_values=dry_ingredients[1],
                                len_dairy_ingredients = len(dairy_ingredients[0]), dairy_ingredients_keys=dairy_ingredients[0], dairy_ingredients_values=dairy_ingredients[1])
    else:
        return redirect(url_for('find'))


@app.route('/search', methods=['GET', 'POST'])
def search():
    app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
    db_cursor = mysql.connection.cursor()
    query = f"SELECT Fresh_Ingredients, Tinned_Ingredients, Dry_Ingredients, Dairy_Ingredients FROM MealsDatabase.MealsTable WHERE json_length(Fresh_Ingredients) > 0;;"
    db_cursor.execute(query)
    results = db_cursor.fetchall()
    json_results = [json.loads(result['Fresh_Ingredients']) for result in results]
    fresh_ingredients = sorted(list(set(key for i in json_results for key in i.keys())))
    json_results = [json.loads(result['Tinned_Ingredients']) for result in results]
    tinned_ingredients = sorted(list(set(key for i in json_results for key in i.keys())))
    json_results = [json.loads(result['Dry_Ingredients']) for result in results]
    dry_ingredients = sorted(list(set(key for i in json_results for key in i.keys())))
    json_results = [json.loads(result['Dairy_Ingredients']) for result in results]
    dairy_ingredients = sorted(list(set(key for i in json_results for key in i.keys())))

    if request.method == "POST":
        details = request.form
        details_dict = details.to_dict()
        if "null" not in request.form["Fresh_Ingredients"]:
            json_key = "Fresh_Ingredients"
            ingredient = details_dict[json_key]
        elif "null" not in request.form["Tinned_Ingredients"]:
            json_key = "Tinned_Ingredients"
            ingredient = details_dict[json_key]
        elif "null" not in request.form["Dry_Ingredients"]:
            json_key = "Dry_Ingredients"
            ingredient = details_dict[json_key]
        elif "null" not in request.form["Dairy_Ingredients"]:
            json_key = "Dairy_Ingredients"
            ingredient = details_dict[json_key]
        app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
        db_cursor = mysql.connection.cursor()
        query = f"""SELECT * FROM MealsDatabase.MealsTable
                WHERE JSON_EXTRACT({json_key}, '$."{ingredient}"');"""
        db_cursor.execute(query)
        results = db_cursor.fetchall()
        session['meal_list'] = [result['Name'] for result in results]
        return redirect(url_for('search_results', ingredient = ingredient))
    return render_template('search.html', 
                            len_fresh_ingredients = len(fresh_ingredients), fresh_ingredients = fresh_ingredients,
                            len_tinned_ingredients = len(tinned_ingredients), tinned_ingredients = tinned_ingredients,
                            len_dry_ingredients = len(dry_ingredients), dry_ingredients = dry_ingredients,
                            len_dairy_ingredients = len(dairy_ingredients), dairy_ingredients = dairy_ingredients)


@app.route('/search/<ingredient>', methods=['GET', 'POST'])
def search_results(ingredient):
    if request.method == "GET":
        meals = session.pop('meal_list', [])
        return render_template('search_results.html', ingredient = ingredient, len_meals = len(meals), meals = meals)
    else:
        return redirect(url_for('search'))


@app.route('/list', methods=['GET', 'POST'])
def list_meals():
    if request.method == "GET":
        app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
        db_cursor = mysql.connection.cursor()
        query = "SELECT *, CAST(Page AS SIGNED) AS Page FROM MealsDatabase.MealsTable ORDER BY Book, Page;"
        db_cursor.execute(query)
        results = db_cursor.fetchall()
        results = [result for result in results]
        meal_names = [meal['Name'] for meal in results]
        staples = [meal['Staple'] for meal in results]
        books = [meal['Book'] for meal in results]
        page = [meal['Page'] for meal in results]
        website = [meal['Website'] for meal in results]
        return render_template('list_meals.html', len_meals = len(meal_names),
                                meal_names = meal_names, staples=staples,
                                books=books, page=page, website=website)
    elif request.method == "POST":
        if (request.form['submit']):
            details_dict = request.form.to_dict()
            meal = json.dumps(details_dict['submit']).replace('"', '')
            return redirect(url_for('some_meal_page', meal = meal))


@app.route('/create', methods=['GET', 'POST'])
def create_meal_plan():
    app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
    db_cursor = mysql.connection.cursor()
    query = f"SELECT GROUP_CONCAT(Name) as Meals, Staple FROM MealsDatabase.MealsTable GROUP BY Staple;"
    db_cursor.execute(query)
    results = db_cursor.fetchall()
    staples_dict = {str(item['Staple']): list(item['Meals'].split(',')) for item in results}
    staple_dict_keys =  list(staples_dict.keys())

    if request.method == "POST":
        details = request.form
        details_dict = details.to_dict()
        meal_list = [value for key, value in details_dict.items() if 'Meal' in key]
        meal_tuple = get_meal_info(meal_list)
        meal_list_dicts = [meal for meal in meal_tuple]
        complete_ingredient_dict = collate_ingredients(meal_list_dicts)
        complete_ingredient_dict['Extra_Ingredients'] = [value for key, value in details_dict.items() if 'Extra' in key]
        session['complete_ingredient_dict'] = complete_ingredient_dict
        return redirect(url_for('display_meal_plan'))
    from variables import extras
    return render_template('create_meal_plan.html',
                            len_bread_meals=len(staples_dict['Bread']), bread_meals=staples_dict['Bread'],
                            len_cous_cous_meals=len(staples_dict['Cous Cous']), cous_cous_meals=staples_dict['Cous Cous'],
                            len_pasta_meals=len(staples_dict['Pasta']), pasta_meals=staples_dict['Pasta'],
                            len_pastry_meals=len(staples_dict['Pastry']), pastry_meals=staples_dict['Pastry'],
                            len_potato_meals=len(staples_dict['Potato']), potato_meals=staples_dict['Potato'],
                            len_rice_meals=len(staples_dict['Rice']), rice_meals=staples_dict['Rice'],
                            len_extras = len(extras), extras = extras)


@app.route('/display', methods=['GET', 'POST'])
def display_meal_plan():
    if request.method == "GET":
        complete_ingredient_dict = session.pop('complete_ingredient_dict')
        session['complete_ingredient_dict'] = complete_ingredient_dict
        fresh_ingredients = [list(complete_ingredient_dict["Fresh_Ingredients"].keys()), list(complete_ingredient_dict["Fresh_Ingredients"].values())]
        tinned_ingredients = [list(complete_ingredient_dict["Tinned_Ingredients"].keys()), list(complete_ingredient_dict["Tinned_Ingredients"].values())]
        dry_ingredients = [list(complete_ingredient_dict["Dry_Ingredients"].keys()), list(complete_ingredient_dict["Dry_Ingredients"].values())]
        dairy_ingredients = [list(complete_ingredient_dict["Dairy_Ingredients"].keys()), list(complete_ingredient_dict["Dairy_Ingredients"].values())]
        return render_template('display_meal_plan.html',
                            len_fresh_ingredients = len(fresh_ingredients[0]), fresh_ingredients_keys=fresh_ingredients[0], fresh_ingredients_values=fresh_ingredients[1],
                            len_tinned_ingredients = len(tinned_ingredients[0]), tinned_ingredients_keys=tinned_ingredients[0], tinned_ingredients_values=tinned_ingredients[1],
                            len_dry_ingredients = len(dry_ingredients[0]), dry_ingredients_keys=dry_ingredients[0], dry_ingredients_values=dry_ingredients[1],
                            len_dairy_ingredients = len(dairy_ingredients[0]), dairy_ingredients_keys=dairy_ingredients[0], dairy_ingredients_values=dairy_ingredients[1],
                            len_extra_ingredients = len(complete_ingredient_dict['Extra_Ingredients']), extra_ingredients=complete_ingredient_dict['Extra_Ingredients'])

    if request.method == "POST":
        if request.form['submit'] == 'Save':
            complete_ingredient_dict = session.pop('complete_ingredient_dict')
            file_path = save_meal_plan(complete_ingredient_dict)
            return render_template('save_complete.html', file_path = file_path)


@app.route('/choose_meal_plan', methods=['GET', 'POST'])
def choose_meal_plan():
    meal_plans = [f.replace('.json', '').split('/')[1] for f in glob("saved_meal_plans/*.json")]
    if request.method == "POST":
        details = request.form
        return redirect(url_for('load_meal_plan', meal_plan = details['Meal Plan']))
    return render_template('choose_meal_plan.html',
                            len_meal_plans = len(meal_plans), meal_plans = meal_plans)


@app.route('/load_meal_plan/<meal_plan>', methods=['GET', 'POST'])
def load_meal_plan(meal_plan):
    if request.method == "GET":
        with open(f"saved_meal_plans/{meal_plan}.json","r") as f:
            session['complete_ingredient_dict'] = json.load(f)
            f.close()
        return redirect(url_for('display_meal_plan'))


@app.route('/delete_meal_plan', methods=['GET', 'POST'])
def delete_meal_plan():
    meal_plans = [f.replace('.json', '').split('/')[1] for f in glob("saved_meal_plans/*.json")]
    if request.method == "POST":
        details = request.form
        details_dict = details.to_dict()
        meal_plans_to_delete = [value for key, value in details_dict.items() if 'Meal Plan' in key]
        delete_plans(meal_plans_to_delete)
        return render_template('delete_complete.html')
    return render_template('delete_meal_plan.html',
                            len_meal_plans = len(meal_plans), meal_plans = meal_plans)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

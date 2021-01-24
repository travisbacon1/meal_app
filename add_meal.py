from flask import Flask, render_template, session, request, jsonify, url_for, redirect
from flask_mysqldb import MySQL
import json
import os
from string import Template
from tabulate import _table_formats, tabulate
import subprocess


app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


def configure_mqsql_server(action):
    process = subprocess.Popen(['sudo', '/usr/local/mysql/support-files/mysql.server', action],
                        stdout=subprocess.PIPE, 
                        stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    print(stdout.decode('utf-8'))
    print(stderr.decode('utf-8'))

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

def parse_ingredients(ingredients_dict, filter_word):
    parsed_ingredient_dict = {}
    excluded_keys = ['Name', 'Staple', 'Book', 'Page', 'Website']
    for key in list(ingredients_dict.keys()):
        if filter_word in key and ingredients_dict[key] != '' and key not in excluded_keys:
            new_key = key.removeprefix(filter_word)
            parsed_ingredient_dict[new_key] = ingredients_dict[key]
    return json.dumps(parsed_ingredient_dict)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == "POST":
        request.form
        if request.form['submit'] == 'Add Meal':
            return redirect(url_for('add'))
        elif request.form['submit'] == 'Get Meal Info':
            return redirect(url_for('find'))
        elif request.form['submit'] == 'Search Ingredients':
            return redirect(url_for('search'))
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
        if details['Meal'] == 'null':
            return render_template('find.html')
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


@app.route('/test', methods=['GET'])
def test():

    meal_name = "meal"
    ing_dict = {
        "Fresh Ingredients": {
            "Tomatoes": 5,
            "Courgettes": 6
        }
    }
    ingredients = list(ing_dict["Fresh Ingredients"].keys())
    quantities = list(ing_dict["Fresh Ingredients"].values())
    print(type(ingredients))
    row = ""
    for i, _ in enumerate(ingredients):
        row += f"""
            <tr>
                <td>{ingredients[i]}</td>
                <td>{quantities[i]}</td>
            </tr>"""
    html_template = """<!DOCTYPE html>
    <html>
        <head>
            <meta charset="utf-8" />
            <link rel= "stylesheet" type= "text/css" href= "{{ url_for('static',filename='styles/styles.css') }}">
        </head>
        """
    html_template += f"""
        <h1>Ingredients List</h1>
        <table>
            <tr>
                <th>Fresh Ingredients</th>
                <th>Quantity</th>
            </tr>{row}
        </table>
    </html>
        """
    with open("./templates/ingredients_list.html", "w") as file:
        file.write(html_template)

    return render_template("ingredients_list.html")


if __name__ == '__main__':
    # configure_mqsql_server('stop')
    app.run(host='0.0.0.0', debug=True)

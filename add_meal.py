from flask import Flask, render_template, request, jsonify, url_for, redirect
from flask_mysqldb import MySQL
import json
import os
from string import Template
from tabulate import _table_formats, tabulate

app = Flask(__name__)

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
        if request.form['submit'] == 'Get Meal Info':
            return redirect(url_for('find'))
    return render_template('index.html')

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == "POST":
        details = request.form
        name = details['Name']
        staple = details['Staple']
        book = details['Book']
        page = int(details['Page'])
        website = details['Website']
        details_dict = details.to_dict()
        fresh_ingredients = parse_ingredients(details_dict, "Fresh ")
        tinned_ingredients = parse_ingredients(details_dict, "Tinned ")
        dairy_ingredients = parse_ingredients(details_dict, "Dairy ")
        dry_ingredients = parse_ingredients(details_dict, "Dry ")
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO MealsTable(Name, Staple, Book, Page, Website, Fresh_Ingredients, Tinned_Ingredients, Dry_Ingredients, Dairy_Ingredients) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)", (name, staple, book, page, website, fresh_ingredients, tinned_ingredients, dry_ingredients, dairy_ingredients))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('add'))
    return render_template('add.html')


@app.route('/find', methods=['GET', 'POST'])
def find():
    html_template = """<!DOCTYPE html>
    <html>
        <head>
            <meta charset="utf-8" />
            <link rel= "stylesheet" type= "text/css" href= "{{ url_for('static',filename='styles/styles.css') }}">
        </head>
        	<body>
		        <form method="post", action="">
                    <H1>Meal Information</H1>
                    <ul>
                        <li>
                            <label for="meal">Meal:</label>
                            <select name="Meal" required>
                                <option value="null"></option>
        """
    app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
    db_cursor = mysql.connection.cursor()
    query = f"SELECT Name FROM MealsDatabase.MealsTable;"
    db_cursor.execute(query)
    results = db_cursor.fetchall()
    meals = [result['Name'] for result in results]
    for meal in meals:
        html_template += f"""<option value="{meal}">{meal}</option>
                            """
    html_template += """
                        </select>
                    </li>
                    <li>
					    <input class="button" type="submit">
				    </li>
                </ul>
            </form>
        </html>
                    """
    if request.method == "POST":
        details = request.form
        if details['Meal'] == 'null':
            return render_template('find.html')
        app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
        db_cursor = mysql.connection.cursor()
        query = f"SELECT * FROM MealsDatabase.MealsTable WHERE Name='{details['Meal']}';"
        # db_cursor = database.cursor(dictionary=True)
        db_cursor.execute(query)
        result = db_cursor.fetchall()
        return redirect(url_for('some_meal_page', meal = result[0]['Name']))
    with open("./templates/find.html", "w") as file:
        file.write(html_template)
    return render_template('find.html')

@app.route('/find/<meal>', methods=['GET', 'POST'])
def some_meal_page(meal):
    if request.method == "GET":
        HTML_TEMPLATE = Template("""
            <h1>Meal info for ${meal_name}!</h1>
                <p>${ingredients}</p>
                    <form method="post", action="">
                        <input class="button" type="submit" value="Return">
                    </form>
            """)
        app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
        db_cursor = mysql.connection.cursor()
        query = f"SELECT * FROM MealsDatabase.MealsTable WHERE Name='{meal}';"
        db_cursor.execute(query)
        result = db_cursor.fetchall()

        return(HTML_TEMPLATE.substitute(meal_name=meal, ingredients=result))
    else:
        return redirect(url_for('find'))

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
    app.run(host='0.0.0.0', debug=True)

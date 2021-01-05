from flask import Flask, render_template, request
from flask_mysqldb import MySQL
import json

app = Flask(__name__)

with open("credentials.txt", "r") as reader:
    credentials = reader.readlines()
    credentials = [credential.strip("\n") for credential in credentials]
    reader.close()

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = credentials[0]
app.config['MYSQL_PASSWORD'] = credentials[1]
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
        return render_template('index.html')
    return render_template('index.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

# Meal Planner

This Python flask app is designed to aid meal planning by cataloging your most frequently used meals and their ingredients, along with general food cupbooard items. This app provides a friendly user interface to a MySQL database holding this data, allowing you to list all your meals, find meals by ingredient, get specific meal information, and create, load, view and delete meal plans.

## Prequisites
* Git installed
* Python3.9 installed
* A MySQL server installed & running (preferably MySQL8)

## Getting started
* Clone this repo (`git clone git@github.com:travisbacon1/meal_app.git`) and navigate to the root directory (`cd meals`)
* `python3 -m venv env`
* Activate the virtual environment with the pre-configured script: `. venvActivate`
* Install the dependencies: `pip3 install -r requirements.txt`
* Load the sample data into the database: `python3 import_sample_data.py`
* Run the app: `python3 gui_app.py`
* Head to localhost:5000 in your browser (`0.0.0.0:5000`)
* Have a play!

## TODOs
* Update schema & app to support meal tags (i.e. type of meal, "special" meal etc. to aid searching)
* Add delete meal functionality
* Add functionality to choose serving size when creating meal plan
* Add support for ingredient units
* Refactor flask code to use blueprints
* Move methods to separate file
* Validate input to make sure it complies with MySQL database schema
* Write unit tests
* Improve CSS styling

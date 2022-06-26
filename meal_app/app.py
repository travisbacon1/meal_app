from flask import Flask
import jinja2
from sqlmodel import create_engine
import os

loader = jinja2.FileSystemLoader('templates')
environment = jinja2.Environment(loader=loader)
engine = create_engine(f'mysql+mysqldb://{os.environ["MYSQL_USER"]}:{os.environ["MYSQL_PASSWORD"]}@{os.environ["MYSQL_HOSTNAME"]}/{os.environ["MYSQL_DATABASE"]}', echo=True)


def create_app():
    """Initialize the core application."""
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object('config.Config')
    
    with app.app_context():
        # Include our Routes
        from .home.home import home
        from .ingredients.add_ingredient import add_ingredient
        from .ingredients.search_ingredients import search_ingredients
        from .meals.add_meal import add_meal
        from .meals.edit_meal import edit_meal
        from .meals.list_meals import list_meals
        from .meals.find_meal import find_meal
        from .meals.inspire import inspire
        from .meal_plans.create_meal_plan import create_meal_plan
        from .meal_plans.display_meal_plan import display_meal_plan
        from .meal_plans.load_meal_plan import load_meal_plan
        from .meal_plans.delete_meal_plan import delete_meal_plan

        # Register Blueprints
        app.register_blueprint(home)
        app.register_blueprint(add_ingredient)
        app.register_blueprint(search_ingredients)
        app.register_blueprint(add_meal)
        app.register_blueprint(edit_meal)
        app.register_blueprint(list_meals)
        app.register_blueprint(find_meal)
        app.register_blueprint(inspire)
        app.register_blueprint(create_meal_plan)
        app.register_blueprint(display_meal_plan)
        app.register_blueprint(load_meal_plan)
        app.register_blueprint(delete_meal_plan)

        return app


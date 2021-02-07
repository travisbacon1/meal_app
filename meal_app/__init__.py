from flask import Flask
from flask_mysqldb import MySQL
import os

# Globally accessible libraries
mysql = MySQL()


def create_app():
    """Initialize the core application."""
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object('config.Config')

    # Initialize Plugins
    mysql.init_app(app)

    with app.app_context():
        # Include our Routes
        from .home.home import home
        from .meals.add import add
        from .meals.list_meals import list_meals
        from .meals.find import find
        from .meals.search import search
        from .meal_plans.create import create
        from .meal_plans.display import display
        from .meal_plans.load import load
        from .meal_plans.delete import delete

        # Register Blueprints
        app.register_blueprint(home)
        app.register_blueprint(add)
        app.register_blueprint(list_meals)
        app.register_blueprint(find)
        app.register_blueprint(search)
        app.register_blueprint(create)
        app.register_blueprint(display)
        app.register_blueprint(load)
        app.register_blueprint(delete)

        return app
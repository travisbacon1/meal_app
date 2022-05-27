from flask import Flask
import jinja2

loader = jinja2.FileSystemLoader('templates')
environment = jinja2.Environment(loader=loader)

def create_app():
    """Initialize the core application."""
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object('config.Config')

    with app.app_context():
        # Include our Routes
        from .home.home import home
        from .ingredients.add_ingredient import add_ingredient
        from .meals.add import add
        from .meals.edit import edit
        from .meals.list_meals import list_meals
        from .meals.find import find
        from .meals.inspire import inspire
        from .meals.search import search
        from .meal_plans.create import create
        from .meal_plans.display import display
        from .meal_plans.load import load
        from .meal_plans.delete import delete

        # Register Blueprints
        app.register_blueprint(home)
        app.register_blueprint(add_ingredient)
        app.register_blueprint(add)
        app.register_blueprint(edit)
        app.register_blueprint(list_meals)
        app.register_blueprint(find)
        app.register_blueprint(inspire)
        app.register_blueprint(search)
        app.register_blueprint(create)
        app.register_blueprint(display)
        app.register_blueprint(load)
        app.register_blueprint(delete)

        return app
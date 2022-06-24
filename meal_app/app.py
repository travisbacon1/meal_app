from flask import Flask
import jinja2
# from flask_sqlalchemy import SQLAlchemy
from sqlmodel import Field, SQLModel, JSON, Column, create_engine
from typing import Optional, Dict, Pattern
import os
import re

loader = jinja2.FileSystemLoader('templates')
environment = jinja2.Environment(loader=loader)
# db = SQLAlchemy()
engine = create_engine(f'mysql+mysqldb://{os.environ["MYSQL_USER"]}:{os.environ["MYSQL_PASSWORD"]}@{os.environ["MYSQL_HOSTNAME"]}/{os.environ["MYSQL_DATABASE"]}', echo=True)


def create_app():
    """Initialize the core application."""
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object('config.Config')
    # engine.init_app(app)
    
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


# class TestTable2(db.Model):
#     __tablename__ = "TestTable2"
#     Name = db.Column(db.VARCHAR(45), primary_key=True)
#     Staple = db.Column(db.VARCHAR(45))
#     Book = db.Column(db.VARCHAR(45))
#     Page = db.Column(db.VARCHAR(45))
#     website = db.Column(db.VARCHAR(45))
#     Fresh_Ingredients = db.Column(db.JSON(45))
#     Tinned_Ingredients = db.Column(db.JSON(45))
#     Dry_Ingredients = db.Column(db.JSON(45))
#     Tinned_Ingredients = db.Column(db.JSON(45))
#     Last_Made = db.Column(db.DateTime)
#     Spring_Summer = db.Column(db.SmallInteger)
#     Autumn_Winter = db.Column(db.SmallInteger)
#     Quick_Easy = db.Column(db.SmallInteger)
#     Special = db.Column(db.SmallInteger)

    # def __repr__(self):
    #     return f'<Meal {self.Name}>'

class TestTable(SQLModel, table=True):
    __table_args__ = {'extend_existing': True}
    __tablename__ = "TestTable"
    Name: str = Field(primary_key=True)
    Staple: str
    Book: Optional[str] = None
    Page: Optional[str] = None
    website: Optional[str] = None
    Fresh_Ingredients: Dict = Field(default={}, sa_column=Column(JSON))
    Dairy_Ingredients: Dict = Field(default={}, sa_column=Column(JSON))
    Dry_Ingredients: Dict = Field(default={}, sa_column=Column(JSON))
    Tinned_Ingredients: Dict = Field(default={}, sa_column=Column(JSON))
    # Last_Made:  Optional[str] = None
    Last_Made:  Pattern[str] = re.compile(r'[0-9]{4}-[0-9]{2}-[0-9]{2}')
    Spring_Summer: Optional[int] = None
    Autumn_Winter: Optional[int] = None
    Quick_Easy: Optional[int] = None
    Special: Optional[int] = None

    def __repr__(self):
        return f'<Meal {self.Name}>'

    def __init__(self, Last_Made, **kwargs):
        if not re.match(r'[0-9]{4}-[0-9]{2}-[0-9]{2}', Last_Made):
            raise Exception('Invalid date format')
        else:
            return self

    # Needed for Column(JSON)
    class Config:
        arbitrary_types_allowed = True



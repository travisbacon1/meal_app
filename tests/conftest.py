import pytest
import sys
sys.path.append('../meal_app')
from meal_app.app import create_app
from meal_app.utilities import execute_mysql_query
from dotenv import load_dotenv

@pytest.fixture(scope='session', autouse=True)
def load_env():
    print("Loading .env")
    load_dotenv()


@pytest.fixture()
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
    })

    # other setup can go here

    yield app


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()


@pytest.fixture(scope='session', autouse=True)
def session():
    print("Creating table")
    query_string = f"""CREATE TABLE IF NOT EXISTS `test` (
        `Name` varchar(45) NOT NULL,
        `Unit` varchar(45) DEFAULT NULL,
        `Type` varchar(45) DEFAULT NULL,
        PRIMARY KEY (`Name`)
        )"""
    execute_mysql_query(query_string, fetch_results=False, commit=True)
    yield
    print("Tearing down table")
    query_string = f"""DROP TABLE `test`"""
    execute_mysql_query(query_string, fetch_results=False, commit=True)
import os
from secrets import token_urlsafe

# basedir = path.abspath(path.dirname(__file__))
# load_dotenv(path.join(basedir, '.env'))

def get_database_credentials():
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
    return username, password

"""Flask configuration."""

class Config(object):
    """Set Flask config variables."""

    TESTING = True
    DEBUG = True
    DEVELOPMENT = True
    FLASK_ENV = 'development'
    SECRET_KEY = token_urlsafe(16)

    # MYSQL_HOST = '127.0.0.1'
    # MYSQL_PORT = 3306
    # MYSQL_USER, MYSQL_PASSWORD = get_database_credentials()
    # MYSQL_DB = 'MealsDatabase'
    MYSQL_CURSORCLASS = 'DictCursor'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
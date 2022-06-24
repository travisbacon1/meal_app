from secrets import token_urlsafe
import os

"""Flask configuration."""

class Config(object):
    """Set Flask config variables."""

    TESTING = True
    DEBUG = True
    DEVELOPMENT = True
    FLASK_ENV = 'development'
    SECRET_KEY = token_urlsafe(16)
    MYSQL_CURSORCLASS = 'DictCursor'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = f'mysql+mysqlconnector://{os.environ["MYSQL_USER"]}:{os.environ["MYSQL_PASSWORD"]}@{os.environ["MYSQL_HOSTNAME"]}/{os.environ["MYSQL_DATABASE"]}'
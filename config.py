from secrets import token_urlsafe

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
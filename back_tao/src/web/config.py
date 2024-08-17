from os import getenv
from dotenv import load_dotenv


class Config(object):
    """
    Configuración base
    """

    SECRET_KEY = "secret"
    TESTING = False
    SESSION_TYPE = "filesystem"
    JWT_SECRET_KEY = "clave_recontra_secreta"
    JWT_TOKEN_LOCATION = ["headers"]
    JWT_ACCESS_COOKIE_NAME = "access_token_cookie"


class DevelopmentConfig(Config):
    """
    Configuracion de development.
    """

    load_dotenv()

    DB_USER = getenv("DB_USER")
    DB_PASS = getenv("DB_PASS")
    DB_HOST = getenv("DB_HOST")
    DB_NAME = getenv("DB_NAME")
    DB_PORT = getenv("DB_PORT")

    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_DATABASE_URI = (
        f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )

    MAIL_SERVER="smtp.gmail.com"
    MAIL_DEFAULT_SENDER="widearrow.ohmydog@gmail.com"
    MAIL_PORT=465
    MAIL_USERNAME="widearrow.ohmydog@gmail.com"
    MAIL_PASSWORD="xhrz lnue wccq zdsc"
    MAIL_USE_SSL=True

class ProductionConfig(Config):
    """
    Configuracion de produccion
    """

    DB_USER = "grupo14" 
    DB_PASS = "eAoujUBzECaLyNAtl9t4"
    DB_HOST = "localhost"
    DB_NAME = "grupo14"
    DB_PORT = "5432"

    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_DATABASE_URI = (
        f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )

    MAIL_SERVER="smtp.gmail.com"
    MAIL_DEFAULT_SENDER="widearrow.ohmydog@gmail.com"
    MAIL_PORT=465
    MAIL_USERNAME="widearrow.ohmydog@gmail.com"
    MAIL_PASSWORD="xhrz lnue wccq zdsc"
    MAIL_USE_SSL=True

config = {"development": DevelopmentConfig}
config = {"production": ProductionConfig}

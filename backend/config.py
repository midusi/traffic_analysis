from os import environ
from dotenv import load_dotenv


class Config(object):
    """
    Configuración base: en esta sección va toda la configuración que es común a todos.
    """

    load_dotenv()
    TESTING = False
    DEBUG = False
    PROPAGATE_EXCEPTIONS = True


class ProductionConfig(Config):
    """
    Configuración para producción. A esta no le den bola por ahora :)
    """

    DB_USER = environ.get("DB_USER")
    DB_PASS = environ.get("DB_PASS")
    DB_HOST = environ.get("DB_HOST")
    DB_NAME = environ.get("DB_NAME")
    SQLALCHEMY_DATABASE_URI = f"mysql://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}"


class DevelopmentConfig(Config):
    """
    Configuración para desarrollo. Pongan sus credenciales para desarrollo local

    DB_USER: Nombre de usuario
    DB_PASS: Password para la BD
    DB_HOST: 'localhost' es usualmente :/
    DB_NAME: Nombre de la base de datos
    """

    DB_USER = environ.get("DB_USER")
    DB_PASS = environ.get("DB_PASS")
    DB_HOST = environ.get("DB_HOST")
    DB_NAME = environ.get("DB_NAME")
    SQLALCHEMY_DATABASE_URI = f"mysql://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}"


class TestingConfig(Config):
    # Testing Configuration...

    DB_USER = environ.get("DB_USER")
    DB_PASS = environ.get("DB_PASS")
    DB_HOST = environ.get("DB_HOST")
    TEST_DB_NAME = environ.get("TEST_DB_NAME")
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_DATABASE_URI = f"mysql://{DB_USER}:{DB_PASS}@{DB_HOST}/{TEST_DB_NAME}"

    TESTING = True


config = {
    "production": ProductionConfig,
    "development": DevelopmentConfig,
    "testing": TestingConfig,
}

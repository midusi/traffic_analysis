from flask import Flask, render_template
from backend.config import config
from backend.models import database, seeds, prueba
from os import urandom
from backend.api import api_blueprint
from flask_jwt_extended import JWTManager
from backend.helpers.mail import mail


def create_app(env="development", static_folder="../../static"):

    app = Flask(__name__, static_folder=static_folder)

    # Configuro el entorno
    app.secret_key = urandom(24)
    app.config.from_object(config[env])

    # Inicializo la base de datos
    database.init_app(app)
    JWTManager(app)
    mail.init_app(app)

    # Registramos blueprint principal
    app.register_blueprint(api_blueprint)

    @app.get("/")
    def entry_point():
        return render_template("prueba.html", pruebas=prueba.list_pruebas())

    @app.cli.command(name="resetdb")
    def resetdb():
        """
        Función para reiniciar la base de datos. La forma de llamar a esta funcionalidad es mediante el
        comando "flask resetdb"
        """
        database.reset_db()

    @app.cli.command(name="seedsdb")
    def seedsdb():
        """
        Función para cargar la bd con datos genéricos. La forma de llamar a esta funcionalidad es mediante el
        comando "flask seedsdb"
        """
        seeds.run()

    return app

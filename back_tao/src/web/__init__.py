from os import walk
from flask_cors import CORS
from src.core.configuracion import get_mantenimiento
from flask import Flask, abort
from flask import render_template, flash, redirect, url_for, session as current_session
from flask_session import Session
from core import autenticacion
from src.web import error
from src.core import database
from src.web.config import config
from core.autenticacion.mail import mail
from src.web.config import config
from src.core import seeds
from src.web.controllers.configuracion import configuracion_bp

from src.web.rutas import registrar_bps
from src.web.helpers import autenticacion
from src.core.autenticacion import get_instituciones_by_id, es_superadmin
from flask_jwt_extended import JWTManager
from src.core import autenticacion_oauth

session = Session()
UPLOAD_FOLDER = 'C:/Fabricio/3 año/Proyecto/proyecto/grupo14/admin/src/web/files'

def create_app(env="development", static_folder="../../static"):
    """Inicializa la aplicación."""
    app = Flask(__name__, static_folder=static_folder)

    app.add_url_rule(
        "/uploads/<id>", endpoint="download_file", build_only=True
    )


    app.config.from_object(config[env])

    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    CORS(app, supports_credentials=True)
    jwt = JWTManager(app)
    session.init_app(app)
    database.init_app(app)
    mail.init_app(app)
    autenticacion_oauth.init_app(app)

    registrar_bps(app)

    @app.get("/")
    @autenticacion.no_necesita_login()
    def home():
        return render_template("index.html")

    app.register_error_handler(404, error.not_found_error)
    app.register_error_handler(401, error.unauthorized)
    app.register_error_handler(403, error.forbidden)

    app.jinja_env.globals.update(
        esta_autenticado=autenticacion.esta_autenticado,
        tiene_permiso=autenticacion.tiene_permiso,
    )

    @app.get("/mis-instituciones")
    @autenticacion.necesita_login()
    @autenticacion.check_mantenimiento()
    def mostrar_instituciones():
        user = autenticacion.buscar_usuario_por_email(current_session["usuario"])
        instituciones = get_instituciones_by_id(user.id)
        if user is not None:
            return render_template(
                "usuarios/instituciones-del-usuario.html",
                usuario=user,
                instituciones=instituciones,
            )
        else:
            flash("Usuario no encontrado", "error")
            return redirect(url_for("usuarios.index"))

    @app.get("/home")
    @autenticacion.necesita_login()
    def home_superadmin():
        user = autenticacion.buscar_usuario_por_email(current_session["usuario"])
        instituciones = get_instituciones_by_id(user.id)
        if user is not None:
            return render_template(
                "home.html",
                usuario=user,
            )
        else:
            flash("Usuario no encontrado", "error")
            return redirect(url_for("usuarios.index"))

    # database.initialize_db()
    from src.core.database import db
    import src.core.autenticacion.usuario
    import src.core.institucion.models
    import src.core.configuracion.models

    print("intentando migrar las tablas...")
    with app.app_context():
        db.create_all()
    print("migrado con exito.")

    @app.cli.command(name="resetdb")
    def resetdb():
        database.reset_db()

    @app.cli.command(name="seedsdb")
    def seedsdb():
        seeds.run()

    return app

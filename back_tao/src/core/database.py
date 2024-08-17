from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


def init_app(app):
    """
    Inicialización de la aplicación.
    """
    db.init_app(app)
    config_db(app)


def config_db(app):
    """
    Configuración de la aplicación.
    """

    @app.teardown_request
    def close_session(exception=None):
        db.session.close()


def reset_db():
    """Resetea la base de datos, crea las tablas que no fueron creadas"""
    print("Eliminando la BD ☠️")
    db.drop_all()
    print("Creando la BD 🥰")
    db.create_all()
    print("Listo el pollo 💋")

def initialize_db():
    print("Migrando las tablas a la bd ☠️")
    db.create_all()
    print("Listo el pollo 💋")

from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()


def init_app(app):
    """Inicializa la aplicación con bcrypt"""
    bcrypt.init_app(app)

from functools import wraps
from flask import session, abort, redirect, flash
from backend.models.usuario import (
    esta_activo,
    es_admin,
)


def esta_autenticado(session):
    """
    Verifica si el usuario está autenticado
    """
    return session.get("usuario") is not None


def esta_habilitado(session):
    """
    Verifica si el usuario está habilitado
    """
    return esta_activo(session["usuario"])


def es_administrador(session):
    """
    Verifica si el usuario es administrador
    """
    return es_admin(session["usuario"])


def necesita_login(admin=False):
    """
    Decorador que verifica si el usuario está autenticado,
    y si es administrador en caso que se pase admin=True como parametro
    @necesita_login(admin=True)
    """

    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not esta_autenticado(session):
                return abort(401)

            if not esta_habilitado(session):
                flash("Fuiste deshabilitado por el administrador.", "error")
                return redirect("/")

            if admin and not es_administrador(session):
                return abort(403)

            return f(*args, **kwargs)

        return decorated_function

    return decorator

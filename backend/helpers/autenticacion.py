from functools import wraps
from flask import session, abort, redirect, flash, url_for, render_template
from src.core.autenticacion import (
    listar_permisos_por_email_usuario,
    get_usuario_institucion_activa,
    buscar_usuario_por_email,
    esta_activo,
    listar_permisos_por_email_usuario_institucion,
    es_superadmin
)
from src.core.configuracion import get_mantenimiento

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


def necesita_login(permisos_requeridos=None):
    """
    Decorador que verifica si el usuario está autenticado,
    tiene permisos y está habilitado.
    @necesita_login(["permiso1, permiso2"])
    """

    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not esta_autenticado(session):
                return abort(401)

            if not esta_habilitado(session):
                flash("Fuiste deshabilitado por el administrador.", "error")
                return redirect("/")

            if permisos_requeridos:
                permisos_usuario = listar_permisos_por_email_usuario_institucion(
                    session["usuario"]
                )
                if not permisos_usuario:
                    return abort(403)

                for permiso in permisos_requeridos:
                    if permiso not in permisos_usuario:
                        return abort(403)

            return f(*args, **kwargs)

        return decorated_function

    return decorator


def no_necesita_login():
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if esta_autenticado(session) and not es_superadmin(session["usuario"]):
                return redirect("/mis-instituciones")
            elif esta_autenticado(session) and es_superadmin(session["usuario"]):
                return redirect("/home")
            return f(*args, **kwargs)

        return decorated_function

    return decorator

def tiene_permiso(permisos_requeridos=None):
    permisos_usuario = listar_permisos_por_email_usuario_institucion(session["usuario"])
    for permiso in permisos_requeridos:
        if permiso not in permisos_usuario:
            return False

    return True


def necesita_institucion_activa(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        email = session["usuario"]
        if email:
            usuario = buscar_usuario_por_email(email)
            institucion_activa = get_usuario_institucion_activa(usuario.id)
            if (usuario and institucion_activa) is not None:
                return f(
                    *args, **kwargs
                )  # El usuario tiene una institución activa, permito el acceso al controlador
        flash(
            "Por favor, activa una institución.", "error"
        )  # Acceso prohibido. Debes tener una institución activa.
        return redirect("/mis-instituciones")

    return decorated_function

def check_mantenimiento():
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            mant = get_mantenimiento()
            if esta_autenticado(session) and mant["estado"]:
                if session and not es_superadmin(session["usuario"]):
                    return render_template("mantenimiento.html", msg=mant["mensaje"])
            elif not esta_autenticado and mant["estado"]:
                return render_template("mantenimiento.html", msg=mant["mensaje"])
            
            return f(*args, **kwargs)
        
        return decorated_function
    return decorator
from flask import Blueprint, url_for, render_template, redirect, request, flash
from src.core.configuracion import get_configuracion, get_info_contacto, update_info_contacto, update_mantenimiento
from src.web.helpers.autenticacion import necesita_login
"""
PERMISOS:
- Super Administrador/a: show, update.
"""

configuracion_bp = Blueprint("configuracion", __name__, url_prefix="/config")

@configuracion_bp.get("/")
@necesita_login(["configuracion_show"])
def index():
    """ vista principal para acceder a la configuración """
    return render_template("configuracion/index.html", config=get_configuracion(), info=get_info_contacto())

@configuracion_bp.post("/info/update")
@necesita_login(["configuracion_update"])
def update_info():
    """actualiza los siguientes campos de configuracion:
    - cantidad de elementos mostrados en cada página del sistema (usado en las tablas/listas paginadas)
    - información de contacto que se muestra de cada institución (usado en la app pública)
    """
    cant_pag = request.form["cant-elementos-pag"]
    if int(cant_pag) < 1 or int(cant_pag) > 15:
        flash("Rango inválido", "error")
        return redirect(url_for("configuracion.index"))

    info_activos = [int(x) for x in list({k: v for k, v in request.form.items() if k.startswith('info-check')}.values())]

    update_info_contacto(cant_elementos_pag=cant_pag, info_contacto_activos=info_activos)
    return redirect(url_for("configuracion.index"))

@configuracion_bp.post("/mantenimiento/update")
@necesita_login(["configuracion_update"])
def update_mant():
    """actualiza los siguientes campos de configuración:
    - estado de mantenimiento del sitio Web (SÍ/NO)
    - mensaje mostrado a los usuarios que intenten acceder al sitio mientras el mantenimiento esté activo
    """
    try:
        mant = "mantenimiento-check" in request.form
        mant_msg = request.form["mantenimiento-msg"]

        if (len(mant_msg) < 10):
            raise Exception("Mensaje muy corto")
        update_mantenimiento(mantenimiento=mant, mantenimiento_msg=mant_msg)
        return redirect(url_for("configuracion.index"))
    except:
        flash("Hubo un error realizando la operación", "error")
        return redirect(url_for("configuracion.index"))
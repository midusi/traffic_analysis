from src.core.configuracion.models.configuracion import Configuracion
from src.core.configuracion.models.info_contacto import InfoContacto
from src.core.database import db

def create_configuracion(**kwargs):
    """crea el elemento de configuración del sistema"""
    config = Configuracion(**kwargs)

    db.session.add(config)
    db.session.commit()

    return config

def create_info_contacto(**kwargs):
    info = InfoContacto(**kwargs)

    db.session.add(info)
    db.session.commit()

    return info

def get_configuracion():
    """retorna el elemento con la configuración del sistema"""
    config = Configuracion.query.first()
    
    return config

def get_info_contacto():
    """retorna una lista con los campos de información de contacto y su estado actual (activo/no activo)"""
    info = InfoContacto.query.all()

    return info

def get_info_contacto_activos():
    info = InfoContacto.query.filter(InfoContacto.activo)

    return info

def get_mantenimiento():
    """retorna un diccionario que incluye la siguiente información sobre el mantenimiento:
        - "estado" (boolean): True si el mantenimiento está activado
        - "mensaje" (string): mensaje que se muestra en caso de que haya mantenimiento
    """
    config = Configuracion.query.first()

    return { "estado": config.mantenimiento, "mensaje": config.mantenimiento_msg }

def get_cant_elementos_pag():
    """retorna la cantidad de elementos que se muestran en cada paginado"""
    config = Configuracion.query.first()

    return config.cant_elementos_pag

def update_info_contacto(**kwargs):
    """actualiza la cantidad de elementos por página (en la configuración) y los campos activos de información de contacto"""
    config = Configuracion.query.first()
    config.cant_elementos_pag = kwargs["cant_elementos_pag"]

    info = InfoContacto.query.all()
    for x in info:
        x.activo = True if x.id in kwargs["info_contacto_activos"] else False

    db.session.commit()

def update_mantenimiento(**kwargs):
    config = Configuracion.query.first()
    config.mantenimiento = kwargs["mantenimiento"]
    config.mantenimiento_msg = kwargs["mantenimiento_msg"]

    db.session.commit()
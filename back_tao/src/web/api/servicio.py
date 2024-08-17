from flask import Blueprint, jsonify, request
from src.web.schemas.servicio import (
    servicio_schema,
    servicios_schema,
    servicios_paginados_schema,
    tipos_servicios_schema,
    tipo_schema,
)
from src.core.servicio import (
    get_servicio_by_id,
    list_tipos,
    listar_servicios_habilitados_paginated,
)
from src.core.configuracion import get_cant_elementos_pag

api_servicios_bp = Blueprint("servicio_api", __name__, url_prefix="/api/services")


@api_servicios_bp.get("/search")
def get_servicios_busqueda():
    """Devuelve los servicios pasandole page (default 1), per_page (default config)
    , una palabra clave y un tipo"""
    page = request.args.get("page", default=1, type=int)
    per_page = request.args.get("per_page", default=get_cant_elementos_pag(), type=int)
    palabra_clave = request.args.get("q", default=None, type=str)
    tipo = request.args.get("type", default=None, type=str)

    if palabra_clave is None:
        return {"error": "El parametro q (palabra clave) es obligatorio."}, 400

    servicios = listar_servicios_habilitados_paginated(
        page=page, per_page=per_page, palabra_clave=palabra_clave, tipo=tipo
    )

    servicios_dumps = servicios_schema.dump(servicios)

    datos_serializados = servicios_paginados_schema.dump(
        {
            "data": servicios_dumps,
            "page": page,
            "per_page": per_page,
            "total": servicios.total,
        }
    )
    return datos_serializados


@api_servicios_bp.get("/<id>")
def get_servicios_id(id):
    """Devuelve el detalle del servicio pasado como parametro"""

    servicio = get_servicio_by_id(id)
    if not servicio:
        return {"error": "No existe o no se encontró un servicio con ese id."}, 400

    datos = servicio_schema.dump(servicio)
    return datos


@api_servicios_bp.get("/types")
def get_tipos_servicios():
    """Obtiene el listado de tipos de servicios."""

    tipos = list_tipos()
    if not tipos:
        return {"error": "No se encontraron tipos de servicios"}, 400

    tipos_serializados = tipo_schema.dump(tipos)
    datos = tipos_servicios_schema.dump({"data": tipos_serializados})
    return datos

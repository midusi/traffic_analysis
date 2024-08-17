from flask import Blueprint, jsonify, request
from marshmallow import ValidationError

from src.web.schemas.institucion import (
    institucion_schema,
    instituciones_paginadas_schema,
)
from src.core.institucion import list_instituciones_paginated

api_instituciones_bp = Blueprint(
    "institucion_api", __name__, url_prefix="/api/institutions"
)


@api_instituciones_bp.get("/")
def get_instituciones():
    """Devuelve las instituciones pasandole page (default 1) y per_page"""
    page = request.args.get("page", default=1, type=int)
    per_page = request.args.get("per_page", default=1, type=int)

    instituciones = list_instituciones_paginated(page, per_page)
    instituciones_dumps = institucion_schema.dump(instituciones)

    datos_serializados = instituciones_paginadas_schema.dump(
        {
            "data": instituciones_dumps,
            "page": page,
            "per_page": per_page,
            "total": instituciones.total,
        }
    )

    return datos_serializados

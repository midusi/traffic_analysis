from flask import Blueprint, jsonify, abort
from flask_jwt_extended import jwt_required, get_jwt
from src.core.solicitudes import count_solicitudes_by_estado, get_servicios_mas_solicitados, count_solicitudes_by_institucion

api_stats_bp = Blueprint("stats_api", __name__, url_prefix="/api/stats")

@api_stats_bp.get("/")
@jwt_required()
def get_estadisticas():

    if not get_jwt()['es_admin']:
        return {"error": "No tenés permisos para acceder a esta información"}, 401
    
    solicitudes_por_estado = [{'estado_id': row.id, 'nombre': row.nombre, 'count': row.count} for row in count_solicitudes_by_estado()]
    servicios_mas_solicitados = [{'servicio_id': row.servicio_id, 'nombre': row.nombre, 'count': row.count} for row in get_servicios_mas_solicitados()]
    instituciones_solicitadas = [{'institucion_id': row.institucion_id, 'nombre': row.nombre, 'count': row.count} for row in count_solicitudes_by_institucion()]

    return jsonify({
        "solicitudes_por_estado": solicitudes_por_estado,
        "servicios_mas_solicitados": servicios_mas_solicitados,
        "instituciones_mas_solicitadas": instituciones_solicitadas
    })
from flask import Blueprint, request, jsonify
from werkzeug.exceptions import UnsupportedMediaType
from backend.models.ia import encolar
from backend.models.schemas.modelo import modelo_schema
from marshmallow import ValidationError

modelo_bp = Blueprint("modelo", __name__, url_prefix="/modelo")


@modelo_bp.post("/encolar")
def encolarVideo():
    """
    Recibe nombre/¿id? del video y los poligonos y lo encola en pendientes
    """
    try:
        req_data = request.json
    except UnsupportedMediaType as err:
        return {"error": repr(err)}, 400

    try:
        data_validada = modelo_schema.load(req_data)
    except ValidationError as err:
        return {"error": repr(err)}, 400

    # imprimir_data(data_validada)
    encolar(data_validada)

    return jsonify({"message": "Se recibió el video para procesar"}), 200

def imprimir_data(data_validada):
    print("Resolución:", data_validada['res'])
    print("Path:", data_validada['path'])
    for i, polygon in enumerate(data_validada['polygons']):
        print(f"Polígono {i + 1}:")
        print(f"  Tipo: {polygon['tipo']}")
        print(f"  Nombre: {polygon['name']}")
        print("  Puntos:")
        for point in polygon['points']:
            print(f"    {point}")



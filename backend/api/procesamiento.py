from flask import Blueprint, request, jsonify
from werkzeug.exceptions import UnsupportedMediaType
# from models.ia.ia import run

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

    

    print(req_data)
    print(req_data['polygons'])
    return jsonify({"message": "Se recibió el video para procesar"}), 200
    
# def procesarVideo():

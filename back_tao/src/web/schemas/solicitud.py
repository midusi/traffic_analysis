from marshmallow import fields, Schema
from src.web.schemas.servicio import ServicioSchema

class CrearAnotacionSchema(Schema):
    text = fields.Str(required=True)
class AnotacionSchema(Schema):
    contenido = fields.Str(required=False)
    publicado_por = fields.Str(required=False)
    fecha = fields.Str(required=False)

class EstadoSchema(Schema):
    id = fields.Int(required=True)
    nombre = fields.Str(required=True)

class CambioEstadosSchema(Schema):
    estado = fields.Nested(EstadoSchema)
    fecha = fields.Str(required=True)
    comentario = fields.Str(required=False)

class SolicitudSchema(Schema):
    id = fields.Int(required=True)
    fecha_creacion = fields.Str(required=False)
    detalle = fields.Str(required=True)
    archivos_adjuntos = fields.Str(required=False)
    anotaciones = fields.Nested(AnotacionSchema, many=True)
    nombre_servicio = fields.Str(load_only=True, required=True)
    estado_actual = fields.Nested(EstadoSchema)
    servicio = fields.Nested(ServicioSchema)
    cambios_estado = fields.Nested(CambioEstadosSchema, many=True)

class SolicitudesPaginadasSchema(Schema):
    data = fields.Nested(SolicitudSchema, many=True)
    page = fields.Int(required=True)
    per_page = fields.Int(required=True)
    total = fields.Int(required=True)
    has_previous = fields.Boolean(required=True)
    has_next = fields.Boolean(required=True)

class NuevaSolicitudSchema(Schema):
    usuario_id = fields.Int(required=True)
    detalle = fields.Str(required=True)
    nombre_servicio = fields.Str(required=True)
    servicio_id = fields.Int(required=True)


solicitud_schema = SolicitudSchema()
solicitudes_schema = SolicitudSchema(many=True)
solicitudes_paginadas_schema = SolicitudesPaginadasSchema()
crear_anotacion_schema = CrearAnotacionSchema()
nueva_solicitud_schema=NuevaSolicitudSchema()
estado_schema=EstadoSchema()

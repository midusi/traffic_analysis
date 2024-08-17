from marshmallow import fields, Schema


class InstitucionSchema(Schema):
    nombre = fields.Str(required=True)
    info = fields.Str(required=True)
    direccion = fields.Str(required=True)
    localizacion = fields.Str(required=True)
    web = fields.Str(required=True)
    horario_atencion = fields.Str(required=True)
    contacto = fields.Str(required=True)
    habilitado = fields.Bool(required=True)


class InstitucionesPaginadasSchema(Schema):
    data = fields.Nested(InstitucionSchema, many=True)
    page = fields.Int(required=True)
    per_page = fields.Int(required=True)
    total = fields.Int(required=True)


institucion_schema = InstitucionSchema(many=True)
instituciones_paginadas_schema = InstitucionesPaginadasSchema()

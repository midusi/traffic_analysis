from marshmallow import fields, Schema


class PerfilSchema(Schema):
    username = fields.Str(required=True)
    email = fields.Str(required=True)
    nombre = fields.Str(required=True)
    apellido = fields.Str(required=True)
    activo = fields.Bool(required=True)


perfil_schema = PerfilSchema()

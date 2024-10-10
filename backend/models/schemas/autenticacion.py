from marshmallow import fields, Schema


class AutenticacionSchema(Schema):
    id = fields.Int(dump_only=True)
    email = fields.Str(required=True)
    password = fields.Str(required=True)


class PerfilSchema(Schema):
    username = fields.Str(required=True)
    email = fields.Str(required=True)
    nombre = fields.Str(required=True)
    apellido = fields.Str(required=True)
    activo = fields.Bool(required=True)
    admin = fields.Bool(required=True)


autenticacion_schema = AutenticacionSchema()
perfil_schema = PerfilSchema()

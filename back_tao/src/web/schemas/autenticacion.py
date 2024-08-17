from marshmallow import fields, Schema


class AutenticacionSchema(Schema):
    id = fields.Int(dump_only=True)
    email = fields.Str(required=True)
    password = fields.Str(required=True)


autenticacion_schema = AutenticacionSchema()

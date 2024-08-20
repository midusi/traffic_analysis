from marshmallow import Schema, fields, validate


class RegistroSchema(Schema):
    nombre = fields.String(required=True, validate=validate.Length(min=1, max=25))
    apellido = fields.String(required=True, validate=validate.Length(min=1, max=25))
    email = fields.Email(required=True)
    password = fields.String(required=True, validate=validate.Length(min=8))
    admin = fields.Boolean(required=True)


class ConfirmarRegistroSchema(Schema):
    email = fields.Email(required=True)
    password = fields.String(required=True, validate=validate.Length(min=8, max=255))


class RecuperarContraseñaSchema(Schema):
    email = fields.Email(required=True)


# Crear una instancia del esquema para usar en la validación
registro_schema = RegistroSchema()
confirmar_registro_schema = ConfirmarRegistroSchema()
recuperar_contraseña_schema = RecuperarContraseñaSchema()

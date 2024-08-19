from marshmallow import Schema, fields


class PruebaSchema(Schema):
    name = fields.Str()

prueba_schema = PruebaSchema(many=True)
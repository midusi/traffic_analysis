from marshmallow import fields, Schema, validate

class PolygonSchema(Schema):
    tipo = fields.String(required=True, validate=validate.OneOf(["Entrada", "Salida", "Exclusion"]))
    points = fields.List(fields.List(fields.Float(), validate=validate.Length(equal=2)), required=True)
    name = fields.String(required=True)

class ModeloSchema(Schema):
    polygons = fields.List(fields.Nested(PolygonSchema), required=True)
    res = fields.List(fields.Integer(), required=True, validate=validate.Length(equal=2))
    path = fields.Str(required=True)

modelo_schema = ModeloSchema();

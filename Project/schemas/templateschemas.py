from marshmallow import Schema, fields

class TempalateSchema(Schema):
    template_name = fields.Str(required=False)
    subject = fields.Str(required=False)
    body = fields.Str(required=False)
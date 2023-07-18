from marshmallow import Schema, fields

class RegisterSchema(Schema):
    first_name  = fields.Str(required=True)
    last_name  = fields.Str(required=True)
    email = fields.Str(required=True)
    password = fields.Str(required=True)
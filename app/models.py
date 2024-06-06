from marshmallow import Schema, fields, validate


class UserSchema(Schema):
    username = fields.Str(required=True, validate=validate.Length(min=1))
    password = fields.Str(required=True, validate=validate.Length(min=1))
    email = fields.Email(required=True)
    user_image = fields.Str()
    user_video = fields.Str()
    user_pdf = fields.Str()


user_schema = UserSchema()

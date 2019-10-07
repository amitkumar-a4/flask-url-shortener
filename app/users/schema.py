from marshmallow import Schema, fields


class UserSchema(Schema):
    """
    /users - POST && /users/login - POST
    Parameters:
     - email (str)
     - password (str)
    """
    email = fields.Email(required=True)
    password = fields.Str(required=True)

from marshmallow import Schema, fields


class UrlSchema(Schema):
    """ /urls - POST

    Parameters:
     - url (str)
    """
    url = fields.Url(required=True)

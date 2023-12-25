from marshmallow import Schema, fields


#WTF IS THIS? A Marshmallow Schemas that takes the data incoming from the API
#validate them before sending them to the database, checking is it's in the right format
# for example: name must be an String and Age must be an Integer, otherwise it will return an error
# This Class we uses as arguments or response for our blueprints.
class PlainUserSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.String(required=True)
    age = fields.Int(required=True)
    cpf = fields.String(required=True)
    city = fields.String(required=True)
    profession = fields.String(required=True)
    email = fields.String(required=True )

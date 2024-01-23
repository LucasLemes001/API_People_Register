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



#Okay, down hare we find a Schema that will take the incoming data and validate it
# The big difference between this Schema and the PlainUserSchema is that
    #this one Will NOT return the datas with the "LOAD_ONLY=TRUE" argument
    # returning the data just like this:
    # { "name": "Mary", 
    #  "city": "São Paulo",
    # "profession": "Software Engineer",
    # "email": "Maryemail@.com." }
class ProfessionalsSchema(Schema):
    id = fields.Int(load_only=True)
    name = fields.String(required=True)
    age = fields.Int(required=True, load_only=True)
    cpf = fields.String(required=True, load_only=True)
    city = fields.String(required=True)
    profession = fields.String(required=True)
    email = fields.String(required=True)


# THE LOGIN SCHEMA, have one ID, that we will not return
    # username that must string, and returnable,
    # and a password, that we will not return NEVER.
    # the password will be hashed before it stores it in the database
    # and the result will be something like this:
    # { id: 1, 
    # "username": "Mary", 
    # "password": "$pbkdf2-sha256$29000$HYNQipGy9j4H4Pw/h/CeMw$KISYg7CNp8pQpha.qJ/iziwYTI67EkCTZmpX90W2adU"
    # }
class LoginSchema(Schema):
    id = fields.Int(load_only=True)
    username = fields.String(required=True)
    password = fields.String(required=True, load_only=True) #Remember to NEVER return passwords


# The BlocklistSchemas will take the incoming data and validate it.
    # only charge the revoked tokens id if we ask to do so
    # and take the revoked tokens stored in the database
class BlocklistSchemas(Schema):
    id = fields.Int(dump_only=True)
    revoked_token = fields.String(required=True, load_only=True)
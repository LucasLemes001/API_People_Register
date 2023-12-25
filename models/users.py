#HARE WE GOING TO DEAL WITH USERS DB MODEL TABLES
#We Create a Class and inherit from db.Model
#We create a __tablename__ and all of the columns we want
#the columns have nullable=False means that they cannot be null data, must have something
#the columns have unique=True means that they cannot be repeated
from db import db

class UsersModel(db.Model):
    __tablename__ = "users registered"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    cpf = db.Column(db.String(11), unique=True, nullable=False)
    city = db.Column(db.String(80), nullable=False)
    profession = db.Column(db.String(80), nullable=True)
    email = db.Column(db.String(80), unique=True, nullable=False)

    
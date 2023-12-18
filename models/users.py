#HARE WE GOING TO DEAL WITH USERS DB MODEL TABLES
from db import db

class UsersModel(db.Model):
    __tablename__ = "users registered"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    cpf = db.Column(db.String(11), unique=True)
    city = db.Column(db.String(80), nullable=False)
    profession = db.Column(db.String(80), nullable=True)
    email = db.Column(db.String(80), unique=True)

    
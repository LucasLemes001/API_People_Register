from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import db
from models.users import UsersModel
from resources.schemas import PlainUserSchema
from sqlalchemy.exc import SQLAlchemyError
from flask import request
'''
Explaning the code:
 1. First we create a blueprint named "users" and stores the data into a "blp" variable.
 2. Then when we call the route(defined by @blp.route("/routename")), we use the blueprint to runs the class(does't matter the Class Name) and inherit from MethodView class.
 3. Then we create a response, that it will take the incoming data and passit into the schema.
 4. After validate the data, he does what the function needs to do.
 The function name is what we expect to an endpoint, like get, post, put, delete,
 so we dont have do to something like this "@blp.route("/routename"), methots=["GET"])"
 beacuse the method is defined by the function's name.
 '''

blp = Blueprint("users", __name__, description="Operations on users")

@blp.route("/users")
class User(MethodView):
    @blp.response(200, PlainUserSchema(many=True), description="Get all users")
    def get(self):   # Intended to get all users listed into the DB
        all_users = UsersModel.query.all()
        
        return all_users


@blp.route("/newusers") #Intended to create a new user
class NewUser(MethodView):
    @blp.arguments(PlainUserSchema)
    @blp.response(200, PlainUserSchema, description="Create a new user")
    def post(self, user_data): # Intended to create a new user
        
        if UsersModel.query.filter(UsersModel.cpf == user_data["cpf"]).first():
                abort(409, message="User with this cpf already exists")
        
        
        
        if UsersModel.query.filter(UsersModel.email == user_data["email"]).first():
            abort(409, message="User with this email already exists")  # Check if user email already exists
        
        
        new_user = UsersModel(**user_data)
        db.session.add(new_user)
        db.session.commit()
        
        return new_user, 201
    
@blp.route("/users/<int:id>")
class UserById(MethodView):
    
    @blp.response(200, PlainUserSchema, description="Get an existing user")
    
    def get(self, id):  # Intended to return a single user by his ID
        try:
            user = UsersModel.query.get_or_404(id)
            return user
        
        
        except:
            abort(404, message="User not found")

    
    
    @blp.response(200, PlainUserSchema, description="Delete an existing user")
    def delete(self, id): #Intended to delete a user by his ID
       
        try:
            get_user = UsersModel.query.get_or_404(id)
            db.session.delete(get_user)
            db.session.commit()
            return {"message": "User deleted!!"}, 200
        
        
        except:
            abort(404, message="User not found")


    @blp.response(200, PlainUserSchema, description="Update an existing user")
    def put(self, id): # Intended to modify a user by his ID
       
        user = UsersModel.query.get(id)
        user_data = request.get_json()

        if user: 
            user.name = user_data["name"]
            user.age = user_data["age"]
            user.cpf = user_data["cpf"]
            user.city = user_data["city"]
            user.profession = user_data["profession"]
            user.email = user_data["email"]
       
       
        else:
            user = UsersModel(**user_data,id=id)
    
        db.session.add(user)
        db.session.commit()
        return user
        




    
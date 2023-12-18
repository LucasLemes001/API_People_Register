from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import db
from models.users import UsersModel
from resources.schemas import PlainUserSchema
from sqlalchemy.exc import SQLAlchemyError



blp = Blueprint("users", __name__, description="Operations on users")

@blp.route("/users")
class User(MethodView):
    @blp.response(200, PlainUserSchema(many=True))
    def get(self):   # Intended to get all users listed into the DB
        all_users = UsersModel.query.all()
        
        return all_users


@blp.route("/newusers") #Intended to create a new user
class NewUser(MethodView):
    @blp.arguments(PlainUserSchema)
    @blp.response(201, PlainUserSchema)
    def post(self, user_data): # Intended to create a new user
        
        if UsersModel.query.filter(UsersModel.cpf == user_data["cpf"]).first():  # Check if user already exists
            abort(409, message="User already exists")
        new_user = UsersModel(**user_data)
        db.session.add(new_user)
        db.session.commit()
        return {"message":"New User Registered","user":new_user},201
    





@blp.route("/users/<int:id>")
class UserById(MethodView):
    @blp.response(200, PlainUserSchema)
    def get(self, id):  # Intended to return a single user by his ID
        try:
            user = UsersModel.query.get_or_404(id)
            return user
        except SQLAlchemyError:
            abort(404, message="User not found")

    @blp.response(200, PlainUserSchema)
    def delete(self, id): #Intended to delete a user by his ID
        try:
            get_user = UsersModel.query.get_or_404(id)
            db.session.delete(get_user)
            db.session.commit()
            return {"message": "User deleted!!"},200
        except SQLAlchemyError:
            abort(404, message="User not found")


    
    


    def put(self, id): # Intended to modify a user by his ID
        pass
    
        # data = request.get_json()
        # user = users[id]
        # user |= data
        # return user

    
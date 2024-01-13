from db import db
from models import LoginModel
from flask_smorest import Blueprint, abort
from flask.views import MethodView
from resources.schemas import LoginSchema
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity, get_jwt
from passlib.hash import pbkdf2_sha256


blp = Blueprint("login", __name__, description="Operations on login")


# Down hare, this "/register" enpoint will create a "new member"
# We going to take the incoming data (Username and Passwords)
# Check if the username already exists
# If doesnt exist, then we take his password and cript it
# Then Stores it in the database
@blp.route("/register")
class RegisterLogin(MethodView):
    @blp.arguments(LoginSchema)
    def post(self, login_data):
        if LoginModel.query.filter(LoginModel.username == login_data["username"]).first():
            abort(409, message="User with that username already exists")

        new_user = LoginModel(
            username=login_data["username"],
            password = pbkdf2_sha256.hash(login_data["password"]),
        )
        
        db.session.add(new_user)
        db.session.commit()

        return {"message": "User created successfully"}, 201
    

# This "/registerdperson/<int:user_id>" endpoint will take
    # the Id of the user and return it:
     #his ID, and his username.
        # We will never show the password of the user
@blp.route("/registeredperson/<int:user_id>")
class RegisteredPerson(MethodView):
    @blp.response(200,LoginSchema)
    def get(self, user_id):
        the_user = LoginModel.query.get_or_404(user_id)
        return the_user
    

@blp.route("/deleteregister/<int:user_id>")
class UnregisterPerson(MethodView):
    # @blp.response(200,LoginSchema)    THIS IS COMMENTED BECAUSE IF INST SO, THE MESSAGE WILL NOT BE PRINTED
    def delete(self, user_id):
        the_user = LoginModel.query.get_or_404(user_id)

        db.session.delete(the_user)
        db.session.commit()
        
        return {"message": "User deleted"}, 200   #THIS MESSAGE INST BEEN PRINTED!! FIX IT
    

    

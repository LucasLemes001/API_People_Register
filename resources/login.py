from db import db
from models import LoginModel, BlocklistModel
from flask_smorest import Blueprint, abort
from flask.views import MethodView
from resources.schemas import LoginSchema, BlocklistSchemas
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity, get_jwt
from passlib.hash import pbkdf2_sha256


blp = Blueprint("login", __name__, description="Operations on login/register/unregister.")


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
            abort(409, message="This username already exists")

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
    

    

# EXPLANING THE CODE BELOW:
    # tHE endpoint "login" will recive the incoming data (username and password)
    # check the username in the database -> if exists
    # than we hash the password and compare with the password in the database
    # if it matches, then we create a token, and refresh token, and return them
    # if not, then we return an error
@blp.route("/login")
class Login(MethodView):
    @blp.arguments(LoginSchema)
    def post(self, incoming_data):

        user = LoginModel.query.filter(LoginModel.username == incoming_data["username"]).first()

        if user and pbkdf2_sha256.verify(incoming_data["password"], user.password):
            access_token = create_access_token(identity=user.username, fresh=True) 
            refresh_token = create_refresh_token(identity=user.username)

            return {"access_token": access_token, "refresh_token": refresh_token}, 200

        abort(401, message="Username or Password is incorrect!")

#IMPORTANT NOTES FOR POSTMAN:
        #To IMPROVE YOUR TIME ON PASSING THE AUTH RESPONSE VALUE, DEFINE SOME ENVOIREMENT VARIABLE:
        # USE THIS CODE BELLOW ON TEST SCREN RIGHT UNDET THE ENDPOINT URL
        # ON THE LOGIN ENDPOINT WHERE YOU RECIVE THE ACCESS TOKEN AND REFRESH TOKEN
        # ON TEST SCREN TYPE:
#             '''
#             let response = pm.response.json();
# pm.environment.set("access_token", response["access_token"]);
# pm.environment.set("refresh_token", response["refresh_token"]);
#             '''

# THEN GO ON AUTH IN THE ENDPOINT YOU WANT TO PROTECT AND PUT:
        # BEARER TOKEN: "Bearer {{access_token}}"
        

@blp.route("/refresh")
class Refresh(MethodView):
    @jwt_required(refresh=True)
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        return {"access_token": new_token}
    


@blp.route("/logout")
class logout(MethodView):
    @jwt_required()
    @blp.response(200,BlocklistSchemas)
    def post(self):
        jti = get_jwt()["jti"]
        revoked_token = BlocklistModel(
            revoked_token = jti
        )
        db.session.add(revoked_token)
        db.session.commit()
       
       
        return {"message": "Successfully logged out"}
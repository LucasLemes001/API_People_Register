import os
from flask import Flask, jsonify
from flask_smorest import Api
from db import db
from flask_jwt_extended import JWTManager
from sqlalchemy import desc
from models import BlocklistModel




from resources.users import blp as Userblueprint
from resources.login import blp as Loginblueprint

def create_app(db_url=None):
    app = Flask(__name__)
    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "People Register"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or os.getenv("DATABASE_URL", "sqlite:///data.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)
    api = Api(app)
    app.config["JWT_SECRET_KEY"] = "120475130852511602680261797632296015338"
    jwt = JWTManager(app)
    


    # IMPORTANT TASK ###
        # 1 Create a Identety to identify the ADMIN
        # 2 Create the bloacklist Model, schemas and verification system
    @jwt.additional_claims_loader
    def additional_claims_to_jwt(identity):
        # Look into the detabase and see whether the user is an admin
        if identity == 1:
            return {"is_admin": True}
        return {"is_admin": False}
    


    @jwt.token_in_blocklist_loader
    def is_token_blocked(jwt_header, jwt_payload):
        return BlocklistModel.query.filter_by(revoked_token=jwt_payload["jti"]).first()

    
    @jwt.revoked_token_loader
    def revoked_token(jwt_header, jwt_payload):
         return(
            jsonify(
                {"descrition":"The Token has been revoked.","error":"token_revoked"}
            )
        ), 401


    @jwt.expired_token_loader
    def expired_token(jwt_header, jwt_error):
        return(
            jsonify(
                {"description":"The Token has expired, please log in again.","error":"token_expired"}
            )
        ), 401


    @jwt.invalid_token_loader
    def invalid_token(error):
        return(
            jsonify(
                {"description":"Signature verification failed.","error":"invalid_token"}
            )
        ), 401
    

    @jwt.unauthorized_loader
    def missing_token(error):
        return(
            jsonify(
                {"description":"Request does not contain an access token. Please Log In","error":"authorization_required"}
            )
        ), 401



    @jwt.needs_fresh_token_loader
    def token_not_fresh(error):
        return(
            jsonify(
                {"description":"The token is not fresh.","error":"fresh_token_required"}

            )
        ), 401





    with app.app_context():
        db.create_all()

    api.register_blueprint(Userblueprint)
    api.register_blueprint(Loginblueprint)
    return app








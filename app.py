import os
from flask import Flask
from flask_smorest import Api
from db import db


from resources.users import blp as Userblueprint

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
    


    with app.app_context():
        db.create_all()

    api.register_blueprint(Userblueprint)

    return app







# @app.get("/users")
# def get_users():
#     return users


# @app.get("/users/<int:id>")
# def get_especific_user(id):
#     for user in users:
#           if user["id"] == id:
#             return user
#     return {"message": "User not found"}

# @app.post("/newusers")
# def create_user():
#     new_data = request.get_json()
#     for user in users:
#         if user["name"] == new_data["name"]:
#             return "User already exists"
#     new_name = new_data["name"]
#     new_age = new_data["age"]
#     id = len(users) + 1
#     users.append({"name": new_name, "age": new_age, "id": id})
#     return {"message": "User created!"}


# @app.delete("/deleteuser/<int:id>")
# def delete_user(id):
#     for user in users:
#         if user["id"] == id:
#             users.remove(user)
#             return "User deleted"
#     return "User not found"


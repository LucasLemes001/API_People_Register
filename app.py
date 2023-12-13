from flask import Flask, request
from flask_smorest import Api, abort
from db import users

app = Flask(__name__)

@app.get("/users")
def get_users():
    return users


@app.get("/users/<int:id>")
def get_especific_user(id):
    for user in users:
          if user["id"] == id:
            return user
    return {"message": "User not found"}

@app.post("/newusers")
def create_user():
    new_data = request.get_json()
    for user in users:
        if user["name"] == new_data["name"]:
            return "User already exists"
    new_name = new_data["name"]
    new_age = new_data["age"]
    id = len(users) + 1
    users.append({"name": new_name, "age": new_age, "id": id})
    return {"message": "User created!"}


@app.delete("/deleteuser/<int:id>")
def delete_user(id):
    for user in users:
        if user["id"] == id:
            users.remove(user)
            return "User deleted"
    return "User not found"


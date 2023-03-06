from flask import Blueprint
from app.controllers.user_controller import UserController

users_bp = Blueprint("users", __name__)
users_bp.route("", methods=["POST"])(UserController.create)
users_bp.route("", methods=["GET"])(UserController.list)
users_bp.route("/login", methods=["POST"])(UserController.login)
users_bp.route("/validation/<encrypted_email>", methods=["GET"])(
    UserController.user_validation
)

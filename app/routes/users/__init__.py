from flask import Blueprint
from app.controllers.user_controller import UserController

users_bp = Blueprint('users', __name__)
users_bp.route('', methods=['POST'])(UserController.create)
<<<<<<< HEAD
=======
users_bp.route('', methods=['GET'])(UserController.list)
>>>>>>> e85246450d871000a2ae4bb0838dcf3bb183511b
users_bp.route('/login', methods=['POST'])(UserController.login)

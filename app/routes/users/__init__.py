from flask import Blueprint
from app.controllers.user_controller import UserController

users_bp = Blueprint('users', __name__)
users_bp.route('/new', methods=['POST'])(UserController.create)
users_bp.route('/login', methods=['POST'])(UserController.login)

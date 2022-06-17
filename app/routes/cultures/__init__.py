from flask import Blueprint
from app.controllers.culture_controller import CultureController

cultures_bp = Blueprint('cultures', __name__)
cultures_bp.route('', methods=['POST'])(CultureController.create)

from flask import Blueprint
from app.controllers.culture_controller import CultureController

cultures_bp = Blueprint('cultures', __name__)
cultures_bp.route('', methods=['POST'])(CultureController.create)
cultures_bp.route('delete', methods=['DELETE'])(CultureController.delete)
cultures_bp.route('update', methods=['PATCH'])(CultureController.update)
cultures_bp.route('/irrigation-zone/<irrigation_zone_id>', methods=['GET'])(CultureController.list)
cultures_bp.route('/<culture_id>', methods=['GET'])(CultureController.show)
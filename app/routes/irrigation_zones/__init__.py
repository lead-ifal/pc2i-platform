from flask import Blueprint
from app.controllers.zone_controller import ZoneController

irrigation_zones_bp = Blueprint('irrigation_zones', __name__)
irrigation_zones_bp.route('/new', methods=['POST'])(ZoneController.create)
irrigation_zones_bp.route('/user/<user_id>', methods=['GET'])(ZoneController.list)

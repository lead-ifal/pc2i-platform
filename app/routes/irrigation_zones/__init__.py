from flask import Blueprint
from app.controllers.zone_controller import ZoneController

irrigation_zones_bp = Blueprint('irrigation-zones', __name__)
irrigation_zones_bp.route('', methods=['POST'])(ZoneController.create)
irrigation_zones_bp.route('/<zone_id>', methods=['GET'])(ZoneController.show)
irrigation_zones_bp.route('/irrigate/<zone_id>', methods=['GET'])(ZoneController.toggle_irrigation)
irrigation_zones_bp.route('/user/<user_id>', methods=['GET'])(ZoneController.list)
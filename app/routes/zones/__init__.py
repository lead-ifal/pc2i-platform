from flask import Blueprint
from app.controllers.zone_controller import ZoneController

zones_bp = Blueprint('zones', __name__)
zones_bp.route('/new', methods=['POST'])(ZoneController.create)
zones_bp.route('/user/<user_id>', methods=['GET'])(ZoneController.list)

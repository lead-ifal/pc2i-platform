from flask import Blueprint
from app.controllers.sensor_type_controller import SensorTypeConstroller

sensor_types_bp = Blueprint("sensors-types", __name__)
sensor_types_bp.route("", methods=["POST"])(SensorTypeConstroller.create)
sensor_types_bp.route("", methods=["GET"])(SensorTypeConstroller.list)

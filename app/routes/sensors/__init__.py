from flask import Blueprint
from app.controllers.sensor_controller import SensorController

sensors_bp = Blueprint("sensors", __name__)
sensors_bp.route("", methods=["POST"])(SensorController.create)
sensors_bp.route("/irrigation-zone/<irrigation_zone_id>", methods=["GET"])(
    SensorController.list
)
sensors_bp.route("/<sensor_id>/<value>", methods=["POST"])(SensorController.publish)
sensors_bp.route("/readings", methods=["GET"])(SensorController.list_readings)

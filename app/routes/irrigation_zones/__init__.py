from flask import Blueprint
from app.controllers.zone_controller import ZoneController

irrigation_zones_bp = Blueprint("irrigation-zones", __name__)
irrigation_zones_bp.route("", methods=["POST"])(ZoneController.create)
irrigation_zones_bp.route("", methods=["PATCH"])(ZoneController.update)
irrigation_zones_bp.route("", methods=["DELETE"])(ZoneController.delete)
irrigation_zones_bp.route("schedule", methods=["DELETE"])(
    ZoneController.delete_schedule
)
irrigation_zones_bp.route("schedule", methods=["PATCH"])(ZoneController.update_schedule)
irrigation_zones_bp.route("/schedule-irrigation", methods=["POST"])(
    ZoneController.schedule_irrigation
)
irrigation_zones_bp.route("/<zone_id>", methods=["GET"])(ZoneController.show)
irrigation_zones_bp.route("/irrigate/<zone_id>", methods=["GET"])(
    ZoneController.toggle_irrigation
)
irrigation_zones_bp.route("/user/<user_id>", methods=["GET"])(ZoneController.list)
irrigation_zones_bp.route("/<zone_id>/schedules", methods=["GET"])(
    ZoneController.schedule_irrigation_list
)

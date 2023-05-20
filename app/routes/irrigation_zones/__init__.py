from flask import Blueprint
from app.controllers.zone_controller import ZoneController
from app.controllers.schedule_controller import ScheduleController

irrigation_zones_bp = Blueprint("irrigation-zones", __name__)
irrigation_zones_bp.route("", methods=["POST"])(ZoneController.create)
irrigation_zones_bp.route("/<irrigation_zone_id>", methods=["PATCH"])(
    ZoneController.update
)
irrigation_zones_bp.route("/<irrigation_zone_id>", methods=["DELETE"])(
    ZoneController.delete
)
irrigation_zones_bp.route("schedule/<schedule_id>", methods=["DELETE"])(
    ScheduleController.delete_schedule
)
irrigation_zones_bp.route("schedule/<schedule_id>", methods=["PATCH"])(
    ScheduleController.update_schedule
)
irrigation_zones_bp.route("/schedule-irrigation", methods=["POST"])(
    ScheduleController.schedule_irrigation
)
irrigation_zones_bp.route("/<zone_id>", methods=["GET"])(ZoneController.show)
irrigation_zones_bp.route("/irrigate/<zone_id>", methods=["GET"])(
    ZoneController.toggle_irrigation
)
irrigation_zones_bp.route("/user/<user_id>", methods=["GET"])(ZoneController.list)
irrigation_zones_bp.route("/<zone_id>/schedules", methods=["GET"])(
    ScheduleController.schedule_irrigation_list
)

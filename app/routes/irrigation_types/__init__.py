from flask import Blueprint
from app.controllers.irrigation_type_controller import IrrigationTypeController

irrigation_types_bp = Blueprint("irrigation-types", __name__)
irrigation_types_bp.route("", methods=["GET"])(
    IrrigationTypeController.irrigation_types_list
)
irrigation_types_bp.route("/<type_id>", methods=["GET"])(
    IrrigationTypeController.irrigation_types_show
)

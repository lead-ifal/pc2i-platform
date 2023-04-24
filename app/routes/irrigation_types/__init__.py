from flask import Blueprint
from app.controllers.type_controller import TypeController

irrigation_types_bp = Blueprint("irrigation-types", __name__)
irrigation_types_bp.route("", methods=["GET"])(TypeController.irrigation_types_list)
irrigation_types_bp.route("/<type_id>", methods=["GET"])(
    TypeController.irrigation_types_show
)

from app.controllers.global_controller import GlobalController
from app.constants.status_code import HTTP_SUCCESS_CODE
from app.constants.response_messages import  SUCCESS_MESSAGE

from app.constants.irrigation_types import irrigation_types

class TypeController:
    def irrigation_types_list():
        return GlobalController.generate_response(HTTP_SUCCESS_CODE, SUCCESS_MESSAGE, irrigation_types)

    def irrigation_types_show(type_id):
        irrigation_type=irrigation_types[int(type_id)]
        return GlobalController.generate_response(HTTP_SUCCESS_CODE, SUCCESS_MESSAGE, irrigation_type)
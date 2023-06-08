from bson import ObjectId
from functools import wraps
from flask import request
from app.constants.response_messages import UNAUTHORIZED_API_KEY_MESSAGE
from app.constants.status_code import HTTP_UNAUTHORIZED_CODE
from app.controllers.global_controller import GlobalController
from app.models.irrigation_zone import IrrigationZone


def verify_api_key_by_user_id(id, api_key):
    return id == api_key


def access_control(levels):
    def decorator(route_function):
        @wraps(route_function)
        def main(*args, **kwargs):
            api_key = request.headers.get("Authorization")
            id = list(kwargs.values())[0]
            try:
                if levels == 0:
                    if verify_api_key_by_user_id(id, api_key):
                        return route_function(*args, **kwargs)

                elif levels == 1:
                    irrigation_zone = IrrigationZone.get_irrigation_zone_by_id(id)

                elif levels == 2:
                    irrigation_zone = IrrigationZone.get_irrigation_zone_by_entity_id(
                        id
                    )

                if irrigation_zone["user_id"] == ObjectId(api_key):
                    return route_function(*args, **kwargs)

                raise Exception()
            except:
                return GlobalController.generate_response(
                    HTTP_UNAUTHORIZED_CODE, UNAUTHORIZED_API_KEY_MESSAGE
                )

        return main

    return decorator

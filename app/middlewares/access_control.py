from bson import ObjectId
from functools import wraps
from flask import request
from typing import Collection
from app.constants.response_messages import INTERNAL_SERVER_ERROR_MESSAGE
from app.constants.status_code import HTTP_SERVER_ERROR_CODE
from app.controllers.global_controller import GlobalController
from app.extensions import database


cultures: Collection = database.db.cultures
irrigation_zones: Collection = database.db.irrigation_zones
scheduled_irrigations: Collection = database.db.scheduled_irrigations


def access_control(route_function):
    @wraps(route_function)
    def main(*args, **kwargs):
        api_key = request.headers.get("Authorization")
        id = list(kwargs.values())[0]
        try:
            if "irrigation_zone_id" in kwargs:
                irrigation_zone = irrigation_zones.find_one({"_id": ObjectId(id)})
            elif "culture_id" in kwargs:
                culture = cultures.find_one({"_id": ObjectId(id)})
                irrigation_zone = irrigation_zones.find_one(
                    {"_id": culture["irrigation_zone_id"]}
                )
            elif "schedule_id" in kwargs:
                schedule = scheduled_irrigations.find_one({"_id": ObjectId(id)})
                irrigation_zone = irrigation_zones.find_one(
                    {"_id": schedule["irrigation_zone_id"]}
                )
            else:
                if id == api_key:
                    return route_function(*args, **kwargs)
                else:
                    raise Exception()

            if irrigation_zone["user_id"] == ObjectId(api_key):
                return route_function(*args, **kwargs)

            raise Exception()
        except:
            return GlobalController.generate_response(
                HTTP_SERVER_ERROR_CODE, INTERNAL_SERVER_ERROR_MESSAGE
            )

    return main

from functools import wraps
from app.constants.status_code import HTTP_BAD_REQUEST_CODE
from app.constants.response_messages import ERROR_MESSAGE
from app.controllers.global_controller import GlobalController


def check_mongodb_id(route_function):
    @wraps(route_function)
    def main(*args, **kwargs):
        MONGODB_ID_LENGTH = 24
        id = list(kwargs.values())[0]
        if len(id) == MONGODB_ID_LENGTH:
            return route_function(*args, **kwargs)

        else:
            return GlobalController.generate_response(
                HTTP_BAD_REQUEST_CODE, ERROR_MESSAGE
            )

    return main

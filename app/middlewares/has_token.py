from functools import wraps
from flask import request
from typing import Collection
from app.controllers.global_controller import GlobalController
from app.extensions import database
from app.constants.status_code import HTTP_UNAUTHORIZED_CODE
from app.constants.response_messages import UNAUTHORIZED_MESSAGE
import os
users: Collection = database.db.users

def has_token(route_function):
  @wraps(route_function)
  def main(*args, **kwargs):
    if os.getenv("DEV_MODE") == "True":
      return route_function(*args, **kwargs)
    token = request.headers.get('token')

    if token is None:
      return GlobalController.generate_response(HTTP_UNAUTHORIZED_CODE, UNAUTHORIZED_MESSAGE)

    else:
      try:
        count = users.count_documents({ 'token': token })

        if count == 0:
          raise Exception()

        return route_function(*args, **kwargs)

      except:
        return GlobalController.generate_response(HTTP_UNAUTHORIZED_CODE, UNAUTHORIZED_MESSAGE)

  return main

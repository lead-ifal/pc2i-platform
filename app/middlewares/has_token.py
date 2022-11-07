from functools import wraps
from flask import request
from typing import Collection
from config import Config
from app.controllers.global_controller import GlobalController
from app.extensions import database
from app.constants.status_code import HTTP_UNAUTHORIZED_CODE
from app.constants.response_messages import UNAUTHORIZED_MESSAGE

users: Collection = database.db.users

def has_token(route_function):
  @wraps(route_function)
  def main(*args, **kwargs):
    token = request.headers.get('token')
    if token is None and Config.DEV_MODE is False:
      return GlobalController.generate_response(HTTP_UNAUTHORIZED_CODE, UNAUTHORIZED_MESSAGE)

    elif token is not None or Config.DEV_MODE is True:
      try:
        if token is None:
          count = users.count_documents({'token' : 'dev' })
        else:  
          count = users.count_documents({ 'token': token })

        if count == 0:
          raise Exception()

        return route_function(*args, **kwargs)

      except:
        return GlobalController.generate_response(HTTP_UNAUTHORIZED_CODE, UNAUTHORIZED_MESSAGE)

  return main

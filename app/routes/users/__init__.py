from flask import Blueprint

users_routes = Blueprint('users', __name__)

import bcrypt
from flask import request
from app.models.user import User
from app.controllers.user_controller import UserController
from app.controllers.global_controller import GlobalController
from app.constants.status_code import HTTP_BAD_REQUEST_CODE, HTTP_CREATED_CODE, HTTP_SUCCESS_CODE
from app.constants.response_messages import ERROR_MESSAGE, SUCCESS_MESSAGE
from typing import Collection
from app import database

users: Collection = database.users

@users_routes.route('/user/new', methods = ['POST'])
def create():
  required_params = ['name', 'email', 'password']
  body = request.get_json()
  includes_params = GlobalController.includes_all_required_params(required_params, body)

  try:
    if includes_params:
      user_exists = UserController.user_already_exists(body['email'], users)['exists']

      if user_exists:
        raise Exception()

      body['password'] = UserController.encode_password(body['password'])
      user = User(**body)
      users.insert_one(user.dict())

      return GlobalController.generate_response(
        HTTP_CREATED_CODE,
        SUCCESS_MESSAGE,
        user.dict(exclude={'password'})
      )

    raise Exception()

  except:
    return GlobalController.generate_response(HTTP_BAD_REQUEST_CODE, ERROR_MESSAGE)

@users_routes.route('/user/login', methods=['POST'])
def read():
  required_params = ['email', 'password']
  body = request.get_json()
  includes_params = GlobalController.includes_all_required_params(required_params, body)

  try:
    if includes_params:
      user_data = UserController.user_already_exists(body['email'], users)
      user_exists = user_data['exists']

      if user_exists:
        user = User(**user_data['data'])
        password_is_correct = bcrypt.checkpw(body['password'].encode(), user.password)

        if password_is_correct:
          return GlobalController.generate_response(
            HTTP_SUCCESS_CODE,
            SUCCESS_MESSAGE,
            user.dict(exclude={'password'})
          )

    raise Exception()

  except:
    return GlobalController.generate_response(HTTP_BAD_REQUEST_CODE, ERROR_MESSAGE)

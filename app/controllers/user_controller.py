import bcrypt
from flask import request
from typing import Collection
from bson import ObjectId
from app.extensions import database
from app.middlewares.has_token import has_token
from app.models.user import User
from app.controllers.global_controller import GlobalController
from app.constants.status_code import HTTP_BAD_REQUEST_CODE, HTTP_CREATED_CODE, HTTP_SUCCESS_CODE
from app.constants.response_messages import ERROR_MESSAGE, SUCCESS_MESSAGE
from app.constants.required_params import required_params

users: Collection = database.db.users

class UserController():

  def encode_password(password: str):
    try:
      salt = bcrypt.gensalt()

    except Exception as err:
      print(err)
      raise Exception()

    encoded_password = password.encode('utf8')
    hash = bcrypt.hashpw(encoded_password, salt)

    return hash
  
  def user_already_exists(email: str):
    user_already_exists = True

    saved_user = users.find_one({ 'email': email })

    if saved_user is None:
      user_already_exists = False

    return { 'exists': user_already_exists, 'data': saved_user }

  def create():
    body = request.get_json()
    params = required_params['users']['create']
    includes_params = GlobalController.includes_all_required_params(params, body)

    try:
      if includes_params:
        user_exists = UserController.user_already_exists(body['email'])['exists']

        if user_exists:
          raise Exception()
        
        body['password'] = UserController.encode_password(body['password'])
        body['token'] = ObjectId()
        user = User(**body)
        result = users.insert_one(user.dict(exclude_none=True))
        user_data = user.dict(exclude_none=True, exclude={'password'})
        user_data['_id'] = result.inserted_id

        return GlobalController.generate_response(
          HTTP_CREATED_CODE,
          SUCCESS_MESSAGE,
          user_data
        )

      raise Exception()

    except:
      return GlobalController.generate_response(HTTP_BAD_REQUEST_CODE, ERROR_MESSAGE)

  @has_token
  def list():
    users_list = users.find({}, {"password":0 })
    data = []

    for user in users_list:

      data.append(user)

    return GlobalController.generate_response(HTTP_SUCCESS_CODE, SUCCESS_MESSAGE, data)


  def login():
    body = request.get_json()
    params = required_params['users']['read']
    includes_params = GlobalController.includes_all_required_params(params, body)

    try:
      if includes_params:
        user_data = UserController.user_already_exists(body['email'])
        user_exists = user_data['exists']

        if user_exists:
          user = User(**user_data['data'])
          password_is_correct = bcrypt.checkpw(body['password'].encode(), user.password)

          if password_is_correct:
            return GlobalController.generate_response(
              HTTP_SUCCESS_CODE,
              SUCCESS_MESSAGE,
              user.dict(exclude={'password'}, by_alias=True)
            )

      raise Exception()

    except:
      return GlobalController.generate_response(HTTP_BAD_REQUEST_CODE, ERROR_MESSAGE)

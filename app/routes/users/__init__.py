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

@users_routes.route('/users/', methods = ['POST'])
def create():
  requiredParams = ['name', 'email', 'password']
  body = request.get_json()
  includesParams = GlobalController.includesAllRequiredParams(requiredParams, body)

  try:
    if includesParams:
      userExists = UserController.userAlreadyExists(body['email'], users)['exists']

      if userExists:
        raise Exception()

      body['password'] = UserController.encodePassword(body['password'])
      user = User(**body)
      users.insert_one(user.dict())

      return GlobalController.generateResponse(
        HTTP_CREATED_CODE,
        SUCCESS_MESSAGE,
        user.dict(exclude={'password'})
      )

    raise Exception()

  except:
    return GlobalController.generateResponse(HTTP_BAD_REQUEST_CODE, ERROR_MESSAGE)

@users_routes.route('/users/login', methods=['POST'])
def signin():
  requiredParams = ['email', 'password']
  body = request.get_json()
  includesParams = GlobalController.includesAllRequiredParams(requiredParams, body)

  try:
    if includesParams:
      userData = UserController.userAlreadyExists(body['email'], users)
      userExists = userData['exists']

      if userExists:
        user = User(**userData['data'])
        encodedPassword = body['password'].encode()
        savedPassword = user.password
        passwordIsCorrect = bcrypt.checkpw(encodedPassword, savedPassword)
        
        if passwordIsCorrect:
          return GlobalController.generateResponse(
            HTTP_SUCCESS_CODE,
            SUCCESS_MESSAGE,
            user.dict(exclude={'password'})
          )
          
    raise Exception()

  except:
    return GlobalController.generateResponse(HTTP_BAD_REQUEST_CODE, ERROR_MESSAGE)

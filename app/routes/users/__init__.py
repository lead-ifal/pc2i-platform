import json
import bcrypt
from flask import Blueprint

users_routes = Blueprint('users', __name__)

from flask import request
from app.models.user import User
from app.controllers.user_controller import UserController
from app.controllers.global_controller import GlobalController
from app.constants.status_code import HTTP_BAD_REQUEST_CODE, HTTP_CREATED_CODE, HTTP_SUCCESS_CODE
from datetime import datetime
from typing import Collection
from app import database

users: Collection = database.users

@users_routes.route('/user/new', methods = ['POST'])
def create():
  requiredParams = ['name', 'email', 'password']
  body = request.get_json()
  body['date_added'] = datetime.utcnow()

  includesParams = GlobalController.includesAllRequiredParams(requiredParams, body)

  if includesParams:
    user = UserController.userAlreadyExists(body['email'], users)

    if user['exists']:
      errorMessage = 'Já existe um usuário cadastrado com esse endereço de e-mail'
      return GlobalController.generateResponse(HTTP_BAD_REQUEST_CODE, errorMessage)

    body['password'] = UserController.encodePassword(body['password'])

    user = User(**body)
    userData = {
      'date_added': json.dumps(user.date_added, default=str),
      'email': user.email,
      'name': user.name
    }

    users.insert_one(user.dict())
    message = 'Usuário criado com sucesso'

    return GlobalController.generateResponse(HTTP_CREATED_CODE, message, userData)

  errorMessage = 'Os parâmetros "name", "email" e "password" são obrigatórios'
  return GlobalController.generateResponse(HTTP_BAD_REQUEST_CODE, errorMessage)

@users_routes.route('/user/login', methods=['POST'])
def signin():
  requiredParams = ['email', 'password']
  body = request.get_json()

  includesParams = GlobalController.includesAllRequiredParams(requiredParams, body)

  if includesParams:
    userData = UserController.userAlreadyExists(body['email'], users)
    userExists = userData['exists']

    if userExists:
      user = User(**userData['data'])
      encodedPassword = body['password'].encode()
      savedPassword = user.password
      passwordIsCorrect = bcrypt.checkpw(encodedPassword, savedPassword)
      
      if passwordIsCorrect:
        message = 'Autenticado com sucesso'
        data = {
          'email': user.email,
          'name': user.name,
          'date_added': json.dumps(user.date_added, default=str)
        }

        return GlobalController.generateResponse(HTTP_SUCCESS_CODE, message, data)
        
      errorMessage = 'A senha está incorreta'
      return GlobalController.generateResponse(HTTP_BAD_REQUEST_CODE, errorMessage)

    errorMessage = 'E-mail inválido'
    return GlobalController.generateResponse(HTTP_BAD_REQUEST_CODE, errorMessage)

  errorMessage = 'Os parâmetros "email" e "password" são obrigatórios'
  return GlobalController.generateResponse(HTTP_BAD_REQUEST_CODE, errorMessage)
import bcrypt
from flask import Blueprint

users_routes = Blueprint('users', __name__)

from flask import request
from app.models.user import User
from app.controllers.user_controller import UserController
from app.controllers.global_controller import GlobalController
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
      return GlobalController.generateResponse(400, errorMessage)

    body['password'] = UserController.encodePassword(body['password'])

    user = User(**body)
    userData = { 'date_added': user.date_added, 'email': user.email }

    users.insert_one(user.dict())
    message = 'Usuário criado com sucesso'

    return GlobalController.generateResponse(200, message, userData)

  errorMessage = 'Os parâmetros "name", "email" e "password" são obrigatórios'
  return GlobalController.generateResponse(400, errorMessage)

@users_routes.route('/user/login', methods=['POST'])
def signin():
  requiredParams = ['email', 'password']
  body = request.get_json()

  includesParams = GlobalController.includesAllRequiredParams(requiredParams, body)

  if includesParams:
    user = UserController.userAlreadyExists(body['email'], users)

    if user['exists']:
      encodedPassword = body['password'].encode()
      savedPassword = user['data']['password']
      passwordIsCorrect = bcrypt.checkpw(encodedPassword, savedPassword)
      
      if passwordIsCorrect:
        message = 'Autenticado com sucesso'
        data = {
          'email': user['data']['email'],
          'name': user['data']['name'],
          'date_added': user['data']['date_added']
        }

        return GlobalController.generateResponse(200, message, data)
        
      errorMessage = 'A senha está incorreta'
      return GlobalController.generateResponse(400, errorMessage)

    errorMessage = 'E-mail inválido'
    return GlobalController.generateResponse(400, errorMessage)

  errorMessage = 'Os parâmetros "email" e "password" são obrigatórios'
  return GlobalController.generateResponse(400, errorMessage)
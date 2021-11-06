from typing import Collection
import bcrypt

class UserController:
  def encodePassword(password: str):
    salt = bcrypt.gensalt()
    encodedPassword = password.encode('utf8')

    return bcrypt.hashpw(encodedPassword, salt)
  
  def userAlreadyExists(email: str, usersDatabase: Collection):
    userAlreadyExists = True

    savedUser = usersDatabase.find_one({ 'email': email })

    if savedUser is None:
      userAlreadyExists = False

    return { 'exists': userAlreadyExists, 'data': savedUser }
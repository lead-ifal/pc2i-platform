from typing import Collection
import bcrypt

class UserController:
  def encode_password(password: str):
    salt = bcrypt.gensalt()
    encoded_password = password.encode('utf8')

    return bcrypt.hashpw(encoded_password, salt)
  
  def user_already_exists(email: str, users_database: Collection):
    user_already_exists = True

    saved_user = users_database.find_one({ 'email': email })

    if saved_user is None:
      user_already_exists = False

    return { 'exists': user_already_exists, 'data': saved_user }

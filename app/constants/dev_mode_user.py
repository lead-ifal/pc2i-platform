from datetime import datetime
from hashlib import md5
from app.controllers.user_controller import UserController
from bson import ObjectId
import os

dev_mode_user =  {
  'encrypted_email':UserController.encode_email('devMode@test.com'),
  'validation': True,
  'token': ObjectId('637fb4e71cebba152fb0fb84'),
  'email': 'devMode@test.com',
  'name': 'Usuário do DevMode',
  'password':UserController.encode_password(os.getenv('DEV_MODE_USER_PASSWORD')),
  'date_added':  datetime.utcnow()
    }
  

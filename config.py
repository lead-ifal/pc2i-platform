import os

class Config:

    SECRET_KEY = os.urandom(32)

    # Recupera o diretório onde o script irá ser executado.
    basedir = os.path.abspath(os.path.dirname(__file__))

    # Ativa o modo debug.
    DEBUG = True

    # Connect to the database
    USER = "pc2idev"
    PASSWORD = ""
    HOST = "localhost"
    MONGO_DATABASE = 'pc2idev'
    MONGO_URI = "mongodb+srv://{}:{}@cluster0.vdufl.mongodb.net/{}?retryWrites=true&w=majority".format(USER,PASSWORD,MONGO_DATABASE)

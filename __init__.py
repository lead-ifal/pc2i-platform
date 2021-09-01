from datetime import datetime
from models.cultivation import Cultivation
import os
from pprint import pprint

from flask import Flask, request, url_for, jsonify
from flask_pymongo import PyMongo
from pymongo.collection import Collection, ReturnDocument
from pymongo.errors import DuplicateKeyError

from models.user import User
from models.objectid import PydanticObjectId

from config import Config


app = Flask(__name__)
app.config.from_object(Config)


pymongo = PyMongo(app)

users: Collection = pymongo.db.users
cultivations: Collection = pymongo.db.cultivations

@app.errorhandler(404)
def resource_not_found(e):
    """
    An error-handler to ensure that 404 errors are returned as JSON.
    """
    return jsonify(error=str(e)), 404


@app.route("/users/")
def list_users():
    """
    GET a list of users.
    The results are paginated using the `page` parameter.
    """

    page = int(request.args.get("page", 1))
    per_page = 10  # Valor constante.

    # Para paginação de resultados, é necessário ordená-los pelo nome,
    # e então pular o número de documentos das páginas anteriores que foram exibidos,
    # e então limitar o número ao tamanho de página fixo, ``per_page``.
    cursor = users.find().sort("name").skip(per_page * (page - 1)).limit(per_page)
    user_count = users.count_documents({})

    links = {
        "self": {"href": url_for(".list_users", page=page, _external=True)},
        "last": {
            "href": url_for(
                ".list_users", page=(user_count // per_page) + 1, _external=True
            )
        },
    }
    # Adiciona um link 'prev' se não estiver na primeira página:
    if page > 1:
        links["prev"] = {
            "href": url_for(".list_users", page=page - 1, _external=True)
        }
    # Adiciona um link 'next' se não estiver na última página:
    if page - 1 < user_count // per_page:
        links["next"] = {
            "href": url_for(".list_users", page=page + 1, _external=True)
        }

    return {
        "users": [User.from_mongo(doc).to_json() for doc in cursor],
        "_links": links,
    }


@app.route("/users/new", methods=["POST"])
def new_user():
    print(request)
    raw_user = request.get_json()
    raw_user["date_added"] = datetime.utcnow()

    user = User(**raw_user)
    insert_result = users.insert_one(user.to_bson())
    user.id = PydanticObjectId(str(insert_result.inserted_id))
    print(user)

    return user.to_json()

@app.route("/cultivations/new", methods=["POST"])
def new_cultivation():
    raw_cultivation = request.get_json()

    cultivation = Cultivation(**raw_cultivation)
    cultivations.insert_one(cultivation.to_bson())

    return cultivation.to_json()

app.run()
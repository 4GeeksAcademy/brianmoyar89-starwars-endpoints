"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from api.models import db, User, Character, Planets, Favorite
from api.utils import generate_sitemap, APIException

api = Blueprint('api', __name__)


@api.route('/hello', methods=['POST', 'GET'])
def handle_hello():

    response_body = {
        "message": "Hello! I'm a message that came from the backend, check the network tab on the google inspector and you will see the GET request"
    }

    return jsonify(response_body), 200

@api.route('/Character', methods=['GET'])
def get_character():
    character=Character.query.all()
    data=list(map(lambda person:person.serialize(), character))
    
    return jsonify(data), 200

@api.route('/Character/<int:character_id>', methods=['GET'])
def get_idcharacter(character_id):
    character=Character.query.filter_by(id=character_id).first()
    if character is None:
        return jsonify ({"msg": "no existe el personaje"})
    data=character.serialize()
    return jsonify(data), 200
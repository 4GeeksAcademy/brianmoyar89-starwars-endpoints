"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from api.models import db, User, Character, Planets, Favorite
from api.utils import generate_sitemap, APIException

api = Blueprint('api', __name__)

# Endpoint para listar todos los registros de people en la base de datos
@api.route('/people', methods=['GET'])
def get_people():
    people = Character.query.all()
    data = [person.serialize() for person in people]
    return jsonify(data), 200

# Endpoint para listar la información de una sola people por su ID
@api.route('/people/<int:people_id>', methods=['GET'])
def get_people_by_id(people_id):
    person = Character.query.get(people_id)
    if person is None:
        return jsonify({"msg": "No existe la persona"}), 404
    data = person.serialize()
    return jsonify(data), 200

# Endpoint para listar todos los registros de planets en la base de datos
@api.route('/planets', methods=['GET'])
def get_planets():
    planets = Planets.query.all()
    data = [planet.serialize() for planet in planets]
    return jsonify(data), 200

# Endpoint para listar la información de un solo planet por su ID
@api.route('/planets/<int:planet_id>', methods=['GET'])
def get_planet_by_id(planet_id):
    planet = Planets.query.get(planet_id)
    if planet is None:
        return jsonify({"msg": "No existe el planeta"}), 404
    data = planet.serialize()
    return jsonify(data), 200

# Endpoint para listar todos los usuarios del blog
@api.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    data = [user.serialize() for user in users]
    return jsonify(data), 200

# Endpoint para listar todos los favoritos del usuario actual
@api.route('/users/favorites', methods=['GET'])
def get_user_favorites():
    if not current_user:
        return jsonify({"msg": "Usuario no autenticado"}), 401

    favorites = current_user.favorite
    data = [favorite.serialize() for favorite in favorites]
    return jsonify(data), 200

# Endpoint para añadir un nuevo planet favorito al usuario actual
@api.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def add_favorite_planet(planet_id):
    if not current_user:
        return jsonify({"msg": "Usuario no autenticado"}), 401

    planet = Planets.query.get(planet_id)
    if planet is None:
        return jsonify({"msg": "No existe el planeta"}), 404

    # Verifica si el planeta ya está en los favoritos del usuario.
    existing_favorite = Favorite.query.filter_by(user_id=current_user.id, planets_id=planet.id).first()
    if existing_favorite:
        return jsonify({"msg": "El planeta ya está en tus favoritos"}), 400

    favorite = Favorite(user_id=current_user.id, planets_id=planet.id)
    db.session.add(favorite)
    db.session.commit()

    return jsonify({"msg": "Planeta agregado a tus favoritos"}), 201

# Endpoint para añadir una nueva people favorita al usuario actual
@api.route('/favorite/people/<int:people_id>', methods=['POST'])
def add_favorite_people(people_id):
    if not current_user:
        return jsonify({"msg": "Usuario no autenticado"}), 401

    person = Character.query.get(people_id)
    if person is None:
        return jsonify({"msg": "No existe la persona"}), 404

    # Verifica si la persona ya está en los favoritos del usuario.
    existing_favorite = Favorite.query.filter_by(user_id=current_user.id, character_id=person.id).first()
    if existing_favorite:
        return jsonify({"msg": "La persona ya está en tus favoritos"}), 400

    favorite = Favorite(user_id=current_user.id, character_id=person.id)
    db.session.add(favorite)
    db.session.commit()

    return jsonify({"msg": "Persona agregada a tus favoritos"}), 201

# Endpoint para eliminar un planet favorito del usuario actual por ID
@api.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def delete_favorite_planet(planet_id):
    if not current_user:
        return jsonify({"msg": "Usuario no autenticado"}), 401

    planet = Planets.query.get(planet_id)
    if planet is None:
        return jsonify({"msg": "No existe el planeta"}), 404

    favorite = Favorite.query.filter_by(user_id=current_user.id, planets_id=planet.id).first()
    if not favorite:
        return jsonify({"msg": "El planeta no está en tus favoritos"}), 404

    db.session.delete(favorite)
    db.session.commit()

    return jsonify({"msg": "Planeta eliminado de tus favoritos"}), 200

# Endpoint para eliminar una people favorita del usuario actual por ID
@api.route('/favorite/people/<int:people_id>', methods=['DELETE'])
def delete_favorite_people(people_id):
    if not current_user:
        return jsonify({"msg": "Usuario no autenticado"}), 401

    person = Character.query.get(people_id)
    if person is None:
        return jsonify({"msg": "No existe la persona"}), 404

    favorite = Favorite.query.filter_by(user_id=current_user.id, character_id=person.id).first()
    if not favorite:
        return jsonify({"msg": "La persona no está en tus favoritos"}), 404

    db.session.delete(favorite)
    db.session.commit()

    return jsonify({"msg": "Persona eliminada de tus favoritos"}), 200

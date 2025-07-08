"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Favorite, FavoriteType, Planet, Warrior, Spaceship
# from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace(
        "postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object


@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints


@app.route('/')
def sitemap():
    return generate_sitemap(app)


@app.route('/users', methods=['GET'])
def get_all_users():
    users = User.query.all()
    serialized_users = [user.serialize() for user in users]
    return jsonify(serialized_users), 200


@app.route('/planets', methods=['GET'])
def handle_get_planets():
    planets = Planet.query.all()
    planets = list(map(lambda p: p.serialize(), planets))
    return jsonify(planets)


@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_planet_by_id(planet_id):
    planet = Planet.query.get(planet_id)
    if not planet:
        return jsonify({"error": "Planeta no encontrado"}), 404

    return jsonify(planet.serialize()), 200


@app.route('/warriors', methods=['GET'])
def handle_get_warriors():
    warriors = Warrior.query.all()
    warriors = list(map(lambda p: p.serialize(), warriors))
    return jsonify(warriors)


@app.route('/warriors/<int:warrior_id>', methods=['GET'])
def get_warriors_by_id(warrior_id):
    warrior = Warrior.query.get(warrior_id)
    if not warrior:
        return jsonify({"error": "Warrior no encontrado"}), 404

    return jsonify(warrior.serialize()), 200


@app.route('/spaceships', methods=['GET'])
def handle_get_spaceships():
    spaceships = Spaceship.query.all()
    spaceships = list(map(lambda p: p.serialize(), spaceships))
    return jsonify(spaceships)


@app.route('/spaceships/<int:spaceship_id>', methods=['GET'])
def get_spaceship_by_id(spaceship_id):
    spaceship = Spaceship.query.get(spaceship_id)
    if not spaceship:
        return jsonify({"error": "Nave no encontrado"}), 404

    return jsonify(spaceship.serialize()), 200


@app.route('/favorites/<int:user_id>', methods=['GET'])
def handle_get_favourites(user_id):
    user_favorites = Favorite.query.filter_by(user_id=user_id).all()
    user_favorites = list(map(lambda fav: fav.serialize(), user_favorites))
    return jsonify(user_favorites), 200


@app.route('/warriors', methods=['POST'])
def handle_post_warrior():
    body = request.get_json()

    # Validación básica
    if not body.get("name") or not body.get("species") or not body.get("rank"):
        return jsonify({"msg": "Faltan datos obligatorios"}), 400

    new_warrior = Warrior(
        name=body["name"],
        species=body["species"],
        rank=body["rank"]
    )
    db.session.add(new_warrior)
    db.session.commit()

    return jsonify(new_warrior.serialize()), 201


@app.route('/planets', methods=['POST'])
def handle_post_planet():
    body = request.get_json()

    if not body.get("name"):
        return jsonify({"msg": "Falta el nombre del planeta"}), 400

    new_planet = Planet(
        name=body["name"],
        climate=body.get("climate"),
        population=body.get("population")
    )
    db.session.add(new_planet)
    db.session.commit()

    return jsonify(new_planet.serialize()), 201


@app.route('/spaceships', methods=['POST'])
def handle_post_spaceship():
    body = request.get_json()

    if not body.get("name"):
        return jsonify({"msg": "Falta el nombre de la nave"}), 400

    new_spaceship = Spaceship(
        name=body["name"],
        model=body.get("model"),
        manufacturer=body.get("manufacturer")
    )
    db.session.add(new_spaceship)
    db.session.commit()

    return jsonify(new_spaceship.serialize()), 201


@app.route('/favorites/<string:item_type>/<int:item_id>', methods=['POST'])
def handle_post_favorite(item_type, item_id):
    new_favorite = Favorite()
    new_favorite.user_id = 1
    if item_type == "warrior":
        new_favorite.type = FavoriteType.Warrior
        new_favorite.warrior_id = item_id
    elif item_type == "planet":
        new_favorite.type = FavoriteType.Planet
        new_favorite.planet_id = item_id
    elif item_type == "spaceship":
        new_favorite.type = FavoriteType.Spaceship
        new_favorite.spaceship_id = item_id
    else:
        return jsonify({"msg": "Tipo de favorito inválido"}), 404

    db.session.add(new_favorite)
    db.session.commit()

    return jsonify({"msg": "Favorito agregado", "favorite": new_favorite.serialize()}), 201


@app.route('/planets/<int:planet_id>', methods=['DELETE'])
def delete_planet(planet_id):
    planet = Planet.query.get(planet_id)
    if not planet:
        return jsonify({"error": "Planeta no encontrado"}), 404

    db.session.delete(planet)
    db.session.commit()
    return jsonify({"message": f"Planeta con id {planet_id} eliminado correctamente"}), 200


@app.route('/warriors/<int:warrior_id>', methods=['DELETE'])
def delete_warrior(warrior_id):
    warrior = Warrior.query.get(warrior_id)
    if not warrior:
        return jsonify({"error": "Guerrero no encontrado"}), 404

    db.session.delete(warrior)
    db.session.commit()
    return jsonify({"message": f"Guerrero con id {warrior_id} eliminado correctamente"}), 200


@app.route('/spaceships/<int:spaceship_id>', methods=['DELETE'])
def delete_spaceship(spaceship_id):
    spaceship = Spaceship.query.get(spaceship_id)
    if not spaceship:
        return jsonify({"error": "Nave no encontrada"}), 404

    db.session.delete(spaceship)
    db.session.commit()
    return jsonify({"message": f"Nave con id {spaceship_id} eliminada correctamente"}), 200


@app.route('/favorites/<int:favorite_id>', methods=['DELETE'])
def delete_favorite(favorite_id):
    favorite = Favorite.query.get(favorite_id)
    if not favorite:
        return jsonify({"error": "Favorito no encontrado"}), 404

    db.session.delete(favorite)
    db.session.commit()
    return jsonify({"message": f"Favorito con id {favorite_id} eliminado correctamente"}), 200


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)

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
from models import db, User, Character, Planet, Starship, Vehicle, Favorites
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


@app.route('/characters', methods=['GET'])
def get_all_character():

    characters = Character.query.all()
    characters_serialized = [character.serialize() for character in characters]

    if not characters:
        return jsonify({
            "msg": "Characters not exist yet"
        }), 404

    return jsonify({
        "msg": "Succefully showed",
        "character": characters_serialized
    }), 200


@app.route('/characters/<int:character_id>', methods=['GET'])
def get_character(character_id):

    character = Character.query.all(character_id)

    if not character:
        return jsonify({
            "msg": "Character dont found"
        }), 404

    return jsonify({
        "msg": "Character exist",
        "character": character.id()
    })

@app.route('/planets', methods=['GET'])
def get_all_planets():

    planets = Planet.query.all()
    planets_serialized = [planet.serialize() for planet in planets]

    if not planets:
        return jsonify({
            "msg": "planets not exist yet"
        }), 404

    return jsonify({
        "msg": "Succefully showed",
        "character": planets_serialized
    }), 200


@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_character(planet_id):

    planet = Planet.query.all(planet_id)

    if not planet:
        return jsonify({
            "msg": "Planet doesnt found"
        }), 404

    return jsonify({
        "msg": "Planet exist",
        "character": planet.id()
    })

@app.route('/starships', methods=['GET'])
def get_all_starship():

    starships = Starship.query.all()
    starship_serialized = [starship.serialize() for starship in starships]

    if not starships:
        return jsonify({
            "msg": "starships not exist yet"
        }), 404

    return jsonify({
        "msg": "Succefully showed",
        "character": starship_serialized
    }), 200


@app.route('/starships/<int:starships_id>', methods=['GET'])
def get_starship(starship_id):

    starship = Starship.query.all(starship_id)

    if not starship:
        return jsonify({
            "msg": "Starship doesnt found"
        }), 404

    return jsonify({
        "msg": "starship exist",
        "character": starship.id()
    })

@app.route('/vehicles', methods=['GET'])
def get_all_vehicle():

    vehicles = Vehicle.query.all()
    vehicle_serialized = [vehicle.serialize() for vehicle in vehicles]

    if not vehicles:
        return jsonify({
            "msg": "vehicles not exist yet"
        }), 404

    return jsonify({
        "msg": "Succefully showed",
        "character": vehicle_serialized
    }), 200


@app.route('/vehicles/<int:vehicle_id>', methods=['GET'])
def get_vehicle(vehicle_id):

    vehicle = Vehicle.query.all(vehicle_id)

    if not vehicle:
        return jsonify({
            "msg": "Vehicle doesnt found"
        }), 404

    return jsonify({
        "msg": "vehicle exist",
        "character": vehicle.id()
    })

@app.route('/users', methods=['GET'])
def get_all_user():
    users = User.query.all()
    user_serialized = [user.serialize() for user in users]

    return jsonify({
        "msg": "Users retrieved successfully",
        "users": user_serialized}), 200











# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)

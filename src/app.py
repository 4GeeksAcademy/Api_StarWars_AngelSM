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
    

    if not characters:
        return jsonify({
            "msg": "Characters not exist yet"
        }), 404
    
    characters_serialized = [character.serialize() for character in characters]
    
    return jsonify({
        "msg": "Succefully showed",
        "character": characters_serialized
    }), 200


@app.route('/characters/<int:character_id>', methods=['GET'])
def get_character(character_id):

    character = Character.query.get(character_id)

    if not character:
        return jsonify({
            "msg": "Character not found"
        }), 404

    return jsonify({
        "msg": "Character exist",
        "character": character.serialize()
    })


@app.route('/planets', methods=['GET'])
def get_all_planets():

    planets = Planet.query.all()
    
    if not planets:
        return jsonify({
            "msg": "planets not exist yet"
        }), 404
    
    planets_serialized = [planet.serialize() for planet in planets]
    
    return jsonify({
        "msg": "Succefully showed",
        "planets": planets_serialized
    }), 200


@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_planet(planet_id):

    planet = Planet.query.get(planet_id)

    if not planet:
        return jsonify({
            "msg": "Planet doesnt found"
        }), 404

    return jsonify({
        "msg": "Planet exist",
        "planet": planet.serialize()
    })



@app.route('/starships', methods=['GET'])
def get_all_starship():

    starships = Starship.query.all()
    
    if not starships:
        return jsonify({
            "msg": "starships not exist yet"
        }), 404

    starship_serialized = [starship.serialize() for starship in starships]

    return jsonify({
        "msg": "Succefully showed",
        "starships": starship_serialized
    }), 200


@app.route('/starships/<int:starships_id>', methods=['GET'])
def get_starship(starship_id):

    starship = Starship.query.get(starship_id)

    if not starship:
        return jsonify({
            "msg": "Starship doesnt found"
        }), 404

    return jsonify({
        "msg": "starship exist",
        "starship": starship.serialize()
    })


@app.route('/vehicles', methods=['GET'])
def get_all_vehicle():

    vehicles = Vehicle.query.all()
    

    if not vehicles:
        return jsonify({
            "msg": "vehicles not exist yet"
        }), 404
    
    vehicle_serialized = [vehicle.serialize() for vehicle in vehicles]

    return jsonify({
        "msg": "Succefully showed",
        "vehicles": vehicle_serialized
    }), 200


@app.route('/vehicles/<int:vehicle_id>', methods=['GET'])
def get_vehicle(vehicle_id):

    vehicle = Vehicle.query.get(vehicle_id)

    if not vehicle:
        return jsonify({
            "msg": "Vehicle doesnt found"
        }), 404

    return jsonify({
        "msg": "vehicle exist",
        "vehicle": vehicle.serialize()
    })


@app.route('/users', methods=['GET'])
def get_all_user():
    users = User.query.all()
    user_serialized = [user.serialize() for user in users]

    return jsonify({
        "msg": "Users retrieved successfully",
        "users": user_serialized}), 200


@app.route('/users', methods=['POST'])
def new_user():
    request_data = request.get_json()

    if not request_data.get("email") or not request_data.get("username"):
        return {
            "msg": "Missing requiered fields"
        }, 400

    NewUser = User(
        email=request_data.get("email"),
        id=request_data.get("id"),
        username=request_data.get("username")
    )

    db.session.add(NewUser)
    db.session.commit()

    return jsonify({
        "msg": "User created"
    }), 201


@app.route('/users/<int:user_id>/favorites', methods=['GET'])
def get_user_favorites(user_id):
    user = User.query.get(user_id)

    if not user:
        return jsonify({
           "msg": "User doesnt exist"
        }), 404
    favorites= user.favorites
    favorites_list = [fav.serialize() for fav in favorites]
    return jsonify({
        "msg": "this is ur favorites",
        "favorites": favorites_list
    }), 200

@app.route('/favorite/planets/<int:planet_id>', methods = ['POST'])
def add_favorites_planets(planet_id):
    user_id = 1
    user = User.query.get(user_id)
    planet = Planet.query.get(planet_id)

    if not user or not planet:
        return jsonify({"msg":"User or planet not found"}), 404
    
    new_favorite_planet = Favorites(user_id=user.id, planet_id=planet.id)
    db.session.add(new_favorite_planet)
    db.session.commit()

    return jsonify({"msg": "Planet added to favorites"}), 201

@app.route('/favorite/planets/<int:planet_id>', methods=['DELETE'])
def delete_favorite_planet(planet_id):
    user_id = 1
    favorite = Favorites.query.filter_by(user_id=user_id, planet_id=planet_id).first()

    if not favorite:
        return jsonify({"msg": "Favorite planet not found"}), 404

    db.session.delete(favorite)
    db.session.commit()

    return jsonify({"msg": "Planet removed"}), 200

@app.route('/favorite/characters/<int:character_id>', methods = ['POST'])
def add_favorite_character (character_id):
    user_id = 1
    user = User.query.get(user_id)
    character = Character.query.get(character_id)

    if not user or not character:
        return jsonify({"msg":"User or character not found"}),404
    
    new_favorite_character = Favorites(user_id = user.id, character_id = character.id)
    db.session.add(new_favorite_character)
    db.session.commit()

    return jsonify({
        "msg":"Character added to favorite"
    }), 200
@app.route('/favorite/characters/<int:character_id>', methods = ['DELETE'])
def delete_favorite_character (character_id):
    user_id = 1
    favorite = Favorites.query.filter_by(user_id=user_id, character_id=character_id).first()
    db.session.delete(favorite)
    db.session.commit()

    return jsonify({
        "msg": "Cahracter removed"
    }), 200
@app.route('/favorite/starship/<int:starship_id>', methods = ['POST'])
def add_favorite_starship (starship_id):
    user_id = 1
    user = User.query.get(user_id)
    starship = Starship.query.get(starship_id)

    if not user or not starship:
        return jsonify({"msg":"User or starship not found"}),404
    
    new_favorite_starship = Favorites(user_id = user.id, starship_id = starship.id)
    db.session.add(new_favorite_starship)
    db.session.commit()

    return jsonify({
        "msg":"Starship added to favorite"
    }), 200
@app.route('/favorite/starship/<int:starship_id>', methods = ['DELETE'])
def delete_favorite_starship (starship_id):
    user_id = 1
    favorite = Favorites.query.filter_by(user_id = user_id, starship_id = starship_id).first()
    db.session.delete(favorite)
    db.session.commit ()

@app.route('/favorite/vehicles/<int:vehicle_id>', methods = ['POST'])
def add_fav_vehicle(vehicle_id):
    user_id = 1 
    user = User.query.get(user_id)
    vehicle= Vehicle.query.get(vehicle_id)

    if not user or not vehicle:
        return jsonify({"msg":"User or vehicle not found"}),404
    
    new_favorite_vehicle = Favorites(user_id= user.id, vehicle_id= vehicle.id)
    db.session.add(new_favorite_vehicle)
    db.session.commit()

    return jsonify({'msg':'Vehicle added to favorite'}), 200
@app.route('/favorite/vehicles/<int:vehicle_id>', methods = ['DELETE'])
def delete_fav_vehicle(vehicle_id):
    user_id=1
    favorite = Favorites.query.filter_by(user_id = user_id, vehicle_id = vehicle_id).first()
    db.session.delete(favorite)
    db.session.commit()
    


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)

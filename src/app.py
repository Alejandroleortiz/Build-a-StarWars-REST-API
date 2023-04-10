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
from models import db, User, Planet, Character

#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
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
@app.route('/') #GET
def sitemap():
    return generate_sitemap(app)

@app.route('/characters', methods=['GET'])
def getCharacters(): # Obtener personajes
    characters = Character.query.all()
    characters = list(map(lambda character: character.serialize(), characters))
    return jsonify(characters), 200 

    data = {
        "msg": "Hello, this is your GET /characters response "
    }
    return jsonify(data), 200 

@app.route('/characters/<int:character_id>', methods=['GET'])
def getCharacter(character_id): # Obtener personaje por id

    data = {
        "msg": "Hello, this is your GET /one character response "
    }
    return jsonify({"Character": f'{character_id}'}), 200 

@app.route('/planets', methods=['GET'])
def get_all_planets(): # Obtener planetas
    planets = Planet.query.all()
    planets = list(map(lambda planet: planet.serialize(), planets))
    return jsonify(planets), 200 

@app.route('/planets/<int:planet_id>', methods=['GET'])
def getPlanet(planet_id): #Obtener Planeta por id
    
    data = {
        "msg": "Hello, this is your GET /one planet response "
    }
    return jsonify({"Planet": f'{planet_id}'}), 200 

@app.route('/users', methods=['GET']) #Obtener usuarios
def get_all_users():
    users = User.query.all()
    users = list(map(lambda user: user.serialize(), users))
    return jsonify(users), 200 

@app.route('/users', methods=['POST']) #crear usuarios
def create_user():
    datos = request.get_json()

    user = User()
    user.email = datos ['email']
    user.password = datos ['password']
    user.is_active = datos['is_active']
    user.suscription_date = False
    characters = False
    planets = False
    
    db.session.add(user)
    db.session.commit()

    return jsonify(user.serialize()), 201


@app.route('/user/favorites', methods=['GET'])
def getFavorites(): #Acceder a favoritos

    data = {
        "msg": "Hello, this is your GET /favorites user response "
    }
    return jsonify(data), 200

@app.route('/favorites/planet/<int:planet_id>', methods=['POST'])
def addPlanet(planet_id): #Agregar planeta
    data = {
        "msg": "Hello, this is your POST /Add favorites planet response "
    }
    return jsonify(data), 201

@app.route('/favorites/character/<int:character_id>', methods=['POST'])
def addCharacter(character_id): #Agregar personaje
    data = {
        "msg": "Hello, this is your POST /Add favorites character response "
    }
    return jsonify(data), 201


@app.route('/favorites/planet/<int:planet_id>', methods=['DELETE'])
def deletePlanet(planet_id): #Borrar planeta
    data = {
        "msg": "Hello, this is your POST /Add favorites character response "
    }
    return jsonify(data), 201

@app.route('/favorites/character/<int:character_id>', methods=['DELETE'])
def deleteCharacter(character_id): # Borrar personaje
    data = {
        "msg": "Hello, this is your POST /Add favorites character response "
    }
    return jsonify(data), 201


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)

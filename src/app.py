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
from models import db, User
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

    data = {
        "msg": "Hello, this is your GET /characters response "
    }
    return jsonify(data), 200 

@app.route('/characters/<character_id>', methods=['GET'])
def getCharacter(character_id): # Obtener personaje por id

    data = {
        "msg": "Hello, this is your GET /one character response "
    }
    return jsonify({"Character": f'{character_id}'}), 200 

@app.route('/planets', methods=['GET'])
def getPlanets(): # Obtener planetas

    data = {
        "msg": "Hello, this is your GET /planets response "
    }
    return jsonify(data), 200 

@app.route('/planets/<planet_id>', methods=['GET'])
def getPlanet(planet_id): #Planeta por id

    data = {
        "msg": "Hello, this is your GET /one planet response "
    }
    return jsonify({"Planet": f'{planet_id}'}), 200 

@app.route('/user', methods=['GET'])
def getUser():

    data = {
        "msg": "Hello, this is your GET /user response "
    }
    return jsonify(data), 200 

@app.route('/user/favorites', methods=['GET'])
def getFavorites():

    data = {
        "msg": "Hello, this is your GET /favorites user response "
    }
    return jsonify(data), 200

@app.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def addPlanet():
    data = {
        "msg": "Hello, this is your POST /Add favorites planet response "
    }
    return jsonify(data), 201

@app.route('/favorite/character/<int:character_id>', methods=['POST'])
def addCharacter():
    data = {
        "msg": "Hello, this is your POST /Add favorites character response "
    }
    return jsonify(data), 201


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)

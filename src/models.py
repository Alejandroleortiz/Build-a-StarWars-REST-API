from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), default=True)
    suscription_date = db.Column(db.String, nullable=False)
    characters = db.relationship('Character', secondary="favorite_character", backref="user")
    planets = db.relationship('Planet', secondary="favorite_planet", backref="user")

def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "is_active":self.is_active,
            "suscription_date":self.suscription_date,
            "characters":self.characters,
            "planets":self.planets,
            # do not serialize the password, its a security breach
        }

class Character(db.Model):
    __tablename__ = 'character'

    uid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    description = db.Column(db.String(200), nullable=False)

class Planet(db.Model):
    __tablename__ = 'planet'

    uid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    description = db.Column(db.String(200), nullable=False)

class Favorite_character(db.Model):
    __tablename__ = 'favorite_character'

    character_id = db.Column(db.Integer, db.ForeignKey('character.uid'), primary_key=True)
    user_id=db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    

class Favorite_planet(db.Model):
    __tablename__ = 'favorite_planet'

    planet_id = db.Column(db.Integer, db.ForeignKey('planet.uid'), primary_key=True)
    user_id=db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    
    # def __repr__(self):
    #     return '<User %r>' % self.email

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.commit()

    def delete(self):
        db.session.add(self)
        db.session.commit()

    
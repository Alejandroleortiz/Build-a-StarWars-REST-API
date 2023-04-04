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
    character_id = db.relationship(foreign_keys="[character.user_id]", backref="character_id")
    planet_id = db.relationship(foreign_keys="[planet.user_id]", backref="planet_id")

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

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    character_id = db.Column(db.Integer, db.ForeignKey('character.uid'), primary_key=True)
    user = db.relationship('User')
    character = db.relationship('Character', backref="character")

class Favorite_planet(db.Model):
    __tablename__ = 'favorite_planet'

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    planet_id = db.Column(db.Integer, db.ForeignKey('planet.uid'), primary_key=True)
    user = db.relationship('User')
    planet = db.relationship('Planet', backref="planet")
    
    # def __repr__(self):
    #     return '<User %r>' % self.username

    def save(self):
        db.session.add(self)
        db.session.commit()

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }
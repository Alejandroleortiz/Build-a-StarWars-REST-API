from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), default=True)
    suscription_date = db.Column(String, nullable=False)

class Character(Base):
    __tablename__ = 'character'

    uid = db.Column(Integer, primary_key=True)
    name = db.Column(String(150), nullable=False)
    description = db.Column(String(200), nullable=False)

class Planet(Base):
    __tablename__ = 'planet'

    uid = db.Column(Integer, primary_key=True)
    name = db.Column(String(150), nullable=False)
    description = db.Column(String(200), nullable=False)

class Favorite_character(Base):
    __tablename__ = 'favorite_character'

    user_id = db.Column(Integer, ForeignKey('user.id'))
    character_id = db.Column(Integer, ForeignKey('character.uid'), primary_key=True)
    user = db.relationship('User', backref="user")
    character = db.relationship('Character', backref="character")

class Favorite_planet(Base):
    __tablename__ = 'favorite_planet'

    user_id = db.Column(Integer, ForeignKey('user.id'))
    planet_id = db.Column(Integer, ForeignKey('planet.uid'), primary_key=True)
    user = db.relationship('User', backref="user")
    planet = db.relationship('Planet', backref="planet")
    
    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }
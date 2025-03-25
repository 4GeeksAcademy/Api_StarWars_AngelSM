from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Integer, BigInteger, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()


class User(db.Model):

    __tablename__= 'user'
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(
        String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    firstname: Mapped[str] = mapped_column(String(50), nullable=True)
    lastname: Mapped[str] = mapped_column(String(100), nullable=True)
    username: Mapped[str] = mapped_column(String(15), nullable=False)

    favorites = relationship("Favorites", back_populates="user")

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "username": self.username
        }


class Character(db.Model):

    __tablename__ = 'character'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    skin_color: Mapped[str] = mapped_column(String(50), nullable=False)
    gender: Mapped[str] = mapped_column(String(50), nullable=False)
    History: Mapped[str] = mapped_column(String(500), nullable=False)
    Height: Mapped[float] = mapped_column(nullable=False)

    
    favorites = relationship("Favorites", back_populates="character")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "skin": self.skin_color,
            "gender": self.gender,
            "History": self.History,
            "Height": self.Height
        }


class Planet(db.Model):

    __tablename__= 'planet'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    History: Mapped[str] = mapped_column(String(500), nullable=False)
    gravity: Mapped[str] = mapped_column(String(100), nullable=False)
    diameter: Mapped[int] = mapped_column(nullable=False)
    climate: Mapped[str] = mapped_column(String(255), nullable=False)
    population: Mapped[int] = mapped_column(BigInteger, nullable=False)

    
    favorites = relationship("Favorites", back_populates="planet")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "History": self.History,
            "gravity": self.gravity,
            "Size": self.diameter,
            "population": self.population,
            "climate": self.climate
        }


class Starship(db.Model):

    __tablename__ = 'starship' 
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    model: Mapped[str] = mapped_column(String(255), nullable=False)
    cargo_capacity: Mapped[int] = mapped_column(BigInteger, nullable=False)
    length: Mapped[float] = mapped_column(Float(10, 2), nullable=False)

    
    favorites = relationship("Favorites", back_populates="starship")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "model": self.model,
            "capacity": self.cargo_capacity,
            "length": self.length
        }


class Vehicle(db.Model):

    __tablename__ = 'vehicle'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    model: Mapped[str] = mapped_column(String(255), nullable=False)
    cargo_capacity: Mapped[int] = mapped_column(BigInteger, nullable=False)
    length: Mapped[float] = mapped_column(Float(10, 2), nullable=False)


    favorites = relationship("Favorites", back_populates="vehicle")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "model": self.model,
            "capacity": self.cargo_capacity,
            "length": self.length
        }


class Favorites(db.Model):
    __tablename__ = 'favorites'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(db.ForeignKey('user.id'), nullable=False)
    planet_id: Mapped[int] = mapped_column(db.ForeignKey('planet.id'), nullable=True)
    starship_id: Mapped[int] = mapped_column(db.ForeignKey('starship.id'), nullable=True)
    vehicle_id: Mapped[int] = mapped_column(db.ForeignKey('vehicle.id'), nullable=True)
    character_id: Mapped[int] = mapped_column(db.ForeignKey('character.id'), nullable=True)

   
    user = relationship("User", back_populates="favorites")
    planet = relationship("Planet", back_populates="favorites")
    starship = relationship("Starship", back_populates="favorites")
    vehicle = relationship("Vehicle", back_populates="favorites")
    character = relationship("Character", back_populates="favorites")

    def serialize(self):
        return {
            "id": self.id,
            "user": self.user_id,
            "planet": self.planet_id,
            "starship": self.starship_id,
            "vehicle": self.vehicle_id,
            "character": self.character_id
        }
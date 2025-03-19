from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Integer, BigInteger, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()


class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(
        String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    firstname: Mapped[str] = mapped_column(String(50), nullable=False)
    lastname: Mapped[str] = mapped_column(String(100), nullable=False)
    username: Mapped[str] = mapped_column(String(15), nullable=False)

    favs = relationship("Favorites", back_populates="User")

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "username": self.username
        }


class Character(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    skin_color: Mapped[str] = mapped_column(String(50), nullable=False)
    gender: Mapped[str] = mapped_column(String(50), nullable=False)
    History: Mapped[str] = mapped_column(String(500), nullable=False)
    Height: Mapped[float] = mapped_column(nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "skin": self.skin_color,
            "gender": self.gender,
            "History": self.History,
            "Height":self.Height
        }


class Planet(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    History: Mapped[str] = mapped_column(String(500), nullable=False)
    gravity: Mapped[str] = mapped_column(String(100), nullable=False)
    diameter: Mapped[int] = mapped_column(nullable=False)
    climate: Mapped[str] = mapped_column(String(255), nullable=False)
    population: Mapped[int] = mapped_column(BigInteger, nullable=False)

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
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    model: Mapped[str] = mapped_column(String(255), nullable=False)
    cargo_capacity: Mapped[int] = mapped_column(BigInteger, nullable=False)
    length: Mapped[float] = mapped_column(Float(10, 2), nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "model": self.model,
            "capacity": self.cargo_capacity,
            "length": self.length
        }


class Vehicle(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    model: Mapped[str] = mapped_column(String(255), nullable=False)
    cargo_capacity: Mapped[int] = mapped_column(BigInteger, nullable=False)
    length: Mapped[float] = mapped_column(Float(10, 2), nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "model": self.model,
            "capacity": self.cargo_capacity,
            "length": self.length
        }


class Favorites(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(db.ForeignKey('users.id'), nullable=False)
    planet_id: Mapped[int] = mapped_column(db.ForeignKey('planets.id'), nullable=True)
    starship_id: Mapped[int] = mapped_column(db.ForeignKey('starships.id'), nullable=True)
    vehicle_id: Mapped[int] = mapped_column(db.ForeignKey('vehicles.id'), nullable=True)
    Character_id:Mapped[int] = mapped_column(db.ForeignKey('character.id'), nullable=True)

    user = relationship("User", back_populates="favorites")
    planet = relationship("Planet", back_populates="favorites")
    starship = relationship("Starship", back_populates="favorites")
    vehicle = relationship("Vehicle", back_populates="favorites")
    character = relationship("Character", back_populates = "favorites")
import enum
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, Integer, ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional, List

db = SQLAlchemy()


class FavoriteType(enum.Enum):
    Planet = 1
    Warrior = 2
    Spaceship = 3


class User(db.Model):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(
        String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)

    # Relación reversa
    favorites: Mapped[List["Favorite"]] = relationship(
        "Favorite", back_populates="user")

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "favorite": [fav.serialize() for fav in self.favorites]
        }


class Planet(db.Model):
    __tablename__ = "planet"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    climate: Mapped[str] = mapped_column(String(80), nullable=True)
    population: Mapped[int] = mapped_column(Integer, nullable=True)

    favorites: Mapped[List["Favorite"]] = relationship(
        "Favorite", back_populates="planet")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "climate": self.climate,
            "population": self.population

        }


class Spaceship(db.Model):
    __tablename__ = "spaceship"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    model: Mapped[str] = mapped_column(String(80), nullable=True)
    manufacturer: Mapped[str] = mapped_column(String(80), nullable=True)

    favorites: Mapped[List["Favorite"]] = relationship(
        "Favorite", back_populates="spaceship")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "model": self.model,
            "manufacturer": self.manufacturer
        }


class Warrior(db.Model):
    __tablename__ = "warrior"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    species: Mapped[str] = mapped_column(String(80), nullable=True)
    rank: Mapped[str] = mapped_column(String(80), nullable=True)

    favorites: Mapped[List["Favorite"]] = relationship(
        "Favorite", back_populates="warrior")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "species": self.species,
            "rank": self.rank
        }


class Favorite(db.Model):
    __tablename__ = "favorite"

    id: Mapped[int] = mapped_column(primary_key=True)
    type: Mapped[FavoriteType] = mapped_column(Enum(FavoriteType))
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    planet_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("planet.id"), nullable=True)
    spaceship_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("spaceship.id"), nullable=True)
    warrior_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("warrior.id"), nullable=True)

    # Relaciones reversas
    user: Mapped[User] = relationship("User", back_populates="favorites")
    planet: Mapped[Planet] = relationship(
        "Planet", back_populates="favorites")
    spaceship: Mapped[Spaceship] = relationship(
        "Spaceship", back_populates="favorites")
    warrior: Mapped[Warrior] = relationship(
        "Warrior", back_populates="favorites")

    def serialize(self):
        favorite_item = None

        data = {
            "id": self.id,
            "type": self.type.name,

        }

        if self.planet:
            data["planet"] = self.planet.serialize()
        if self.spaceship:
            data["spaceship"] = self.spaceship.serialize()
        if self.warrior:
            data["warrior"] = self.warrior.serialize()

        return data

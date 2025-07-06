from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, Integer
from sqlalchemy.orm import Mapped, mapped_column

db = SQLAlchemy()


class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(
        String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }

    class Planet (db.Model):  # Representa la tabla planet en mi base de datos

        __tablename__ = "planet"

        id: Mapped[int] = mapped_column(primary_key=True)
        name: Mapped[str] = mapped_column(
            String(120), unique=True, nullable=False)
        climate: Mapped[str] = mapped_column(String(80), nullable=True)
        population: Mapped[int] = mapped_column(Integer, nullable=True)

        def serialize(self):
            return {
                "id": self.id,
                "name": self.name,
                "climate": self.climate,
                "population": self.population
            }

        class Spaceship (db.Model):

            __tablename__ = "spaceship"

            id: Mapped[int] = mapped_column(primary_key=True)
            name: Mapped[str] = mapped_column(
                String(120), unique=True, nullable=False)
            model: Mapped[str] = mapped_column(String(80), nullable=True)
            manufacturer: Mapped[int] = mapped_column(
                String(80), nullable=True)

            def serialize(self):
                return {
                    "id": self.id,
                    "name": self.name,
                    "model": self.model,
                    "manufacturer": self.manufacturer
                }

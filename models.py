from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    UniqueConstraint,
)

db = SQLAlchemy()


class Client(db.Model):  # type: ignore[name-defined]
    __tablename__ = "client"
    id = Column(Integer, nullable=False, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    surname = Column(String(50), nullable=False)
    credit_card = Column(String(50))
    car_number = Column(String(10))


class Parking(db.Model):  # type: ignore[name-defined]
    __tablename__ = "parking"
    id = Column(Integer, nullable=False, primary_key=True, index=True)
    address = Column(String(100), nullable=False)
    opened = Column(Boolean)
    count_places = Column(Integer, nullable=False)
    count_available_places = Column(Integer, nullable=False)


class ClientParking(db.Model):  # type: ignore[name-defined]
    __tablename__ = "client_parking"
    id = Column(Integer, nullable=False, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("client.id"))
    parking_id = Column(Integer, ForeignKey("parking.id"))
    time_in = Column(DateTime)
    time_out = Column(DateTime)
    __table_args__ = (
        UniqueConstraint(
            "client_id",
            "parking_id",
            name="unique_client_parking"
        ),
    )

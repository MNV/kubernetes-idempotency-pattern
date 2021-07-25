import enum

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import DateTime, Enum
from sqlalchemy.sql import func

db = SQLAlchemy()


class OrderModel(db.Model):
    __tablename__ = "order"

    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String(30))
    price = db.Column(db.Integer())
    created_at = db.Column(DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(DateTime(timezone=True), onupdate=func.now())

    def __init__(self, number, price):
        self.number = number
        self.price = price

    def __repr__(self):

        return f"{self.number} ({self.price})"

    def create(self):
        db.session.add(self)
        db.session.commit()

        return self

from flask_sqlalchemy import SQLAlchemy
from marshmallow import fields
from marshmallow_sqlalchemy import ModelSchema

from src.models import OrderModel

db = SQLAlchemy()


class OrderSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = OrderModel
        sqla_session = db.session

    number = fields.String(required=True)
    price = fields.String(required=True)

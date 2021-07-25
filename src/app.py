import os
from hashlib import md5

from flask import Flask, jsonify, request, make_response
from flask import json
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func

from src.config import Config
from src.models import OrderModel
from src.schemas import OrderSchema

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)


@app.errorhandler(Exception)
def handle_exception(e):
    response = e.get_response()
    response.data = json.dumps(
        {
            "code": e.code,
            "message": e.description,
        }
    )
    response.content_type = "application/json"

    return response


def generate_etag(data):
    if data:
        return md5(str(data).encode()).hexdigest()


@app.route("/health")
def health():
    return jsonify({"status": "OK"})


@app.route("/")
def index():
    return f"Hello from {os.environ['HOSTNAME']}!"


@app.route("/orders", methods=["GET"])
def get_orders():
    schema = OrderSchema()
    orders = []
    for order in db.session.query(OrderModel).all():
        orders.append(schema.dump(order))

    return make_response(jsonify(orders))


@app.route("/order", methods=["POST"])
def create():
    max_order_id = db.session.query(func.max(OrderModel.id)).scalar()
    current_version = generate_etag(max_order_id)
    if not current_version or not request.if_match or current_version in request.if_match:
        data = request.get_json()
        schema = OrderSchema()
        order: OrderModel = schema.load(data)
        result = schema.dump(order.create())

        max_order_id = db.session.query(func.max(OrderModel.id)).scalar()

        response = make_response(jsonify(result), 200)
        response.set_etag(generate_etag(max_order_id))

        return response

    return make_response(
        {
            "error": {"code": "order_exists", "message": "Order exists."}
        }, 409
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="80")

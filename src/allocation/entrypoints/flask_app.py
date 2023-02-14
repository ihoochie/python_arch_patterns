from datetime import date

from flask import Flask, jsonify, request
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.allocation import config
from src.allocation.domain import model
from src.allocation.adapters import orm, repository
from src.allocation.service_layer import services, unit_of_work

orm.start_mappers()
get_session = sessionmaker(bind=create_engine(config.get_postgres_uri()))

app = Flask(__name__)


@app.route("/allocate", methods=["POST"])
def allocate_endpoint():
    uow = unit_of_work.SqlAlchemyUnitOfWork()

    try:
        batchref = services.allocate(
            request.json["orderid"], request.json["sku"], request.json["qty"], uow
        )
    except (model.OutOfStock, services.InvalidSku) as e:
        return jsonify({"message": str(e)}), 400

    return jsonify({"batchref": batchref}), 201


@app.route("/add_batch", methods=["POST"])
def add_batch():
    uow = unit_of_work.SqlAlchemyUnitOfWork()
    eta = request.json.get("eta")

    if eta is not None:
        eta = date.fromisoformat(eta)

    services.add_batch(
        request.json["ref"], request.json["sku"], request.json["qty"], eta, uow
    )
    return "OK", 201

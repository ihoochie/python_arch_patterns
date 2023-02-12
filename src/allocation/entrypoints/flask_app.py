from datetime import date

from flask import Flask, jsonify, request
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.allocation import config
from src.allocation.domain import model
from src.allocation.adapters import orm, repository
from src.allocation.service_layer import services

orm.start_mappers()
get_session = sessionmaker(bind=create_engine(config.get_postgres_uri()))

app = Flask(__name__)


def is_valid_sku(sku, batches):
    return sku in {b.sku for b in batches}


@app.route("/allocate", methods=["POST"])
def allocate_endpoint():
    session = get_session()
    repo = repository.SqlAlchemyRepository(session)

    try:
        batchref = services.allocate(
            request.json["orderid"], request.json["sku"], request.json["qty"], repo, session
        )
    except (model.OutOfStock, services.InvalidSku) as e:
        return jsonify({"message": str(e)}), 400

    return jsonify({"batchref": batchref}), 201


@app.route("/add_batch", methods=["POST"])
def add_batch():
    session = get_session()
    repo = repository.SqlAlchemyRepository(session)
    eta = request.json.get("eta")

    if eta is not None:
        eta = date.fromisoformat(eta)

    services.add_batch(
        request.json["ref"], request.json["sku"], request.json["qty"], eta, repo, session
    )
    return "OK", 201

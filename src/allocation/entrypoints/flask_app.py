from datetime import date

from flask import Flask, request
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.allocation import config
from src.allocation.domain import events
from src.allocation.adapters import orm
from src.allocation.service_layer import handlers, unit_of_work, messagebus

orm.start_mappers()
get_session = sessionmaker(bind=create_engine(config.get_postgres_uri()))

app = Flask(__name__)


@app.route("/allocate", methods=["POST"])
def allocate_endpoint():
    try:
        event = events.AllocationRequired(
            request.json["orderid"], request.json["sku"], request.json["qty"]
        )
        results = messagebus.handle(event, unit_of_work.SqlAlchemyUnitOfWork())
        batchref = results.pop(0)
    except handlers.InvalidSku as e:
        return {"message": str(e)}, 400

    return {"batchref": batchref}, 201


@app.route("/add_batch", methods=["POST"])
def add_batch():
    eta = request.json.get("eta")

    if eta is not None:
        eta = date.fromisoformat(eta)

    handlers.add_batch(
        events.BatchCreated(request.json["ref"], request.json["sku"], request.json["qty"], eta),
        unit_of_work.SqlAlchemyUnitOfWork()
    )
    return "OK", 201

import json
from dataclasses import asdict
import logging

import redis

from src.allocation import config
from src.allocation.domain import events


logger = logging.getLogger(__name__)

r = redis.Redis(**config.get_redis_host_and_port())


def publish(channel, event: events.Event):
    logger.debug("publishing : channel=%s, event=%s", channel, event)
    r.publish(channel, json.dumps(asdict(event)))

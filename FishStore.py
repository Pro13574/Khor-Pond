import pickle
import time
from dataclasses import dataclass
from typing import Dict, List, Union

import redis

from Fish import Fish
from FishData import FishData
from logging_utils import get_logger


def current_milli_time():
    return round(time.time() * 1000)


@dataclass
class ExampleObject:
    name: str
    unit_price: float
    quantity_on_hand: int = 0


log = get_logger("redis")


def connect_to_redis(host="localhost", port=6379, password=None, retries=5, retry_interval=1, db=0) -> redis.StrictRedis | None:
    for i in range(retries):
        try:
            r = redis.StrictRedis(host=host,
                                  port=port,
                                  password=password,
                                  db=db)
            if r.ping():
                log.info(f"connected to Redis at {host}:{port}")
                return r
            else:
                raise redis.ConnectionError()

        except redis.ConnectionError:
            if i < retries - 1:
                log.warning(
                    f"failed to connect to Redis at {host}:{port}, retrying in {retry_interval} second")
                time.sleep(retry_interval)
            else:
                log.error(
                    f"failed to connect to Redis at {host}:{port}, after {retries} attempts")
                return None


class FishStore:
    def __init__(self, redis):
        self.redis: redis.StrictRedis = redis

    def add_fish(self, fish: FishData):
        self.redis.set(fish.getId(), pickle.dumps(fish))
        # , ex=fish.getLifetime()

    # def remove_fish(self, fish_ids: List[str]):
    #     self.redis.delete(*fish_ids)

    def remove_fish(self, fish_id: str):
        self.redis.delete(fish_id)

    # TODO: need to compare performance later
    def remove_batch(self, fish_ids: List[str]):
        pipe = self.redis.pipeline(transaction=False)
        for key in fish_ids:
            pipe.delete(key)

    def get_fishes(self) -> Dict[str, Fish]:
        fish_ids = self.redis.keys()
        fishes_data = [
            pickle.loads(data) for data in self.redis.mget(fish_ids) if data is not None
        ]
        fishes = [Fish(data=fish) for fish in fishes_data]
        return dict(zip(fish_ids, fishes))

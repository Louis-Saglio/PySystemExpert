import random
from typing import Hashable, Iterable, Tuple, Set

from core_lib import Engine
from data_lib import DataManager
from settings import DATA_BASE_FILE, INSTANCE_ID_CHARS_POOL, INSTANCE_ID_LENGTH

Fact_tuple = Tuple[str, Hashable, bool]


class SystemExpert:

    # todo : data verification

    def __init__(self):
        self.engine = Engine(set(), set())
        self.data_manager = DataManager(DATA_BASE_FILE)

    def _get_instance_id(self):
        return random.sample(INSTANCE_ID_CHARS_POOL, INSTANCE_ID_LENGTH)

    def create_instance(self) -> str:
        instance_id = self._get_instance_id()
        self.data_manager.create_instance(instance_id)
        return instance_id

    def add_fact(self, uuid: str, name: str, value: Hashable, state: bool):
        pass

    def add_rule(self, uuid: str, majors: Iterable[Fact_tuple], conclusions: Iterable[Fact_tuple]):
        pass

    def process(self, uuid: str):
        pass

    def get_facts(self, uuid: str) -> Set[Fact_tuple]:
        pass

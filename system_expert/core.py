from random import choice
from typing import Hashable, Iterable, Tuple, Set

from core_lib import Engine
from data_lib import DataManager
from settings import DATA_BASE_FILE, USER_UUID_CHARS_POOL, USER_UUID_LENGTH

Fact_tuple = Tuple[str, Hashable, bool]


class SystemExpert:

    # todo : data verification

    def __init__(self):
        self.engine = Engine(set(), set())
        self.data_manager = DataManager(DATA_BASE_FILE)  # todo : check database integrity

    def _get_user_id(self):
        used_uuids = self.data_manager.get_used_user_uuids()
        for _ in range(1000):
            uuid = ''.join(choice(USER_UUID_CHARS_POOL) for _ in range(USER_UUID_LENGTH))
            if uuid not in used_uuids:
                return uuid
        else:
            raise UserWarning(
                f"Not enough user_uuid {len(used_uuids)}. Increase USER_UUID_LENGTH and USER_UUID_CHARS_POOL"
            )

    def create_user(self) -> str:
        user_id = self._get_user_id()
        self.data_manager.create_user(user_id)
        return user_id

    def add_fact(self, uuid: str, name: str, value: Hashable, state: bool):
        pass

    def add_rule(self, uuid: str, majors: Iterable[Fact_tuple], conclusions: Iterable[Fact_tuple]):
        pass

    def process(self, uuid: str):
        pass

    def get_facts(self, uuid: str) -> Set[Fact_tuple]:
        pass

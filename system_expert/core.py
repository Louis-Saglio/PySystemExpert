from typing import Hashable, Iterable, Tuple, Set

from core_lib import Engine
from data_lib import DataManager

Fact = Tuple[str, Hashable, bool]


class SystemExpert:

    def __init__(self):
        self.engine = Engine(set(), set())
        self.data_manager = DataManager()

    def get_api_key(self) -> str:
        return self.data_manager.add_user()

    def add_fact(self, uuid: str, name: str, value: Hashable, state: bool):
        pass

    def add_rule(self, uuid: str, majors: Iterable[Fact], conclusions: Iterable[Fact]):
        pass

    def process(self, uuid: str):
        pass

    def get_facts(self, uuid: str) -> Set[Fact]:
        pass


SystemExpert().add_rule("khgb", [('hb', 'uhb', True), ('h', 'val', True)], [])

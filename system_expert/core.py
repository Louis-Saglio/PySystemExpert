from random import choice
from typing import Hashable, Iterable, Tuple, Set, FrozenSet

import core_lib
import data_lib
import settings

Fact_tuple = Tuple[str, Hashable, bool]
Rule_tuple = Tuple[FrozenSet[Fact_tuple], FrozenSet[Fact_tuple]]


class SystemExpert:
    """
    Logiciel de système expert. Les méthodes public de cette classes sont les intéractions possibles avec le logiciel.
    Une instance de logiciel par utilisateur ?
    Séparer l'interface du logiciel ?

    A) On peut lancer plusieurs instances de système expert.
    B) Chaque instance agit sur les mêmes données.
    C) Chaque instance gère plusieurs utilisateurs.
    D) Plusieures connexions à un même compte utilisateur sont acceptées.
    E) Un utilisateur ne peut pas accèder aux données d'un autre utilisateur.
    F) Il n'y a qu'une base de donnée
    Donc :
    L'accès au données est asynchrone est par conséquent doit être controllé.
    Chaque requête envoyée au SE doit préciser l'utilisateur.
    Chaque entrée doit être vérifiée


    Setter methods (add_fact, add_rule) accept parameters of builtin types.

    Multiprocess intercommunication is made through database
    """

    # todo : data verification

    def __init__(self):
        self.engine = core_lib.Engine(set(), set())  # todo : Why instanciate here ?
        self.data_manager = data_lib.DataManager(':memory:' if settings.DEBUG else settings.DATA_BASE_FILE)
        # todo : check database integrity

    def _get_new_user_id(self):
        used_uuids = self.data_manager.get_used_user_uuids()
        for _ in range(1000):
            uuid = ''.join(choice(settings.USER_UUID_CHARS_POOL) for _ in range(settings.USER_UUID_LENGTH))
            if uuid not in used_uuids:
                return uuid
        else:
            raise UserWarning(
                f"Not enough user_uuid {len(used_uuids)}. Increase USER_UUID_LENGTH and USER_UUID_CHARS_POOL"
            )

    def create_user(self) -> str:
        user_id = self._get_new_user_id()
        self.data_manager.create_user(user_id)
        return user_id

    def add_fact(self, user_uuid: str, name: str, value: Hashable, state: bool):
        return self.data_manager.add_fact(user_uuid, name, value, state)

    def get_fact(self, user_uuid: str, fact_id: int):
        return self.data_manager.get_fact(user_uuid, fact_id)

    def add_rule(self, user_uuid: str, majors: Iterable[int], conclusions: Iterable[int]) -> int:
        return self.data_manager.add_rule(user_uuid, majors, conclusions)

    def process(self, uuid: str):
        pass

    def get_facts(self, user_uuid: str) -> Set[Fact_tuple]:
        return self.data_manager.get_facts(user_uuid)

    def get_rules(self, user_uuid: str) -> FrozenSet[Rule_tuple]:
        pass

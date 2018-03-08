from random import choice
from typing import Hashable, Iterable, Tuple, Set

import core_lib
import data_lib
import settings

Fact_tuple = Tuple[str, Hashable, bool]


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
    Donc :
    L'accès au données est asynchrone est par conséquent doit être controllé.
    Chaque requête envoyée au SE doit préciser l'utilisateur.


    Setter methods (add_fact, add_rule) accept parameters of builtin types.
    Getter methods (get_fact, get_facts) return custom sample type.
    Unless a specific field is precised (_get_new_user_id).
    """

    # todo : data verification

    def __init__(self):
        self.engine = core_lib.Engine(set(), set())
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

    def add_rule(self, uuid: str, majors: Iterable[Fact_tuple], conclusions: Iterable[Fact_tuple]):
        pass

    def process(self, uuid: str):
        pass

    def get_facts(self, uuid: str) -> Set[Fact_tuple]:
        pass

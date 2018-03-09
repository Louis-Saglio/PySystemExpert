import os
import sqlite3
from typing import Hashable, Tuple, Iterable

CREATE_DB_SCRIPT = os.path.join(os.path.dirname(__file__), 'create_db.sql')


class DataManager:
    """
    Classe chargée de sauvegarder et de restituer des données spécifiques aux système experts.
    Pour des raisons de performance, une base de données doit pouvoir enregistrer les données de plusieur systèmes experts.
    Par conséquent la gestion des données doit supporter le multiutilisateur, un utilisateur étant une instance de système expert.
    """

    def __init__(self, db_path: str):
        self.connexion = sqlite3.connect(db_path)
        self.db_path = db_path
        if self.db_path == ':memory:':  # todo : explicit better than implicit ?
            self.create_db()

    def create_db(self):
        with open(CREATE_DB_SCRIPT) as f:
            self.connexion.executescript(f.read())

    def create_user(self, uuid: str):
        self.connexion.execute(
            "INSERT INTO users (uuid) VALUES (?)",
            (uuid,)
        )
        self.connexion.commit()

    def _get_user_id(self, user_uuid: str) -> int:
        return self.connexion.execute(
            "SELECT id FROM users WHERE uuid = ?",
            (user_uuid,)
        ).fetchone()[0]

    def add_fact(self, user_uuid: str, name: str, value: Hashable, state: bool) -> int:
        fact_id = self.connexion.execute(
            "INSERT INTO facts (name, value, state, type, user_id) VALUES (?,?,?,?,?)",
            (name, value, state, type(value).__name__, self._get_user_id(user_uuid))
        ).lastrowid
        self.connexion.commit()
        return fact_id

    def get_used_user_uuids(self) -> set:
        return {uuid[0] for uuid in self.connexion.execute("SELECT uuid FROM users").fetchall()}

    def get_fact(self, user_uuid: str, fact_id: int) -> Tuple[str, Hashable, bool]:
        fact_data = self.connexion.execute(
            "SELECT name, value, state, type FROM facts WHERE id = ? AND user_id = ?",
            (fact_id, self._get_user_id(user_uuid))
        ).fetchone()
        fact_value = __builtins__.get(fact_data[3])(fact_data[1])
        # todo : value type must be builtin, remplace Hashable by ...
        return fact_data[0], fact_value, fact_data[2]

    def add_rule(self, user_uuid: str, majors: Iterable[int], conclusions: Iterable[int]) -> int:
        """
        :param user_uuid: self explanatory
        :param majors: an iterable of fact id
        :param conclusions: an iterable of fact id
        :return: the rule id
        """
        rule_id = self.connexion.execute(
            'INSERT INTO rules (user_id) VALUES (?)',
            (self._get_user_id(user_uuid),)
        ).lastrowid
        # todo : check if majors and conclusions exist on this user
        for major in majors:
            self.connexion.execute(
                "INSERT INTO majors (fact_id, rule_id) VALUES (?,?)",
                (major, rule_id)
            )
        for conclusion in conclusions:
            self.connexion.execute(
                "INSERT INTO conclusions (fact_id, rule_id) VALUES (?,?)",
                (conclusion, rule_id)
            )
        self.connexion.commit()
        return rule_id

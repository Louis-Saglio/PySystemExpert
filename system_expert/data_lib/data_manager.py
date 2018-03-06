import os
import sqlite3
from typing import Hashable

CREATE_DB_SCRIPT = os.path.join(os.path.dirname(__file__), 'create_db.sql')


class DataManager:

    def __init__(self, db_path: str):
        self.connexion = sqlite3.connect(db_path)
        self.db_path = db_path
        if self.db_path == ':memory:':
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

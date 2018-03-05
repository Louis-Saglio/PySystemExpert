import os
import sqlite3
from typing import Hashable

CREATE_DB_SCRIPT = os.path.join(os.path.dirname(__file__), 'create_db.sql')


class DataManager:

    def __init__(self, db_path):
        self.connexion = sqlite3.connect(db_path)
        self.db_path = db_path

    def create_db(self,):
        self.connexion.executescript(CREATE_DB_SCRIPT)

    def create_instance(self, uuid: str):
        self.connexion.execute(
            "INSERT INTO users (uuid) VALUES (?)",
            (uuid,)
        )

    def add_fact(self, instance_id: str, name: str, value: Hashable, state: bool):
        pass

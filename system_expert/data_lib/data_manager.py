import sqlite3
from typing import Hashable

import os

CREATE_DB_SCRIPT = os.path.join(os.path.dirname(__file__), 'create_db.sql')


class DataManager:

    def __init__(self, db_path):
        self.connexion = sqlite3.connect(db_path)

    def create_instance(self) -> str:
        pass

    def add_fact(self, instance_id: str, name: str, value: Hashable, state: bool):
        pass

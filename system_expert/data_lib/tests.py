import unittest

import data_manager


class TestDataManager(unittest.TestCase):

    def setUp(self):
        self.data_manager = data_manager.DataManager(':memory:')
        self.data_manager.connexion.execute("INSERT INTO users (uuid) VALUES ('test_user')")
        self.data_manager.connexion.commit()

    def test_create_instance(self):
        uuid = 'test_id'
        self.data_manager.create_user(uuid)
        self.assertEqual(
            uuid,
            self.data_manager.connexion.execute("SELECT uuid FROM users WHERE id = 2").fetchone()[0]
        )

    def test__get_user_id(self):
        self.data_manager.connexion.execute(
            "INSERT INTO users (uuid) VALUES ('foobar_uuid')"
        )
        self.assertEqual(
            2,
            self.data_manager._get_user_id("foobar_uuid")
        )

    def test_add_fact(self):
        # todo : test returned value of get_fact
        self.data_manager.add_fact("test_user", "fact", "val", True)
        self.assertEqual(
            ('fact', 'val', 1, 'str', 'test_user'),
            self.data_manager.connexion.execute(
                "SELECT f.name, f.value, f.state, f.type, u.uuid FROM facts f JOIN users u ON f.user_id = ?",
                (self.data_manager._get_user_id('test_user'),)
            ).fetchone()
        )

    def test_get_fact(self):
        # Assumes that add_fact works
        fact_id = self.data_manager.add_fact("test_user", "fact", 42, True)
        self.assertEqual(
            ("fact", 42, True),
            self.data_manager.get_fact("test_user", fact_id)
        )


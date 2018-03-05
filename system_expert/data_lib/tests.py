import unittest

from data_manager import DataManager, CREATE_DB_SCRIPT


class TestDataManager(unittest.TestCase):

    def setUp(self):
        self.data_manager = DataManager(':memory:')
        with open(CREATE_DB_SCRIPT) as f:
            self.data_manager.connexion.executescript(f.read())
        self.data_manager.connexion.execute("INSERT INTO users (uuid) VALUES ('test_user')")
        self.data_manager.connexion.commit()

    def test_create_instance(self):
        uuid = 'test_id'
        self.data_manager.create_instance(uuid)
        self.assertEqual(
            uuid,
            self.data_manager.connexion.execute("SELECT uuid FROM users WHERE id = 2").fetchone()[0]
        )

    # def test__get_user(self):
    #     self.data_manager.connexion.execute(
    #         "INSERT INTO users (uuid) VALUES ('foobar_uuid')"
    #     )
    #     self.assertEqual(
    #         2,
    #         self.data_manager._get_user("foobar_uuid")
    #     )

    def test_add_fact(self):
        self.data_manager.add_fact("test_user", "fact", "val", True)
        self.assertEqual(
            self.data_manager.connexion.execute(
                "SELECT name, value, state, type, uuid FROM facts f JOIN users u ON f.user_id = u.id"
            ).fetchone(),
            ('fact', 'val', 1, 'str', 'test_user')
        )

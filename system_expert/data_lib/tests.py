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

    def test_add_rule(self):
        # Assumes that add_facts works
        # Assumes that test_user is created
        majors = (
            self.data_manager.add_fact("test_user", "fact1", 15, True),
            self.data_manager.add_fact("test_user", "fact2", b"val", False)
        )
        conclusions = (
            self.data_manager.add_fact("test_user", "fact2", 0.77, True),
        )
        rule_id = self.data_manager.add_rule("test_user", majors, conclusions)
        expected_rule = self.data_manager.connexion.execute("SELECT id, user_id FROM rules WHERE id = ?", (rule_id,)).fetchone()
        expected_majors = self.data_manager.connexion.execute("SELECT fact_id FROM majors WHERE rule_id = ?", (rule_id,)).fetchall()
        expected_conclusion = self.data_manager.connexion.execute("SELECT fact_id FROM conclusions WHERE rule_id = ?", (rule_id,)).fetchone()[0]
        self.assertEqual(
            expected_rule,
            (rule_id, self.data_manager._get_user_id("test_user"))
        )
        self.assertEqual(
            expected_majors,
            [(majors[0],), (majors[1],)]
        )
        self.assertEqual(expected_conclusion, conclusions[0])

    def test__build_fact_from_row_data(self):
        self.assertEqual(
            ("Name", 42, False),
            (self.data_manager._build_fact_from_raw_data(("Name", "42", False, "int")))
        )

    def test_get_facts(self):
        # Assumes that add_fact works
        # Assumes that test_user is created
        self.data_manager.add_fact('test_user', 'name', 42, True)
        self.data_manager.add_fact('test_user', 'name2', b"abc", False)
        facts = self.data_manager.get_facts('test_user')
        self.assertEqual(
            {('name', 42, True), ('name2', b"abc", False)},
            facts
        )

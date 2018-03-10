import unittest

import core
import settings


class TestSystemExpert(unittest.TestCase):

    def setUp(self):
        self.system_expert = core.SystemExpert()
        self.user_uuid = self.system_expert.create_user()

    def test__get_user_id(self):
        settings.USER_UUID_LENGTH = 3
        settings.USER_UUID_CHARS_POOL = 'a'
        self.assertEqual(
            'aaa',
            self.system_expert._get_new_user_id()
        )

    def test_create_user(self):
        settings.USER_UUID_LENGTH = 1
        settings.USER_UUID_CHARS_POOL = 'a'
        user_uuid = self.system_expert.create_user()
        self.assertEqual('a', user_uuid)
        self.assertRaises(UserWarning, self.system_expert._get_new_user_id)

    def test_add_fact(self):
        fact_id = self.system_expert.add_fact(self.user_uuid, 'fact', 42, False)
        fact_data = self.system_expert.data_manager.get_fact(self.user_uuid, fact_id)
        self.assertEqual(('fact', 42, 0), fact_data)

    def test_get_fact(self):
        # Assumes that add_fact works
        fact_id = self.system_expert.add_fact(self.user_uuid, "fact", 42, True)
        self.assertEqual(
            ("fact", 42, True),
            self.system_expert.get_fact(self.user_uuid, fact_id)
        )

    def test_add_rule(self):
        # Assumes that add_fact
        majors = (
            self.system_expert.add_fact(self.user_uuid, "fact1", 15, True),
            self.system_expert.add_fact(self.user_uuid, "fact2", b"val", False)
        )
        conclusions = (self.system_expert.add_fact(self.user_uuid, "fact2", 0.77, True),)

        rule_id = self.system_expert.add_rule(self.user_uuid, majors, conclusions)

        expected_rule_id = self.system_expert.data_manager.connexion.execute(
            "SELECT id FROM rules WHERE id = ?",
            (rule_id,)
        ).fetchone()[0]
        expected_majors = self.system_expert.data_manager.connexion.execute(
            "SELECT fact_id FROM majors WHERE rule_id = ?",
            (rule_id,)
        ).fetchall()
        expected_conclusion_id = self.system_expert.data_manager.connexion.execute(
            "SELECT fact_id FROM conclusions WHERE rule_id = ?",
            (rule_id,)
        ).fetchone()[0]

        self.assertEqual(expected_rule_id, rule_id)
        self.assertEqual(expected_majors, [(majors[0],), (majors[1],)])
        self.assertEqual(expected_conclusion_id, conclusions[0])

    def test_get_facts(self):
        # Assumes that add_fact works
        self.system_expert.add_fact(self.user_uuid, 'name1', 42, False)
        self.system_expert.add_fact(self.user_uuid, 'name2', 0.42, True)
        self.assertEqual(
            self.system_expert.data_manager.get_facts(self.user_uuid),
            self.system_expert.get_facts(self.user_uuid)
        )

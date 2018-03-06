import unittest

import core
import settings


class TestSystemExpert(unittest.TestCase):

    def setUp(self):
        self.system_expert = core.SystemExpert()

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
        user_uuid = self.system_expert.create_user()
        fact_id = self.system_expert.add_fact(user_uuid, 'fact', 42, False)
        fact_data = self.system_expert.data_manager.connexion.execute(
            "SELECT name, value, state, type, user_id FROM facts WHERE id = ?",
            (fact_id,)
        ).fetchone()
        self.assertEqual(
            ('fact', '42', 0, 'int', self.system_expert.data_manager._get_user_id(user_uuid)),
            fact_data
        )

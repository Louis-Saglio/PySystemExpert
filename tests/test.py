import json
import os
import subprocess
import threading
import time
import unittest
from wsgiref import simple_server

import requests

import context
from core import DataManager


class TestRestApiCase(unittest.TestCase):
    port_gen = (i for i in range(8800, 8900))

    def setUp(self):
        ip, port = '127.0.0.1', next(self.port_gen)
        self.http_host = f'http://{ip}:{port}'
        self.server = simple_server.make_server(
            ip, port, context.api_rest.api,
            handler_class=type("NoLog", (simple_server.WSGIRequestHandler,), {"log_message": lambda *args: None})
        )
        self.thread = threading.Thread(target=self.server.serve_forever)
        self.thread.start()

    def tearDown(self):
        self.server.socket.close()
        self.server.shutdown()
        self.thread.join()


class TestFactRessource(TestRestApiCase):

    def setUp(self):
        super().setUp()
        self.url = self.http_host + '/fact'

    def test_on_post_success(self):
        response = requests.post(self.url, json={"name": "sexe", "value": "femme", "state": True})
        self.assertEqual(456573380057838825, json.loads(response.content, encoding='utf-8')["fact_id"])
        self.assertEqual(201, response.status_code)

    def test_on_post_bad_json(self):
        response = requests.post(self.url, data={"name": "sexe", "value": "femme", "state": True})
        self.assertEqual(415, response.status_code)

    def test_on_post_bad_name(self):
        response = requests.post(self.url, json={"name": "sexe", "value": "femme", "not_state": True})
        self.assertEqual(400, response.status_code)

    def test_on_post_state_not_bool(self):
        response = requests.post(self.url, json={"name": "sexe", "value": "femme", "state": "True"})
        self.assertEqual(400, response.status_code)

    def test_on_post_name_not_str(self):
        response = requests.post(self.url, json={"name": 5, "value": "femme", "state": True})
        self.assertEqual(400, response.status_code)


class TestFactsResource(TestRestApiCase):

    def setUp(self):
        super().setUp()
        self.url = self.http_host + '/facts'
        self.url_fact = self.http_host + '/fact'
        self.url_rules = self.http_host + '/rule'

    def test_on_get_success(self):
        requests.post(self.url_fact, json={"name": "sexe", "value": "femme", "state": True})
        requests.post(self.url_fact, json={"name": "age", "value": 18, "state": True})
        requests.post(
            self.url_rules,
            json={
                "majors": [{"name": "taille", "value": 1.65, "state": True}],
                "conclusions": [{"name": "marche", "value": True, "state": True}]
            }
        )
        requests.post(
            self.url_rules,
            json={
                "majors": [
                    {"name": "sexe", "value": "femme", "state": True},
                    {"name": "age", "value": 18, "state": True}
                ],
                "conclusions": [{"name": "taille", "value": 1.65, "state": True}]
            }
        )
        response = requests.get(self.url)
        self.assertEqual(
            {
                'facts': [
                    {'name': 'sexe', 'state': True, 'value': 'femme'},
                    {'name': 'marche', 'state': True, 'value': True},
                    {'name': 'age', 'state': True, 'value': 18},
                    {'name': 'taille', 'state': True, 'value': 1.65}
                ]
            },
            json.loads(response.content, encoding='utf-8')
        )
        self.assertEqual(200, response.status_code)


class TestRuleResource(TestRestApiCase):

    def setUp(self):
        super().setUp()
        self.url = self.http_host + '/rule'

    def test_on_post(self):
        rule_json = {
            "majors": [{"name": "f1", "value": "v1", "state": True}],
            "conclusions": [{"name": "f2", "value": "v2", "state": True}]
        }
        response = requests.post(self.url, json=rule_json)
        self.assertEqual(836216383422732259, json.loads(response.content, encoding='utf-8')["rule_id"])
        self.assertEqual(201, response.status_code)

    def test_on_post_bad_fact(self):
        rule_json = {
            "majors": [{"name": 42, "value": "v1", "state": True}],
            "conclusions": [{"name": "f2", "value": "v2", "state": True}]
        }
        response = requests.post(self.url, json=rule_json)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            json.loads(response.content, encoding='utf-8')["message"],
            "self.NAME class must be str, not int"
        )

    def test_on_post_bad_json_key(self):
        rule_json = {
            "majors": [{"name": "f1", "value": "v1", "state": True}],
            "bad_key": [{"name": "f3", "value": "v3", "state": False}],
            "conclusions": [{"name": "f2", "value": "v2", "state": True}]
        }
        response = requests.post(self.url, json=rule_json)
        self.assertEqual(836216383422732259, json.loads(response.content, encoding='utf-8')["rule_id"])
        self.assertEqual(201, response.status_code)

    def test_on_post_bad_json_value(self):
        rule_json = {
            "majors": [{"name": "f1", "value": "v1", "state": True}],
            "conclusions": "bad_value"
        }
        response = requests.post(self.url, json=rule_json)
        self.assertEqual(400, response.status_code)


class TestRun(unittest.TestCase):

    def test_run_default_config(self):
        os.chdir(config.PROJECT_ROOT_DIR)
        os.chdir(config.REST_API_DIR)
        run = subprocess.Popen(f"python {config.REST_API_RUNNING_SCRPIT}".split())
        time.sleep(1)
        response = requests.get(f"http://{config.HTTP_SERVER_ADDRESS}:{config.HTTP_SERVER_PORT}/facts")
        self.assertEqual(response.content, b'{"facts": []}')
        run.terminate()


class TestDataManager(unittest.TestCase):

    def setUp(self):
        self.data_manager = DataManager(':memory:')
        with open(
            os.path.join(
                config.PROJECT_ROOT_DIR,
                os.path.join(config.DATA_DIR, config.CREATE_DATA_BASE_SCRIPT)
            )
        ) as f:
            self.data_manager.connexion.executescript(f.read())
        self.data_manager.connexion.execute("INSERT INTO users (uuid) VALUES ('test_user')")
        self.data_manager.connexion.commit()

    def test_add_user(self):
        uuid = self.data_manager.add_user()
        self.assertTrue(set(uuid).issubset(set(config.USER_UUID_CHARS)))
        self.assertEqual(
            uuid,
            self.data_manager.connexion.execute("SELECT uuid FROM users WHERE id = 2").fetchone()[0]
        )

    def test__get_user(self):
        self.data_manager.connexion.execute(
            "INSERT INTO users (uuid) VALUES ('foobar_uuid')"
        )
        self.assertEqual(
            2,
            self.data_manager._get_user("foobar_uuid")
        )

    def test_add_fact(self):
        self.data_manager.add_fact("test_user", context.Fact("fact", "val", True))
        self.assertEqual(
            self.data_manager.connexion.execute(
                "SELECT name, value, state, type, uuid FROM facts f JOIN users u ON f.user_id = u.id"
            ).fetchone(),
            ('fact', 'val', 1, 'str', 'test_user')
        )

import json
import threading
import unittest
from wsgiref import simple_server

import requests

import context
import data


class TestFact(unittest.TestCase):

    def test_init(self):
        f1 = context.Fact("a", "b", True)
        f2 = context.Fact(name="a", value="b", state=True)
        self.assertEqual(
            (f1.NAME, f1.VALUE, f1.STATE),
            (f2.NAME, f2.VALUE, f2.STATE)
        )
        self.assertIsInstance(f1.NAME, str)
        self.assertIsInstance(f1.VALUE, str)
        self.assertIsInstance(f1.STATE, bool)

    def test_repr(self):
        f1 = context.Fact("a", "b", True)
        f2 = context.Fact("a", "b", True)
        self.assertEqual(repr(f1), repr(f2))

    def test_hash(self):
        f1 = context.Fact("a", "b", True)
        f2 = context.Fact("a", "b", True)
        self.assertEqual(hash(f1), hash(f2))

    def test_eq(self):
        f1 = context.Fact("a", "b", True)
        f2 = context.Fact("a", "b", True)
        self.assertEqual(f1, f2)

    def test_get_contrary(self):
        f1 = context.Fact("a", "b", True)
        f2 = context.Fact("a", "b", False)
        self.assertEqual(f1.get_contrary(), f2)


class TestRule(unittest.TestCase):

    def test_init(self):
        rule = context.Rule(frozenset(data.FACTS), frozenset((context.Fact("a", "b", True),)))
        self.assertIsInstance(rule.CONCLUSIONS, frozenset)
        self.assertIsInstance(rule.MAJORS, frozenset)
        for conclusion in rule.CONCLUSIONS:
            self.assertIsInstance(conclusion, context.Fact)
        for major in rule.MAJORS:
            self.assertIsInstance(major, context.Fact)


class TestEngine(unittest.TestCase):

    def test_init(self):
        engine = context.Engine(data.FACTS, data.RULES)
        self.assertIsInstance(engine.facts, set)
        self.assertIsInstance(data.RULES, set)
        for fact in engine.facts:
            self.assertIsInstance(fact, context.Fact)
        for rule in engine.rules:
            self.assertIsInstance(rule, context.Rule)

    def test_make_syllogism(self):
        engine = context.Engine(data.FACTS, data.RULES)
        engine._make_syllogism()
        self.assertIn(context.Fact("la race", "germanique", False), engine.facts)

    def test_check_contrary(self):
        engine = context.Engine(data.FACTS, data.RULES)
        engine.facts.add(context.Fact("la race", "germanique", False))
        self.assertRaises(AssertionError, engine.check_contrary)

    def test__remove_useless_rules__contrary_case(self):
        facts = {
            context.Fact("la couleur des cheveux", "noire", True),
            context.Fact("la race", "germanique", True)
        }
        rules = {
            context.Rule(
                majors=context.helpers.new_frozenset(
                    context.Fact("la couleur des cheveux", "noire", True)
                ),
                conclusions=context.helpers.new_frozenset(
                    context.Fact("la race", "germanique", False)
                )
            )
        }
        engine = context.Engine(facts, rules)
        engine._remove_useless_rules()
        self.assertNotIn(
            context.Rule(
                majors=context.helpers.new_frozenset(
                    context.Fact("la couleur des cheveux", "noire", True)
                ),
                conclusions=context.helpers.new_frozenset(
                    context.Fact("la race", "germanique", False)
                )
            ),
            engine.rules
        )

    def test__remove_useless_rules(self):
        facts = {
            context.Fact("la couleur des cheveux", "noire", True),
            context.Fact("la race", "germanique", True)
        }
        rules = {
            context.Rule(
                majors=context.helpers.new_frozenset(
                    context.Fact("la couleur des cheveux", "noire", True)
                ),
                conclusions=context.helpers.new_frozenset(
                    context.Fact("la race", "germanique", True)
                )
            )
        }
        engine = context.Engine(facts, rules)
        engine._remove_useless_rules()
        self.assertNotIn(
            context.Rule(
                majors=context.helpers.new_frozenset(
                    context.Fact("la couleur des cheveux", "noire", True)
                ),
                conclusions=context.helpers.new_frozenset(
                    context.Fact("la race", "germanique", True)
                )
            ),
            engine.rules
        )

    def test_process(self):
        engine = context.Engine(data.PROCESS_FACTS, data.PROCESS_RULES)
        engine._make_syllogism()
        engine.process()
        self.assertIn(context.Fact("marche", "haha", True), engine.facts)


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
        response = requests.post(self.url, json={"name": "sexe", "value": "femme", "foo": True})
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

    def test_on_get_success(self):
        requests.post(self.url_fact, json={"name": "sexe", "value": "femme", "state": True})
        requests.post(self.url_fact, json={"name": "age", "value": "18", "state": True})
        response = requests.get(self.url)
        self.assertEqual(
            {
                "facts": [
                    {"name": "sexe", "value": "femme", "state": True},
                    {'name': 'age', 'state': True, 'value': '18'}
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
        pass

    def test_on_post_bad_json_value(self):
        pass

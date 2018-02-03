import json
import threading
import unittest

import requests

import data
import context


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

    def test_process(self):
        engine = context.Engine(data.PROCESS_FACTS, data.PROCESS_RULES)
        engine._make_syllogism()
        engine.process()
        self.assertIn(context.Fact("marche", "haha", True), engine.facts)


class TestFactRessource(unittest.TestCase):

    from wsgiref import simple_server
    server = simple_server.make_server('127.0.0.1', 8800, context.api_rest.api)
    thread = threading.Thread(target=server.serve_forever)

    @classmethod
    def setUpClass(cls):
        cls.thread.start()

    def test_on_post_success(self):
        response = requests.post('http://127.0.0.1:8800/fact', json={"name": "sexe", "value": "femme", "state": True})
        self.assertEqual(json.loads(response.content, encoding='utf-8')["fact_id"], 456573380057838825)
        self.assertEqual(response.status_code, 201)

    def test_on_post_bad_json(self):
        response = requests.post('http://127.0.0.1:8800/fact', data={"name": "sexe", "value": "femme", "state": True})
        self.assertEqual(response.status_code, 415)

    def test_on_post_bad_name(self):
        response = requests.post('http://127.0.0.1:8800/fact', json={"name": "sexe", "value": "femme", "foo": True})
        self.assertEqual(response.status_code, 400)

    def test_on_post_state_not_bool(self):
        response = requests.post('http://127.0.0.1:8800/fact', json={"name": "sexe", "value": "femme", "state": "True"})
        self.assertEqual(response.status_code, 400)

    def test_on_post_name_not_str(self):
        response = requests.post('http://127.0.0.1:8800/fact', json={"name": 5, "value": "femme", "state": True})
        self.assertEqual(response.status_code, 400)

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.thread.join()

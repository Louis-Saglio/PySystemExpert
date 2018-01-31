import unittest
from context import system_expert as se
import data


class TestFact(unittest.TestCase):

    def test_init(self):
        f1 = se.Fact("a", "b", True)
        f2 = se.Fact(name="a", value="b", state=True)
        self.assertEqual(
            (f1.NAME, f1.VALUE, f1.STATE),
            (f2.NAME, f2.VALUE, f2.STATE)
        )
        self.assertIsInstance(f1.NAME, str)
        self.assertIsInstance(f1.VALUE, str)
        self.assertIsInstance(f1.STATE, bool)

    def test_repr(self):
        f1 = se.Fact("a", "b", True)
        f2 = se.Fact("a", "b", True)
        self.assertEqual(repr(f1), repr(f2))

    def test_hash(self):
        f1 = se.Fact("a", "b", True)
        f2 = se.Fact("a", "b", True)
        self.assertEqual(hash(f1), hash(f2))

    def test_eq(self):
        f1 = se.Fact("a", "b", True)
        f2 = se.Fact("a", "b", True)
        self.assertEqual(f1, f2)

    def test_get_contrary(self):
        f1 = se.Fact("a", "b", True)
        f2 = se.Fact("a", "b", False)
        self.assertEqual(f1.get_contrary(), f2)


class TestRule(unittest.TestCase):

    def test_init(self):
        rule = se.Rule(frozenset(data.FACTS), frozenset((se.Fact("a", "b", True),)))
        self.assertIsInstance(rule.CONCLUSIONS, frozenset)
        self.assertIsInstance(rule.MAJORS, frozenset)
        for conclusion in rule.CONCLUSIONS:
            self.assertIsInstance(conclusion, se.Fact)
        for major in rule.MAJORS:
            self.assertIsInstance(major, se.Fact)


class TestEngine(unittest.TestCase):

    def test_init(self):
        engine = se.Engine(data.FACTS, data.RULES)
        self.assertIsInstance(engine.facts, set)
        self.assertIsInstance(data.RULES, set)
        for fact in engine.facts:
            self.assertIsInstance(fact, se.Fact)
        for rule in engine.rules:
            self.assertIsInstance(rule, se.Rule)

    def test_make_syllogism(self):
        engine = se.Engine(data.FACTS, data.RULES)
        engine.make_syllogism()
        self.assertIn(se.Fact("la race", "germanique", False), engine.facts)

    def test_check_contrary(self):
        engine = se.Engine(data.FACTS, data.RULES)
        engine.facts.add(se.Fact("la race", "germanique", False))
        self.assertRaises(AssertionError, engine.check_contrary)

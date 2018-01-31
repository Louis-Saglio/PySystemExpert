from unittest import TestCase

from main import Fact, Rule, FACTS, new_frozenset


class TestFact(TestCase):

    def test_init(self):
        f1 = Fact("a", "b", True)
        f2 = Fact(name="a", value="b", state=True)
        self.assertEqual(
            (f1.NAME, f1.VALUE, f1.STATE),
            (f2.NAME, f2.VALUE, f2.STATE)
        )
        self.assertIsInstance(f1.NAME, str)
        self.assertIsInstance(f1.VALUE, str)
        self.assertIsInstance(f1.STATE, bool)

    def test_repr(self):
        f1 = Fact("a", "b", True)
        f2 = Fact("a", "b", True)
        self.assertEqual(repr(f1), repr(f2))

    def test_hash(self):
        f1 = Fact("a", "b", True)
        f2 = Fact("a", "b", True)
        self.assertEqual(hash(f1), hash(f2))

    def test_eq(self):
        f1 = Fact("a", "b", True)
        f2 = Fact("a", "b", True)
        self.assertEqual(f1, f2)

    def test_get_contrary(self):
        f1 = Fact("a", "b", True)
        f2 = Fact("a", "b", False)
        self.assertEqual(f1.get_contrary(), f2)


class TestRule(TestCase):

    def test_init(self):
        rule = Rule(frozenset(FACTS), new_frozenset(Fact("a", "b", True)))
        self.assertIsInstance(rule.CONCLUSIONS, frozenset)
        self.assertIsInstance(rule.MAJORS, frozenset)
        for conclusion in rule.CONCLUSIONS:
            self.assertIsInstance(conclusion, Fact)
        for major in rule.MAJORS:
            self.assertIsInstance(major, Fact)


class TestEngine(TestCase):

    def test_sylogism(self):
        pass

    def test_check_contraries(self):
        pass

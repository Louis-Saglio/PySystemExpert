import unittest
import helpers
import engine as core


FACTS = {
    core.Fact("la couleur des cheveux", "noire", True),
    core.Fact("la race", "germanique", True)
}


RULES = {
    core.Rule(
        majors=helpers.new_frozenset(
            core.Fact("la couleur des cheveux", "noire", True)
        ),
        conclusions=helpers.new_frozenset(
            core.Fact("la race", "germanique", False)
        )
    )
}


PROCESS_FACTS = {core.Fact("test", "t_value", True)}

PROCESS_RULES = {
    core.Rule(
        majors=helpers.new_frozenset(
            core.Fact("foo", "f_value", True)
        ),
        conclusions=helpers.new_frozenset(
            core.Fact("marche", "haha", True)
        )
    ),
    core.Rule(
        majors=helpers.new_frozenset(
            core.Fact("test", "t_value", True)
        ),
        conclusions=helpers.new_frozenset(
            core.Fact("foo", "f_value", True)
        )
    )
}


class TestFact(unittest.TestCase):

    def test_init(self):
        f1 = core.Fact("a", "b", True)
        f2 = core.Fact(name="a", value="b", state=True)
        self.assertEqual(
            (f1.NAME, f1.VALUE, f1.STATE),
            (f2.NAME, f2.VALUE, f2.STATE)
        )
        self.assertIsInstance(f1.NAME, str)
        self.assertIsInstance(f1.VALUE, str)
        self.assertIsInstance(f1.STATE, bool)

    def test_repr(self):
        f1 = core.Fact("a", "b", True)
        f2 = core.Fact("a", "b", True)
        self.assertEqual(repr(f1), repr(f2))

    def test_hash(self):
        f1 = core.Fact("a", "b", True)
        f2 = core.Fact("a", "b", True)
        self.assertEqual(hash(f1), hash(f2))

    def test_eq(self):
        f1 = core.Fact("a", "b", True)
        f2 = core.Fact("a", "b", True)
        self.assertEqual(f1, f2)

    def test_get_contrary(self):
        f1 = core.Fact("a", "b", True)
        f2 = core.Fact("a", "b", False)
        self.assertEqual(f1.get_contrary(), f2)


class TestRule(unittest.TestCase):

    def test_init(self):
        rule = core.Rule(frozenset(FACTS), frozenset((core.Fact("a", "b", True),)))
        self.assertIsInstance(rule.CONCLUSIONS, frozenset)
        self.assertIsInstance(rule.MAJORS, frozenset)
        for conclusion in rule.CONCLUSIONS:
            self.assertIsInstance(conclusion, core.Fact)
        for major in rule.MAJORS:
            self.assertIsInstance(major, core.Fact)


class TestEngine(unittest.TestCase):

    def test_init(self):
        engine = core.Engine(FACTS, RULES)
        self.assertIsInstance(engine.facts, set)
        self.assertIsInstance(RULES, set)
        for fact in engine.facts:
            self.assertIsInstance(fact, core.Fact)
        for rule in engine.rules:
            self.assertIsInstance(rule, core.Rule)

    def test_make_syllogism(self):
        engine = core.Engine(FACTS, RULES)
        engine._make_syllogism()
        self.assertIn(core.Fact("la race", "germanique", False), engine.facts)

    def test_check_contrary(self):
        engine = core.Engine(FACTS, RULES)
        engine.facts.add(core.Fact("la race", "germanique", False))
        self.assertRaises(AssertionError, engine.check_contrary)

    def test__remove_useless_rules__contrary_case(self):
        facts = {
            core.Fact("la couleur des cheveux", "noire", True),
            core.Fact("la race", "germanique", True)
        }
        rules = {
            core.Rule(
                majors=helpers.new_frozenset(
                    core.Fact("la couleur des cheveux", "noire", True)
                ),
                conclusions=helpers.new_frozenset(
                    core.Fact("la race", "germanique", False)
                )
            )
        }
        engine = core.Engine(facts, rules)
        engine._remove_useless_rules()
        self.assertNotIn(
            core.Rule(
                majors=helpers.new_frozenset(
                    core.Fact("la couleur des cheveux", "noire", True)
                ),
                conclusions=helpers.new_frozenset(
                    core.Fact("la race", "germanique", False)
                )
            ),
            engine.rules
        )

    def test__remove_useless_rules(self):
        facts = {
            core.Fact("la couleur des cheveux", "noire", True),
            core.Fact("la race", "germanique", True)
        }
        rules = {
            core.Rule(
                majors=helpers.new_frozenset(
                    core.Fact("la couleur des cheveux", "noire", True)
                ),
                conclusions=helpers.new_frozenset(
                    core.Fact("la race", "germanique", True)
                )
            )
        }
        engine = core.Engine(facts, rules)
        engine._remove_useless_rules()
        self.assertNotIn(
            core.Rule(
                majors=helpers.new_frozenset(
                    core.Fact("la couleur des cheveux", "noire", True)
                ),
                conclusions=helpers.new_frozenset(
                    core.Fact("la race", "germanique", True)
                )
            ),
            engine.rules
        )

    def test_process(self):
        engine = core.Engine(PROCESS_FACTS, PROCESS_RULES)
        engine._make_syllogism()
        engine.process()
        self.assertIn(core.Fact("marche", "haha", True), engine.facts)
        self.assertNotIn(
            core.Rule(
                majors=helpers.new_frozenset(
                    core.Fact("foo", "f_value", True)
                ),
                conclusions=helpers.new_frozenset(
                    core.Fact("marche", "haha", True)
                )
            ),
            engine.rules
        )

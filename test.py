from unittest import TestCase

from main import Fact


class TestFact(TestCase):

    def test_init(self):
        f1 = Fact("a", "b", True)
        f2 = Fact(name="a", value="b", state=True)
        self.assertEqual(
            (f1.name, f1.value, f1.state),
            (f2.name, f2.value, f2.state)
        )

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


class TestEngine(TestCase):

    def test_sylogism(self):
        pass

    def test_check_contraries(self):
        pass

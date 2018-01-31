from typing import Set, FrozenSet


def new_frozenset(*args):
    return frozenset(args)


class Fact:

    def __init__(self, name: str, value: str, state: bool):
        self.VALUE = value
        self.NAME = name
        self.STATE = state

    def __repr__(self):
        return f"{self.NAME} est {self.VALUE} : {self.STATE}"

    def __hash__(self):
        """Pour pouvoir stocker un Fact dans un set"""
        return int(''.join(str(ord(l)) for l in self.__repr__()))

    def __eq__(self, other: "Fact"):
        """Fact('abc', 'def', True) == Fact('abc', 'def', True)"""
        return hash(self) == hash(other)

    def get_contrary(self) -> "Fact":
        return Fact(self.NAME, self.VALUE, not self.STATE)


class Rule:

    def __init__(self, majors: FrozenSet[Fact], conclusions: FrozenSet[Fact]):
        self.CONCLUSIONS = conclusions
        self.MAJORS = majors


class Engine:

    def __init__(self, facts: Set[Fact], rules: Set[Rule]):
        self.facts = facts
        self.rules = rules

    def sylogism(self):
        for rule in self.rules:
            if self.facts.issuperset(rule.MAJORS):
                self.facts.update(rule.CONCLUSIONS)

    def check_contraries(self):
        for fact in self.facts:
            assert fact.get_contrary() not in self.facts, f"'{fact}' et son contraire sont dans la base de faits"


FACTS = {
    Fact("la couleur des cheveux", "noire", True),
    Fact("la race", "germanique", True)
}


RULES = {
    Rule(
        majors=new_frozenset(
            Fact("la couleur des cheveux", "noire", True)
        ),
        conclusions=new_frozenset(
            Fact("la race", "germanique", False)
        )
    )
}


if __name__ == '__main__':
    engine = Engine(FACTS, RULES)
    engine.sylogism()
    # engine.check_contraries()

    print(engine.facts)

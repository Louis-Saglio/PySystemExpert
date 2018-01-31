from typing import Set


class Fact:

    def __init__(self, name: str, value: str, state: bool):
        self.value = value
        self.name = name
        self.state = state

    def __repr__(self):
        return f"{self.name} est {self.value} : {self.state}"

    def __hash__(self):
        """Pour pouvoir stocker un Fact dans un set"""
        return int(''.join(str(ord(l)) for l in self.__repr__()))

    def __eq__(self, other: "Fact"):
        """Fact('abc', 'def', True) == Fact('abc', 'def', True)"""
        return hash(self) == hash(other)

    def get_contrary(self) -> "Fact":
        return Fact(self.name, self.value, not self.state)


class Rule:

    def __init__(self, majors: Set[Fact], conclusions: Set[Fact]):
        self.conclusions = conclusions
        self.majors = majors


class Engine:

    def __init__(self, facts: Set[Fact], rules: Set[Rule]):
        self.facts = facts
        self.rules = rules

    def sylogism(self):
        for rule in self.rules:
            if self.facts.issuperset(rule.majors):
                self.facts.update(rule.conclusions)

    def check_contraries(self):
        for fact in self.facts:
            assert fact.get_contrary() not in self.facts, f"'{fact}' et son contraire sont dans la base de faits"


FACTS = {
    Fact("la couleur des cheveux", "noire", True),
    Fact("la race", "germanique", True)
}


RULES = {
    Rule(
        {Fact("la couleur des cheveux", "noire", True)},
        {Fact("la race", "germanique", False)}
    )
}


if __name__ == '__main__':
    engine = Engine(FACTS, RULES)
    engine.sylogism()
    # engine.check_contraries()

    print(engine.facts)

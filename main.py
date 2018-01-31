class Fact:

    def __init__(self, name: str, value: str, state: bool):
        self.value = value
        self.name = name
        self.state = state

    def __repr__(self):
        return f"{self.name} est {self.value} : {self.state}"

    def __hash__(self):
        return int(''.join(str(ord(l)) for l in self.__repr__()))

    def __eq__(self, other: "Fact"):
        return hash(self) == hash(other)

    def get_contrary(self):
        return Fact(self.name, self.value, not self.state)


class Rule:

    def __init__(self, majors: set, conclusions: set):
        self.conclusions = conclusions
        self.majors = majors


class Engine:

    def __init__(self, facts, rules):
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


engine = Engine(FACTS, RULES)
engine.sylogism()
engine.check_contraries()


print(engine.facts)

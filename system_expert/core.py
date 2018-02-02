from typing import Set, FrozenSet


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

    def __repr__(self):
        return f"Majors : {self.MAJORS}\tConclusions : {self.CONCLUSIONS}"


class Engine:
    # todo: facts et rules public ?

    def __init__(self, facts: Set[Fact], rules: Set[Rule]):
        self.facts = facts
        self.rules = rules

    def _make_syllogism(self) -> Set[Rule]:
        """Si les majors d'une règle sont contenu dans self.facts, y ajoute ses conclusions
        return les règles matchées
        """
        matched_rules = set()
        for rule in self.rules:
            if self.facts.issuperset(rule.MAJORS):
                matched_rules.add(rule)
                self.facts.update(rule.CONCLUSIONS)
        return matched_rules

    def check_contrary(self):
        for fact in self.facts:
            assert fact.get_contrary() not in self.facts, f"'{fact}' et son contraire sont dans la base de faits"

    def _remove_from_rules(self, rules):
        for rule in rules:
            self.rules.discard(rule)

    def process(self):
        """Applique les règles logiques à self.facts jusqu'à ce qu'elles ne le modifient plus"""
        ended = False
        while not ended:
            matched_rules = self._make_syllogism()
            self._remove_from_rules(matched_rules)
            ended = not bool(matched_rules)

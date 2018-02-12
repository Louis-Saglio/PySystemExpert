import copy
from typing import Set, FrozenSet, Any

from exceptions import BadFactField


class Fact:

    def __init__(self, name: str, value: Any, state: bool, check: bool=False):
        self.VALUE = value
        self.NAME = name
        self.STATE = state
        if check:
            self.check_fields()

    def __repr__(self):
        return f"{self.NAME} est {self.VALUE} : {self.STATE}"

    def __hash__(self):
        """Pour pouvoir stocker un Fact dans un set
        Un objet Fact ayant les même valeurs aura le même hash dans toutes les sessions"""
        # todo: redefine fact hash
        return int(''.join(str(ord(l)) for l in self.__repr__()))

    def __eq__(self, other: "Fact"):
        """Fact('abc', 'def', True) == Fact('abc', 'def', True)
        Pouvoir comparer un fact présent dans une rule sans que ce soit la même instance :
        sans avoir de base de faits centralisée"""
        return hash(self) == hash(other)

    def get_contrary(self) -> "Fact":
        return Fact(self.NAME, self.VALUE, not self.STATE)

    def check_fields(self):
        if not isinstance(self.NAME, str):
            raise BadFactField(f"self.NAME class must be str, not {self.NAME.__class__.__name__}")
        if not isinstance(self.STATE, bool):
            raise BadFactField(f"self.STATE class must be bool, not {self.STATE.__class__.__name__}")


class Rule:

    def __init__(self, majors: FrozenSet[Fact], conclusions: FrozenSet[Fact]):
        self.CONCLUSIONS = conclusions
        self.MAJORS = majors

    def __repr__(self):
        return f"Majors : {self.MAJORS}\tConclusions : {self.CONCLUSIONS}"

    def __hash__(self):
        """Must define hash to be hashable if an __eq__ is defined
        Un objet Rule ayant les même valeurs aura le même hash dans toutes les sessions"""
        # todo compute hash in init ? || Value change instance simule change ?
        return int(''.join(str(ord(l)) for l in self.__repr__()))

    def __eq__(self, other):
        """Pouvoir comparer une rule présente dans engine sans que ce soit la même instance :
        sans avoir de base de rules centralisée"""
        return hash(self) == hash(other)


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

    def _remove_useless_rules(self):
        for rule in copy.copy(self.rules):
            if rule.CONCLUSIONS.issubset(self.facts) or {CONCLUSION.get_contrary() for CONCLUSION in rule.CONCLUSIONS}.union(self.facts):
                self.rules.remove(rule)

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

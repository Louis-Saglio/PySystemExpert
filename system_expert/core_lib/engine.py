from typing import Set

import copy

from beans import Fact, Rule


class Engine:
    """
    Effectue des opérations spécifiques aux systèmes experts sur un ensemble logiciel de faits (type Fact) et de règles (type Rule)
    """

    # todo: facts et rules public ?

    def __init__(self, facts: Set[Fact], rules: Set[Rule]):
        self.facts = facts
        self.rules = rules

    def _make_syllogism(self) -> Set[Rule]:
        """Si les majors d'une règle sont contenu dans self.facts, y ajoute ses conclusions
        return les règles matchées"""
        matched_rules = set()
        for rule in self.rules:
            if self.facts.issuperset(rule.MAJORS):
                matched_rules.add(rule)
                self.facts.update(rule.CONCLUSIONS)
        return matched_rules

    def check_contrary(self):
        # todo : unused
        for fact in self.facts:
            assert fact.get_contrary() not in self.facts, f"'{fact}' et son contraire sont dans la base de faits"

    def _remove_useless_rules(self):
        """Not thread safe"""
        for rule in copy.copy(self.rules):
            # todo use issuperset
            if rule.CONCLUSIONS.issubset(self.facts) or {CONCLUSION.get_contrary() for CONCLUSION in rule.CONCLUSIONS}.union(self.facts):
                self.rules.remove(rule)

    def process(self):
        """Applique les règles logiques à self.facts jusqu'à ce qu'elles ne le modifient plus
        Not thread safe"""
        while True:
            nbr_facts = len(self.facts)
            self._make_syllogism()
            self._remove_useless_rules()
            if len(self.facts) == nbr_facts:  # S'il n'y a pas de nouveaux faits on quite
                break
            else:
                assert len(self.facts) > nbr_facts

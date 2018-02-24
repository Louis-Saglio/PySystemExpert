import copy
import os
import random
import sqlite3
import string
from typing import Set, FrozenSet, Any

import config
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
        # todo : unused
        for fact in self.facts:
            assert fact.get_contrary() not in self.facts, f"'{fact}' et son contraire sont dans la base de faits"

    def _remove_useless_rules(self):
        for rule in copy.copy(self.rules):
            # todo use issuperset
            if rule.CONCLUSIONS.issubset(self.facts) or {CONCLUSION.get_contrary() for CONCLUSION in rule.CONCLUSIONS}.union(self.facts):
                self.rules.remove(rule)

    def process(self):
        """Applique les règles logiques à self.facts jusqu'à ce qu'elles ne le modifient plus"""
        while True:
            nbr_facts = len(self.facts)
            self._make_syllogism()
            self._remove_useless_rules()
            if len(self.facts) == nbr_facts:  # S'il n'y a pas de nouveaux faits on quite
                break
            else:
                assert len(self.facts) > nbr_facts


class DataManager:

    def __init__(self):
        self.connexion = sqlite3.connect(os.path.join(config.PROJECT_ROOT_DIR, config.DATA_BASE_FILE))

    def _get_user(self, uuid: str):
        return self.connexion.cursor().execute(
            "SELECT id FROM users WHERE uuid = ?",
            (uuid,)
        ).fetchone()[0]

    def add_fact(self, uuid: str, fact: Fact):
        cursor = self.connexion.cursor()
        cursor.execute(
            "INSERT INTO facts (name, value, state, type, user_id) VALUES (?,?,?,?,?)",
            (fact.NAME, fact.VALUE, fact.STATE, str(fact.VALUE.__class__), self._get_user(uuid))
        )
        self.connexion.commit()

    def __del__(self):
        self.connexion.close()

    def create_user(self):
        cursor = self.connexion.cursor()
        uuid = ''.join(random.sample(string.ascii_letters + string.digits, config.USER_UUID_LENGTH))
        cursor.execute("INSERT INTO users (uuid) VALUES (?)", (uuid,))
        self.connexion.commit()
        return uuid


class SystemExpert:

    def __init__(self):
        self.engine = Engine(set(), set())
        self.data_manager = DataManager()

    def get_api_key(self):
        return self.data_manager.create_user()

    def add_fact(self, uuid: str, fact: Fact):
        self.data_manager.add_fact(uuid, fact)

    def add_rule(self, uuid: str, rule: Rule):
        pass

    def process(self, uuid: str):
        pass

    def get_facts(self, uuid: str) -> Set[Fact]:
        pass

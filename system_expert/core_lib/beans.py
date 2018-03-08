from typing import Any, FrozenSet, Hashable
from exceptions import BadFactField


"""
Les méthodes des classes bean ne doivent pas interagir avec un objet externe pour être totalement découplées.
Les méthodes des classes bean ne doivent pas modifier leurs propres attributs pour être thread safe
Les attributs publics d'un objet bean ne doivent contenir que des données spécifiques à la classe de cette objet.
Des attributs privés peuvent être utilisés en tant que variable helper.
"""


class Fact:
    """
    Class bean destiner à modéliser un fait
    """

    def __init__(self, name: str, value: Hashable, state: bool, check: bool=False):
        self.VALUE = value
        self.NAME = name
        self.STATE = state
        if check:
            self._check_fields()

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

    def _check_fields(self):
        # todo : unused
        # todo : check if state is Hashable
        if not isinstance(self.NAME, str):
            raise BadFactField(f"self.NAME class must be str, not {self.NAME.__class__.__name__}")
        if not isinstance(self.STATE, bool):
            raise BadFactField(f"self.STATE class must be bool, not {self.STATE.__class__.__name__}")


class Rule:
    """
    Classe destinée à modéliser une règle
    """

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

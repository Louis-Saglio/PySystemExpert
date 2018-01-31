from system_expert.core import Fact, Rule
from system_expert.helpers import new_frozenset

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

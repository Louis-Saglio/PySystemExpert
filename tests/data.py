import context

FACTS = {
    context.Fact("la couleur des cheveux", "noire", True),
    context.Fact("la race", "germanique", True)
}


RULES = {
    context.Rule(
        majors=context.helpers.new_frozenset(
            context.Fact("la couleur des cheveux", "noire", True)
        ),
        conclusions=context.helpers.new_frozenset(
            context.Fact("la race", "germanique", False)
        )
    )
}


PROCESS_FACTS = {context.Fact("test", "t_value", True)}

PROCESS_RULES = {
    context.Rule(
        majors=context.helpers.new_frozenset(
            context.Fact("foo", "f_value", True)
        ),
        conclusions=context.helpers.new_frozenset(
            context.Fact("marche", "haha", True)
        )
    ),
    context.Rule(
        majors=context.helpers.new_frozenset(
            context.Fact("test", "t_value", True)
        ),
        conclusions=context.helpers.new_frozenset(
            context.Fact("foo", "f_value", True)
        )
    )
}

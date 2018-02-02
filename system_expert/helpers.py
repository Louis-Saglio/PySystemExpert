def new_frozenset(*args) -> frozenset:
    return frozenset(args)


def status(http_status):
    return f"{http_status.value} {http_status.phrase}"

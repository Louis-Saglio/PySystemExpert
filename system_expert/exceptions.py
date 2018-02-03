class SystemExpertException(BaseException):
    pass


class FactException(SystemExpertException):
    pass


class BadFactField(FactException):
    pass

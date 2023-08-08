"All exceptions for e620py"

class E620pyException(Exception):
    pass

class NetworkError(E620pyException):
    pass

class NoResults(E620pyException):
    pass

class AlreadyExists(E620pyException):
    pass

class InvalidArgs(E620pyException):
    pass

class RateLimited(E620pyException):
    pass
